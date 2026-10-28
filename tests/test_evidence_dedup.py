import subprocess
import json
import re

from rewardguard import config, content_evidence, content_review, gitops


def git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), *args], check=True,
                          text=True, capture_output=True).stdout.strip()


def fixture_repo(tmp_path):
    git(tmp_path, 'init', '-q', '-b', 'main')
    git(tmp_path, 'config', 'user.email', 'test@example.test')
    git(tmp_path, 'config', 'user.name', 'Test')
    (tmp_path / 'facts.md').write_text('# Product\n' + 'Trusted product claim. ' * 60 + '\n')
    (tmp_path / 'page.html').write_text('<main>Old offer</main>\n')
    (tmp_path / 'layout.html').write_text('<main>' + 'Shared layout information. ' * 70 + '</main>\n')
    git(tmp_path, 'add', '.')
    git(tmp_path, 'commit', '-qm', 'base')
    base = git(tmp_path, 'rev-parse', 'HEAD')
    (tmp_path / 'page.html').write_text('<main>' + 'New offer with proof. ' * 70 + '</main>\n')
    git(tmp_path, 'add', '.')
    git(tmp_path, 'commit', '-qm', 'change')
    return base, git(tmp_path, 'rev-parse', 'HEAD')


def test_dedup_preserves_roles_codes_revisions_and_budget_admission(tmp_path):
    base, head = fixture_repo(tmp_path)
    cfg = config.Config(install=None, suites=[], run_tests=False)
    cfg.content.context = {'B': ['facts.md'], 'P': ['facts.md'], 'S': ['facts.md']}
    shared = content_review._safe(gitops.show_file(str(tmp_path), head, 'page.html'))
    old = content_evidence.collect(str(tmp_path), base, head, 'page.html', cfg, max_chars=24000,
                                   shared_artifact=shared, deduplicate=False)
    new = content_evidence.collect(str(tmp_path), base, head, 'page.html', cfg, max_chars=24000,
                                   shared_artifact=shared)
    assert new.provenance == old.provenance
    assert new.available == old.available
    assert new.omissions == old.omissions
    assert new.source_observations == old.source_observations
    assert new.budgeted_characters == old.budgeted_characters == len(old.text)
    assert len(new.text) < len(old.text)
    assert 'the complete proposed source artifact above' in new.text
    assert 'retain this unit\'s distinct provenance' in new.text
    assert {tuple(record['codes']) for record in new.provenance if record['role'] == 'configured_context'} >= {('B',), ('P',), ('S',)}
    assert {record['role'] for record in new.provenance if record['path'] == 'layout.html'} == {'base_related_source', 'proposed_related_source'}

    def units(text):
        markers = list(re.finditer(r'\n--- repository evidence (.*?) ---\n', text))
        return [(json.loads(marker.group(1)), text[marker.end():markers[i + 1].start() if i + 1 < len(markers) else len(text)].rstrip('\n'))
                for i, marker in enumerate(markers)]

    previous = {}
    for (old_record, old_body), (record, body) in zip(units(old.text), units(new.text), strict=True):
        assert record == old_record
        if body.startswith('[Exact text is in the complete proposed source artifact above'):
            assert old_body in shared
        elif body.startswith('[Exact text is in the earlier evidence with provenance '):
            identity = body.removeprefix('[Exact text is in the earlier evidence with provenance ').split(' (identical text)', 1)[0]
            assert previous[identity] == old_body
        else:
            assert body == old_body
            identity = {k: record[k] for k in ('path', 'commit', 'role', 'start_line', 'end_line')}
            previous[json.dumps(identity, ensure_ascii=True)] = body


def test_distinct_base_and_proposed_evidence_is_never_aliased(tmp_path):
    base, head = fixture_repo(tmp_path)
    cfg = config.Config(install=None, suites=[], run_tests=False)
    bundle = content_evidence.collect(str(tmp_path), base, head, 'page.html', cfg, max_chars=24000)
    assert '<main>Old offer</main>' in bundle.text
    assert 'New offer with proof.' in bundle.text
    assert any(row['role'] == 'base_artifact' and row['commit'] == base for row in bundle.provenance)
    assert any(row['role'] == 'proposed_artifact' and row['commit'] == head for row in bundle.provenance)


def test_tight_evidence_budget_keeps_identical_omissions_and_admissions(tmp_path):
    base, head = fixture_repo(tmp_path)
    cfg = config.Config(install=None, suites=[], run_tests=False)
    cfg.content.context = {'B': ['facts.md'], 'P': ['facts.md'], 'S': ['facts.md']}
    shared = content_review._safe(gitops.show_file(str(tmp_path), head, 'page.html'))
    old = content_evidence.collect(str(tmp_path), base, head, 'page.html', cfg, max_chars=4000,
                                   shared_artifact=shared, deduplicate=False)
    new = content_evidence.collect(str(tmp_path), base, head, 'page.html', cfg, max_chars=4000,
                                   shared_artifact=shared)
    assert new.omissions and new.omissions == old.omissions
    assert new.provenance == old.provenance
    assert new.available == old.available
    assert new.budgeted_characters == len(old.text)


def test_compression_keeps_long_diff_chunk_boundaries(tmp_path, monkeypatch):
    base, _ = fixture_repo(tmp_path)
    (tmp_path / 'page.html').write_text('<main>\n' + ''.join(f'Changed public copy {n}.\n' for n in range(1100)) + '</main>\n')
    git(tmp_path, 'add', '.')
    git(tmp_path, 'commit', '-qm', 'large change')
    head = git(tmp_path, 'rev-parse', 'HEAD')
    cfg = config.Config(install=None, suites=[], run_tests=False, max_state_chars=24000)
    cfg.content.context = {'B': ['facts.md'], 'P': ['facts.md'], 'S': ['facts.md']}
    original = content_evidence.collect

    class Classifier:
        def __init__(self):
            self.states = []

        def ask(self, state, questions):
            self.states.append(state)
            return {key: .01 for key in questions}

    def run(deduplicate):
        def collect(*args, **kwargs):
            return original(*args, **kwargs, deduplicate=deduplicate)
        monkeypatch.setattr(content_evidence, 'collect', collect)
        client = Classifier()
        result = content_review.review(str(tmp_path), base, head, cfg,
                                       gitops.changed_files(str(tmp_path), base, head), client=client)
        return client.states, result

    before, baseline = run(False)
    after, compressed = run(True)
    assert len(before) > 1 and len(before) == len(after)
    assert any('retain this unit\'s distinct provenance' in state for state in after)
    assert sum(map(len, after)) < sum(map(len, before))
    def diff_prefix(state):
        return state.split('\n--- complete proposed source artifact', 1)[0].split(
            '\n--- automatically collected repository evidence', 1)[0]
    assert list(map(diff_prefix, before)) == list(map(diff_prefix, after))
    assert compressed.to_dict() == baseline.to_dict()
