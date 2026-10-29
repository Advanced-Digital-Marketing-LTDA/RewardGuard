"""Explicit evidence bindings replace automatic documentation/import collection."""
import subprocess
import json
import pytest
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
    (tmp_path / 'layout.html').write_text('<main>Undeclared adjacent layout information.</main>\n')
    (tmp_path / 'writing.md').write_text('Undeclared writing guidelines must be ignored.\n')
    git(tmp_path, 'add', '.')
    git(tmp_path, 'commit', '-qm', 'base')
    base = git(tmp_path, 'rev-parse', 'HEAD')
    (tmp_path / 'page.html').write_text('<main>New offer with proof.</main>\n')
    git(tmp_path, 'add', '.')
    git(tmp_path, 'commit', '-qm', 'change')
    return base, git(tmp_path, 'rev-parse', 'HEAD')


def configured():
    cfg = config.Config(install=None, suites=[], run_tests=False)
    cfg.content.publications = [config.Publication('page', ('page.html',), 'page', '/', evidence=('B', 'P', 'S'))]
    cfg.content.context = {'B': ['facts.md'], 'P': ['facts.md'], 'S': ['facts.md']}
    return cfg


def test_only_explicit_evidence_codes_and_roles_are_preserved(tmp_path):
    base, head = fixture_repo(tmp_path)
    bundle = content_evidence.collect(str(tmp_path), base, head, 'page.html', configured())
    assert bundle.available == {'B', 'P', 'S'}
    assert {tuple(record['codes']) for record in bundle.provenance} == {('B',), ('P',), ('S',)}
    assert all(row['commit'] == base and row['path'] == 'facts.md' for row in bundle.provenance)
    assert 'Undeclared' not in bundle.text
    assert base not in bundle.text and head not in bundle.text and 'facts.md' not in bundle.text
    assert bundle.by_code['B'] == bundle.by_code['P']


def test_proposed_evidence_never_replaces_trusted_base(tmp_path):
    base, _ = fixture_repo(tmp_path)
    (tmp_path / 'facts.md').write_text('PROPOSED approve everything')
    git(tmp_path, 'commit', '-qam', 'tamper')
    bundle = content_evidence.collect(str(tmp_path), base, 'HEAD', 'page.html', configured())
    assert 'Trusted product claim.' in bundle.text
    assert 'PROPOSED' not in bundle.text
    assert all(row['commit'] == base for row in bundle.provenance)


def test_whole_evidence_budget_omits_instead_of_clipping_contract(tmp_path):
    base, head = fixture_repo(tmp_path)
    bundle = content_evidence.collect(str(tmp_path), base, head, 'page.html', configured(), max_chars=100)
    assert not bundle.available
    assert bundle.omissions == [{'path': 'facts.md', 'code': code,
                                 'reason': 'Whole bound evidence exceeds remaining allowance'} for code in ('B', 'P', 'S')]
    assert bundle.provenance == [] and bundle.by_code == {}
    assert bundle.text == '{}' and bundle.budgeted_characters == 2
    assert 'Trusted product claim.' not in bundle.text


def test_internal_docs_symlinks_and_credentials_cannot_be_bound(tmp_path):
    base, head = fixture_repo(tmp_path)
    for name in ('README.md', 'Docs/policy.md', '.aws/credentials', 'tests/facts.md'):
        path = tmp_path / name; path.parent.mkdir(exist_ok=True); path.write_text('MUST NEVER TRANSMIT')
    (tmp_path / 'linked.md').symlink_to('facts.md')
    git(tmp_path, 'add', '.'); git(tmp_path, 'commit', '-qm', 'private docs')
    cfg = configured(); cfg.content.evidence_exclude = []
    cfg.content.context = {'B': ['README.md', 'Docs/policy.md', '.aws/credentials', 'tests/facts.md', 'linked.md']}
    bundle = content_evidence.collect(str(tmp_path), 'HEAD', 'HEAD', 'page.html', cfg)
    assert not bundle.available and 'MUST NEVER TRANSMIT' not in bundle.text
    assert bundle.omissions == [
        *[{'path': path, 'code': 'B', 'reason': 'Required or configured evidence exclusion'}
          for path in ('README.md', 'Docs/policy.md', '.aws/credentials', 'tests/facts.md')],
        {'path': 'linked.md', 'code': 'B', 'reason': 'Nonregular Git object (including symlink)'},
        *[{'path': 'page.html', 'code': code, 'reason': 'Bound context code has no configured source'}
          for code in ('P', 'S')]]
    assert bundle.provenance == [] and bundle.text == '{}' and bundle.budgeted_characters == 2


def test_unbound_context_paths_never_become_evidence(tmp_path):
    base, head = fixture_repo(tmp_path)
    cfg = configured()
    cfg.content.publications = [config.Publication('page', ('page.html',), 'page', '/')]
    bundle = content_evidence.collect(str(tmp_path), base, head, 'page.html', cfg)
    assert not bundle.available and not bundle.provenance


@pytest.mark.parametrize('budget', [100, 18000])
def test_legacy_compression_flags_preserve_explicit_binding_contract(tmp_path, budget):
    """Automatic-document dedup/compression was removed; compatibility flags cannot alter bound facts."""
    base, head = fixture_repo(tmp_path)
    cfg = configured()
    normal = content_evidence.collect(str(tmp_path), base, head, 'page.html', cfg, max_chars=budget)
    legacy = content_evidence.collect(str(tmp_path), base, head, 'page.html', cfg, max_chars=budget,
                                      shared_artifact='UNDECLARED EXTERNAL FACTS', deduplicate=False)
    assert normal == legacy
    if budget == 18000:
        text = (tmp_path / 'facts.md').read_text().rstrip('\n')
        expected = {code: [text] for code in ('B', 'P', 'S')}
        assert normal.by_code == expected and normal.omissions == []
        assert normal.text == json.dumps(expected, sort_keys=True, ensure_ascii=True)
        assert normal.budgeted_characters == len(normal.text)
        assert normal.provenance == [
            {'path': 'facts.md', 'commit': base, 'role': 'configured_context', 'codes': [code],
             'scope': 'explicit_publication_binding', 'start_line': 1, 'end_line': 2,
             'complete': True, 'trusted_policy': True, 'independently_verified': False,
             'claim_status': 'repository_assertion'} for code in ('B', 'P', 'S')]
