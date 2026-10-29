"""Trusted publication routing and location-independent units, without providers."""
import subprocess
import pytest
from rewardguard import config, gitops, content_review


def git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


@pytest.fixture
def repo(tmp_path):
    git(tmp_path, 'init', '-qb', 'main')
    git(tmp_path, 'config', 'user.email', 'test@example.test')
    git(tmp_path, 'config', 'user.name', 'Test')
    (tmp_path / 'page.md').write_text('# Product\n\nFirst public paragraph.\n\nSecond paragraph.\n')
    git(tmp_path, 'add', '.')
    git(tmp_path, 'commit', '-qm', 'base')
    return tmp_path


def cfg(extra=''):
    return config.parse('''run_tests = false
[[content.publications]]
id = "site"
sources = ["*.md", "public/**", "src/**"]
type = "page"
route = "/{stem}"
''' + extra)


def test_empty_mappings_make_markdown_and_javascript_zero_call(repo):
    (repo / 'page.md').write_text('Public sounding words are not authorization.\n')
    git(repo, 'commit', '-qam', 'edit')
    class NoCalls:
        def ask(self, *_): pytest.fail('unmapped content called provider')
    result = content_review.review(str(repo), 'main~1', 'HEAD', config.Config(None, []),
                                  gitops.changed_files(str(repo), 'main~1', 'HEAD'), client=NoCalls())
    assert result.status == 'skipped'


def test_manifest_is_local_stable_and_preserves_source_anchors(repo):
    from rewardguard.content_publications import manifest
    before = manifest(str(repo), 'HEAD', 'HEAD', cfg())
    (repo / 'page.md').write_text('\n\n# Product\n\nFirst public paragraph.\n\nSecond paragraph.\n')
    git(repo, 'commit', '-qam', 'move')
    after = manifest(str(repo), 'HEAD~1', 'HEAD', cfg())
    old = next(a for a in before['artifacts'] if a['path'] == 'page.md')['units']
    new = next(a for a in after['artifacts'] if a['path'] == 'page.md')['units']
    assert [u['identity'] for u in old] == [u['identity'] for u in new]
    assert new[1]['line'] == old[1]['line'] + 2
    assert before['cache']['availability'] in {'disabled', 'configured'}


def test_oversized_changed_publication_is_required_incomplete_coverage(repo):
    from rewardguard import report
    from rewardguard.models import Report
    import argparse
    page = repo / 'page.md'
    page.write_text('Reader paragraph.\n' + ('x' * 160001))
    git(repo, 'commit', '-qam', 'grow public source beyond extraction limit')
    base = git(repo, 'rev-parse', 'HEAD~1')
    result = content_review.review(str(repo), base, 'HEAD', cfg(), gitops.changed_files(str(repo), base, 'HEAD'),
                                  client=object(), log=lambda _: None)
    assert result.status == 'not_evaluated'
    assert result.eligibility[0]['status'] == 'not_evaluated'
    assert result.coverage[0]['reason'] == 'Blob exceeds 160000 byte extraction limit'
    rep = Report(content=result.to_dict(), findings=result.findings, errors=result.errors)
    assert report.status(rep) == 'incomplete'
    from rewardguard import cli
    assert cli._finish(rep, argparse.Namespace(require_complete=True, json=None, markdown=None)) == 3


def test_fragment_rule_state_tracks_complete_literal_target_ids(repo):
    from rewardguard import content_publications, content_rules
    from rewardguard.content_evidence import EvidenceBundle
    page = repo / 'public/page.html'
    page.parent.mkdir()
    page.write_text('<a href="#install">Install</a><h2 id="install">Install</h2>\n')
    git(repo, 'add', '.'); git(repo, 'commit', '-qm', 'static html targets')
    base = git(repo, 'rev-parse', 'HEAD')
    rule = next(r for r in content_rules.all_rules() if r.id == 'CG_LINK_FRAGMENT')
    before = content_publications.manifest(str(repo), base, 'HEAD', cfg())
    artifact = next(a for a in before['artifacts'] if a['path'] == 'public/page.html')
    link = next(u for u in artifact['units'] if u['kind'] == 'link')
    old_state = content_review._rule_state(rule, link, artifact, before, EvidenceBundle(), '')
    assert artifact['target_ids'] == ['install'] and artifact['target_ids_complete'] is True
    page.write_text('<a href="#install">Install</a><h2 id="setup">Install</h2>\n')
    git(repo, 'commit', '-qam', 'rename target only')
    after = content_publications.manifest(str(repo), base, 'HEAD', cfg())
    updated = next(a for a in after['artifacts'] if a['path'] == 'public/page.html')
    link = next(u for u in updated['units'] if u['kind'] == 'link')
    new_state = content_review._rule_state(rule, link, updated, after, EvidenceBundle(), '')
    assert updated['affected'] and updated['target_ids'] == ['setup']
    assert old_state != new_state and 'fragment_targets_complete' in new_state


def test_h1_promise_rule_runs_on_heading_units(repo, monkeypatch):
    from rewardguard import content_rules
    page = repo / 'public/page.html'
    page.parent.mkdir()
    page.write_text('<h1>Free forever</h1><p>The service costs $10 monthly.</p>\n')
    git(repo, 'add', '.'); git(repo, 'commit', '-qm', 'add h1 and body')
    base = git(repo, 'rev-parse', 'HEAD~1')
    rule = next(r for r in content_rules.all_rules() if r.id == 'CG_META_PROMISE_CONFLICT')
    monkeypatch.setattr(content_rules, 'all_rules', lambda: [rule])
    class Client:
        def __init__(self): self.calls = []
        def ask(self, state, questions):
            self.calls.append((state, questions))
            return {key: .9 if key.startswith(('applies_', 'ready_')) else .01 for key in questions}
    client = Client()
    result = content_review.review(str(repo), base, 'HEAD', cfg(), gitops.changed_files(str(repo), base, 'HEAD'),
                                  client=client, log=lambda _: None)
    rows = [row for row in result.coverage if row.get('rule') == rule.id]
    assert rows and any(row.get('line') == 1 for row in rows), rows
    assert any('"kind": "heading"' in state and any('applies_' in key for key in questions)
               for state, questions in client.calls)


def test_explicit_mapping_never_overrides_required_denials_or_symlinks(repo):
    from rewardguard.content_publications import manifest
    for path in ('README.md', 'Docs/private.md', 'public/.env', 'public/Tests/a.md', 'src/a.test.ts'):
        p = repo / path; p.parent.mkdir(parents=True, exist_ok=True); p.write_text('Do not transmit this')
    (repo / 'public/link.md').symlink_to('../page.md')
    git(repo, 'add', '.'); git(repo, 'commit', '-qm', 'denied')
    c = cfg(); c.content.exclude = []; c.content.evidence_exclude = []
    m = manifest(str(repo), 'HEAD~1', 'HEAD', c)
    assert {a['path'] for a in m['artifacts']} == {'page.md'}
    assert any(x['path'] == 'public/link.md' for x in m['exclusions'])


def test_static_templates_exclude_implementation_and_dynamic_content(repo):
    from rewardguard.content_publications import manifest
    p = repo / 'src/page.tsx'; p.parent.mkdir()
    p.write_text('const secretImplementation = "internal words";\nexport default () => <main><h1>Hello reader</h1><p>{user.name}</p><img alt="Useful image" /></main>;\n')
    git(repo, 'add', '.'); git(repo, 'commit', '-qm', 'template')
    a = next(a for a in manifest(str(repo), 'HEAD~1', 'HEAD', cfg())['artifacts'] if a['path'] == 'src/page.tsx')
    assert 'Hello reader' in str(a['units']) and 'Useful image' in str(a['units'])
    assert 'internal words' not in str(a['units'])
    assert any(x['status'] == 'not_evaluated' for x in a['limitations'])


@pytest.mark.parametrize('fragment', ['id=""', 'type="email"', 'route="https://foreign.test"',
    'published="yes"', 'sources=["../secret.md"]', 'dependencies=["unknown"]'])
def test_invalid_mapping_is_rejected(fragment):
    lines = {'id': 'id="site"', 'type': 'type="page"', 'route': 'route="/page"',
             'sources': 'sources=["page.md"]'}
    lines[fragment.split('=')[0]] = fragment
    from rewardguard.models import RewardGuardError
    with pytest.raises(RewardGuardError):
        config.parse('run_tests=false\n[[content.publications]]\n' + '\n'.join(lines.values()))


def test_jsx_expression_strings_and_comments_are_not_reader_units(repo):
    from rewardguard.content_publications import manifest
    p = repo / 'src/page.tsx'; p.parent.mkdir()
    p.write_text('export default () => <main>{flag ? "<p>PRIVATE EXPRESSION</p>" : null}<p>Public paragraph.</p></main>;\n')
    git(repo, 'add', '.'); git(repo, 'commit', '-qm', 'dynamic expression')
    a = next(a for a in manifest(str(repo), 'HEAD~1', 'HEAD', cfg())['artifacts'] if a['path'] == 'src/page.tsx')
    assert 'PRIVATE EXPRESSION' not in str(a['units'])
    assert 'Public paragraph.' in str(a['units'])
    assert a['limitations']


def test_markdown_multiline_comments_never_become_copy(repo):
    from rewardguard.content_publications import manifest
    (repo / 'page.md').write_text('<!--\nPRIVATE COMMENT\n-->\n\nPublic paragraph.\n')
    git(repo, 'commit', '-qam', 'comments')
    a = manifest(str(repo), 'HEAD~1', 'HEAD', cfg())['artifacts'][0]
    assert 'PRIVATE COMMENT' not in str(a['units'])
    assert 'Public paragraph.' in str(a['units'])


@pytest.mark.parametrize("href", ["/target", "target"])
def test_removed_route_reconsiders_unchanged_nonfirst_link(repo, monkeypatch, href):
    from rewardguard import content_rules
    (repo / 'page.md').write_text(f'# Page\n\n[Read target]({href})\n')
    (repo / 'target.md').write_text('Target content.\n')
    git(repo, 'add', '.'); git(repo, 'commit', '-qm', 'routes')
    base = git(repo, 'rev-parse', 'HEAD')
    (repo / 'target.md').unlink(); git(repo, 'commit', '-qam', 'remove target')
    c = cfg(); c.content.packs = ['links']
    rule = next(r for r in content_rules.all_rules() if r.id == 'CG_LINK_FRAGMENT')
    monkeypatch.setattr(content_rules, 'all_rules', lambda: [rule])
    class Client:
        def __init__(self): self.calls = []
        def ask(self, state, questions):
            self.calls.append((state, questions))
            return {key: .9 if key.startswith(('applies_', 'literal_')) else .01 for key in questions}
    client = Client()
    result = content_review.review(str(repo), base, 'HEAD', c, gitops.changed_files(str(repo), base, 'HEAD'), client=client)
    assert any(row.get('rule') == rule.id and row['status'] == 'evaluated' for row in result.coverage)
    assert any('/target' in state for state, _ in client.calls)


def test_transitive_public_dependencies_only_expand_affected_pages(repo, monkeypatch):
    from rewardguard.content_publications import manifest
    from rewardguard import content_rules
    for name, text in {'layout.md': 'Shared layout copy.', 'tokens.md': 'Shared disclaimer.', 'other.md': 'Unrelated page.'}.items():
        (repo / name).write_text(text)
    git(repo, 'add', '.'); git(repo, 'commit', '-qm', 'shared')
    base = git(repo, 'rev-parse', 'HEAD')
    (repo / 'tokens.md').write_text('Revised shared disclaimer.')
    git(repo, 'commit', '-qam', 'revise dependency')
    c = config.Config(None, [], run_tests=False)
    c.content.publications = [config.Publication('page', ('page.md',), 'page', '/page', dependencies=('layout',)),
        config.Publication('layout', ('layout.md',), 'component', '/layout', dependencies=('tokens',)),
        config.Publication('tokens', ('tokens.md',), 'component', '/tokens'),
        config.Publication('other', ('other.md',), 'page', '/other')]
    m = manifest(str(repo), base, 'HEAD', c)
    assert {a['id'] for a in m['artifacts'] if a['affected']} == {'page', 'layout', 'tokens'}
    page = next(a for a in m['artifacts'] if a['id'] == 'page')
    from rewardguard.content_evidence import EvidenceBundle
    rule = next(r for r in content_rules.all_rules() if r.id == 'CG_SECTION_PROMISE_MISMATCH')
    state = content_review._rule_state(rule, page['units'][1], page, m, EvidenceBundle(), '')
    assert 'Revised shared disclaimer.' in state
    assert 'Unrelated page.' not in state


@pytest.mark.parametrize("policy", [None, "", "  \n"])
def test_unadopted_policy_rules_make_no_model_calls(repo, monkeypatch, policy):
    from rewardguard import content_rules
    if policy is not None:
        (repo / '.rewardguard').mkdir()
        (repo / '.rewardguard/content-policy.md').write_text(policy)
        git(repo, 'add', '.'); git(repo, 'commit', '-qm', 'empty policy baseline')
    (repo / 'page.md').write_text('New reader copy.\n')
    git(repo, 'commit', '-qam', 'edit')
    c = cfg('evidence=["P"]\n'); c.content.packs = ['style']
    rule = next(r for r in content_rules.all_rules() if r.id == 'CG_TRUSTED_STYLE_CONFLICT')
    monkeypatch.setattr(content_rules, 'all_rules', lambda: [rule])
    class Client:
        def ask(self, *_): pytest.fail('Unadopted optional policy called a model')
    result = content_review.review(str(repo), 'HEAD~1', 'HEAD', c,
        gitops.changed_files(str(repo), 'HEAD~1', 'HEAD'), client=Client())
    assert any(row['status'] == 'not_applicable' and 'adopted' in row['reason'] for row in result.coverage)
    assert all('probability' not in row for row in result.coverage)


def test_dynamic_gaps_remain_visible_alongside_evaluated_units(repo, monkeypatch):
    from rewardguard import content_rules, content_checks
    p = repo / 'src/page.tsx'; p.parent.mkdir()
    p.write_text('export default () => <main><p>Visible copy.</p>{user.text}</main>;\n')
    git(repo, 'add', '.'); git(repo, 'commit', '-qm', 'partial template')
    c = cfg(); c.content.packs = ['writing']
    rule = next(r for r in content_rules.all_rules() if r.id == 'CG_AMBIGUOUS_MEANING')
    monkeypatch.setattr(content_rules, 'all_rules', lambda: [rule])
    class Client:
        def ask(self, state, questions):
            return {k: .9 if k.startswith('applies_') else .01 for k in questions}
    result = content_review.review(str(repo), 'HEAD~1', 'HEAD', c,
        gitops.changed_files(str(repo), 'HEAD~1', 'HEAD'), client=Client())
    assert result.status == 'reviewed'
    assert {'evaluated', 'not_evaluated'} <= {row['status'] for row in result.coverage}
    checks = content_checks.build_checks({'content': result.to_dict(), 'findings': [], 'notes': result.notes})
    assert 'Eligibility is deterministic' in checks[0]['output']['summary']
    assert 'classification p=' not in checks[0]['output']['summary']


def test_static_template_implementation_edit_never_regrades_copy(repo):
    from rewardguard.content_publications import manifest
    p = repo / 'src/page.svelte'; p.parent.mkdir()
    p.write_text('<script>let count = 1;</script>\n<h1>Public headline</h1>\n<p>Public copy.</p>\n')
    git(repo, 'add', '.'); git(repo, 'commit', '-qm', 'template')
    base = git(repo, 'rev-parse', 'HEAD')
    p.write_text('<script>let count = 2; console.log("implementation only");</script>\n<h1>Public headline</h1>\n<p>Public copy.</p>\n')
    git(repo, 'commit', '-qam', 'implementation')
    c = cfg()
    plan = manifest(str(repo), base, 'HEAD', c)
    a = next(a for a in plan['artifacts'] if a['path'] == 'src/page.svelte')
    assert a['cache_only'] and not a['semantic_changed']
    class Client:
        def ask(self, *_): pytest.fail('Unchanged reader copy called provider')
    result = content_review.review(str(repo), base, 'HEAD', c,
        gitops.changed_files(str(repo), base, 'HEAD'), client=Client())
    assert result.status == 'skipped'
    assert all(row['status'] in {'unchanged', 'not_applicable'} for row in result.coverage)
    assert not result.findings


def test_html_inline_markup_preserves_one_reader_paragraph_with_exact_anchors(repo):
    from rewardguard.content_publications import extract
    publication = config.Publication('page', ('page.html',), 'page', '/')
    source = '<p>Hello <strong>reader</strong> &amp; friend.</p>\n'
    units, limits = extract('page.html', source, publication)
    paragraphs = [u for u in units if u['kind'] == 'copy']
    assert len(paragraphs) == 1
    assert paragraphs[0]['text'] == 'Hello reader & friend.'
    assert all(anchor in source for anchor in paragraphs[0]['anchors'].values())
    assert set(paragraphs[0]['line_map'].values()) == {1}


def test_ambiguous_json_field_location_is_not_invented(repo):
    from rewardguard.content_publications import extract
    publication = config.Publication('copy', ('copy.json',), 'page', '/', fields=('public',))
    source = '{\n  "internal": "Same copy",\n  "public": "Same copy"\n}'
    units, limits = extract('copy.json', source, publication)
    assert not units
    assert any('anchor' in limit['reason'] for limit in limits)


def test_selected_json_fields_do_not_establish_complete_record(repo, monkeypatch):
    from rewardguard import content_rules
    (repo / 'public').mkdir()
    p = repo / 'public/media.json'
    p.write_text('{"title":"Old title", "dimensions":"1920x1080"}')
    (repo / '.rewardguard').mkdir()
    (repo / '.rewardguard/profile.md').write_text('The media profile requires dimensions 1920x1080.')
    git(repo, 'add', '.'); git(repo, 'commit', '-qm', 'media baseline')
    base = git(repo, 'rev-parse', 'HEAD')
    p.write_text('{"title":"New title", "dimensions":"1920x1080"}')
    git(repo, 'commit', '-qam', 'title only')
    c = config.Config(None, [], run_tests=False)
    c.content.publications = [config.Publication('media', ('public/media.json',), 'page', '/media', evidence=('P',), fields=('title',))]
    c.content.include = ['public/*.json']
    c.content.context = {'P': ['.rewardguard/profile.md']}
    rule = next(r for r in content_rules.all_rules() if r.id == 'CG_MEDIA_DELIVERY_PROFILE')
    # This probe exercises the evidence contract independently of deterministic kind filtering.
    from dataclasses import replace
    rule = replace(rule, pack='writing')
    monkeypatch.setattr(content_rules, 'all_rules', lambda: [rule])
    class Client:
        def __init__(self): self.calls = []
        def ask(self, state, questions):
            self.calls.append(questions)
            assert not any(key.startswith(rule.id) for key in questions), 'Partial fields were graded as a complete record'
            return {key: .9 for key in questions}
    result = content_review.review(str(repo), base, 'HEAD', c,
        gitops.changed_files(str(repo), base, 'HEAD'), client=Client())
    assert any(row['status'] == 'not_evaluated' and row.get('rule') == rule.id for row in result.coverage)
    assert not result.findings


def test_complete_literal_schema_record_can_prove_adopted_required_property_omission(repo, monkeypatch):
    from rewardguard import content_rules
    (repo / 'public').mkdir()
    page = repo / 'public/article.html'
    page.write_text('<script type="application/ld+json">{"@type": "Article", "headline": "Existing headline"}</script>\n')
    (repo / '.rewardguard').mkdir()
    (repo / '.rewardguard/schema-policy.md').write_text('Adopted Article schema profile requires a headline property on this article.')
    git(repo, 'add', '.'); git(repo, 'commit', '-qm', 'schema baseline')
    base = git(repo, 'rev-parse', 'HEAD')
    page.write_text('<script type="application/ld+json">{"@type": "Article"}</script>\n')
    git(repo, 'commit', '-qam', 'remove required property')
    c = config.Config(None, [], run_tests=False)
    c.content.publications = [config.Publication('article', ('public/article.html',), 'article', '/article', evidence=('P',))]
    c.content.context = {'P': ['.rewardguard/schema-policy.md']}
    rule = next(r for r in content_rules.all_rules() if r.id == 'CG_SCHEMA_PROFILE')
    monkeypatch.setattr(content_rules, 'all_rules', lambda: [rule])
    class Client:
        def __init__(self): self.graded = []
        def ask(self, state, questions):
            self.graded.extend(key for key in questions if key.startswith(rule.id))
            return {key: .9 if key.startswith(('applies_', 'literal_', 'ready_'))
                    else .8 if key == rule.id + '__required_property' else .01 for key in questions}
    class Explain:
        def explain_content(self, state, rule, statement, rubric, *, anchors):
            assert anchors[1] == '{"@type": "Article"}'
            return [{'line': 1, 'code': '"@type": "Article"', 'problem': 'Required headline is absent.', 'fix': 'Restore headline.'}]
    client = Client()
    result = content_review.review(str(repo), base, 'HEAD', c,
        gitops.changed_files(str(repo), base, 'HEAD'), client=client, haiku=Explain())
    assert result.status == 'reviewed'
    assert rule.id + '__required_property' in client.graded
    assert len(result.findings) == 1 and result.findings[0].severity == 'fail'
    assert result.findings[0].line == 1
    assert all(row['source_only'] for row in result.coverage if row['status'] == 'evaluated')


@pytest.mark.parametrize('prefix,suffix', [
    ('const example = "return <p>PRIVATE BEFORE</p>";\n', ''),
    ('// return <p>PRIVATE COMMENT</p>\n', ''),
    ('/* return <p>PRIVATE BLOCK COMMENT</p> */\n', ''),
    ('', '\nconst internal = "<p>PRIVATE AFTER</p>";'),
])
def test_jsx_expression_boundary_excludes_implementation_strings_and_comments(prefix, suffix):
    from rewardguard.content_publications import extract
    publication = config.Publication('page', ('src/**',), 'page', '/')
    source = prefix + 'export default () => <p>PUBLIC PARAGRAPH</p>;' + suffix
    units, limits = extract('src/page.tsx', source, publication)
    assert [u['text'] for u in units] == ['PUBLIC PARAGRAPH']
    assert units[0]['line'] == prefix.count('\n') + 1


@pytest.mark.parametrize('implementation', [
    'export const internal = `\nPRIVATE IMPLEMENTATION STRING\n`;\n',
    '{\n(() => {\nconst internal = "PRIVATE EXPRESSION BODY";\nreturn internal;\n})()\n}\n',
])
def test_mdx_unsupported_regions_are_omitted_whole(implementation):
    from rewardguard.content_publications import extract
    publication = config.Publication('page', ('src/**',), 'article', '/')
    source = implementation + '\n# Public headline\n\nPUBLIC PARAGRAPH\n'
    units, limits = extract('src/page.mdx', source, publication)
    assert [u['text'] for u in units] == ['# Public headline', 'PUBLIC PARAGRAPH']
    assert units[-1]['line'] == source.splitlines().index('PUBLIC PARAGRAPH') + 1
    assert limits and all(limit['status'] == 'not_evaluated' for limit in limits)


@pytest.mark.parametrize('implementation', [
    'export const internal =\n\n`PRIVATE IMPLEMENTATION STRING`;\n',
    'export const internal = "PRIVATE PREFIX" +\n\n`PRIVATE CONTINUATION`;\n',
    'export const first = "PRIVATE FIRST",\n\nsecond = "PRIVATE SECOND";\n',
])
def test_mdx_incomplete_esm_blank_lines_do_not_resume_reader_extraction(implementation):
    from rewardguard.content_publications import extract
    source = implementation + '\n# Public headline\n\nPUBLIC PARAGRAPH\n'
    publication = config.Publication('page', ('src/**',), 'article', '/')
    units, limits = extract('src/page.mdx', source, publication)
    assert [u['text'] for u in units] == ['# Public headline', 'PUBLIC PARAGRAPH']
    assert units[-1]['line'] == source.splitlines().index('PUBLIC PARAGRAPH') + 1
    assert limits and all(row['status'] == 'not_evaluated' for row in limits)


def test_mdx_complete_esm_boundary_skips_nested_semicolons_and_keeps_markdown():
    from rewardguard.content_publications import extract
    source = ('export const internal = (() => {\n'
              'const value = "PRIVATE; STRING";\n\nreturn value;\n})();\n\n'
              '# Public headline\n\nPUBLIC PARAGRAPH\n')
    units, limits = extract('page.mdx', source,
                            config.Publication('page', ('page.mdx',), 'article', '/'))
    assert [u['text'] for u in units] == ['# Public headline', 'PUBLIC PARAGRAPH']
    assert units[-1]['line'] == source.splitlines().index('PUBLIC PARAGRAPH') + 1
    assert limits and all(row['status'] == 'not_evaluated' for row in limits)


def test_mdx_without_established_esm_boundary_omits_remaining_region():
    from rewardguard.content_publications import extract
    source = 'export const internal =\n\n`PRIVATE IMPLEMENTATION STRING`\n\n# Possible Markdown\n'
    units, limits = extract('page.mdx', source,
                            config.Publication('page', ('page.mdx',), 'article', '/'))
    assert not units
    assert limits and all(row['status'] == 'not_evaluated' for row in limits)


@pytest.mark.parametrize('tail', [
    ' export const internal = `\nPRIVATE IMPLEMENTATION STRING\n`;',
    '\nconst internal = `\nPRIVATE IMPLEMENTATION STRING\n`;',
])
def test_mdx_unexamined_esm_tail_cannot_resume_markdown(tail):
    from rewardguard.content_publications import extract
    source = 'export const first = 1;' + tail + '\n\n# Public headline\n'
    units, limits = extract('page.mdx', source,
                            config.Publication('page', ('page.mdx',), 'article', '/'))
    # Chained statements are unsupported: retain no reader text from an
    # unexamined tail, even if it appears to contain a later Markdown heading.
    assert not units
    assert limits and all(row['status'] == 'not_evaluated' for row in limits)


def test_mdx_safe_esm_whitespace_tail_preserves_subsequent_markdown():
    from rewardguard.content_publications import extract
    source = 'export const internal = "PRIVATE"; \t\n \t\n# Public headline\n\nPublic paragraph.\n'
    units, limits = extract('page.mdx', source,
                            config.Publication('page', ('page.mdx',), 'article', '/'))
    assert [u['text'] for u in units] == ['# Public headline', 'Public paragraph.']
    assert [u['line'] for u in units] == [3, 5]
    assert limits and all(row['status'] == 'not_evaluated' for row in limits)


@pytest.mark.parametrize('source', [
    'export default () => <p>Public</p> + "<p>PRIVATE CONCATENATED</p>";',
    'const pattern = /return <p>PRIVATE REGEX/; export default () => <p>Public</p>;',
    'function helper(){return <p>Private helper</p>;} export default () => <p>Public</p>;',
])
def test_ambiguous_jsx_regions_fail_closed(source):
    from rewardguard.content_publications import extract
    units, limits = extract('page.tsx', source, config.Publication('page', ('page.tsx',), 'page', '/'))
    assert not units
    assert limits and all(row['status'] == 'not_evaluated' for row in limits)


def test_parenthesized_jsx_keeps_only_bounded_expression_and_exact_lines():
    from rewardguard.content_publications import extract
    source = 'export default function Page() {\nreturn (\n<section><p>Public text.</p></section>\n);\n}\nconst x="<p>PRIVATE TRAILING</p>";'
    units, _ = extract('page.tsx', source, config.Publication('page', ('page.tsx',), 'page', '/'))
    assert [u['text'] for u in units] == ['Public text.']
    assert units[0]['line'] == 3


def test_changed_routes_surface_unresolvable_unchanged_link_scope(repo):
    from rewardguard.content_publications import manifest
    (repo / 'page.md').write_text('[Unresolved destination](http://[)\n')
    (repo / 'target.md').write_text('Published target.\n')
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'published routes')
    before = git(repo, 'rev-parse', 'HEAD')
    git(repo, 'rm', 'target.md')
    git(repo, 'commit', '-qm', 'delete public route')
    plan = manifest(str(repo), before, 'HEAD', cfg())
    page = next(a for a in plan['artifacts'] if a['path'] == 'page.md')
    assert page['affected'] and page['cache_only']
    assert page['limitations'] == [{'line':1, 'status':'not_evaluated',
        'reason':'Invalid literal URL; public route dependency could not be resolved'}]
    class NoCalls:
        def ask(self, *a): pytest.fail('unchanged unresolved link must not trigger paid regrading')
    result = content_review.review(str(repo), before, 'HEAD', cfg(),
                                  gitops.changed_files(str(repo), before, 'HEAD'), client=NoCalls())
    assert any(row.get('file') == 'page.md' and row.get('status') == 'not_evaluated'
               and row.get('reason') == page['limitations'][0]['reason'] for row in result.coverage)


def test_html_link_roles_change_identity_and_review_state(repo):
    from rewardguard.content_publications import extract
    from rewardguard.content_review import _semantic
    p = cfg().content.publications[0]
    units = [extract('public/page.html', html, p)[0][0] for html in (
        '<link rel="canonical" href="/one">', '<link rel="alternate" href="/one">', '<a href="/one"></a>')]
    assert len({u['identity'] for u in units}) == 3
    states = [_semantic(u) for u in units]
    assert len({str(s) for s in states}) == 3
    assert 'canonical' in str(states[0]) and 'alternate' in str(states[1])


def test_empty_canonical_is_kept_and_routed_to_review(repo):
    from rewardguard import content_publications
    (repo / 'public').mkdir()
    (repo / 'public/page.html').write_text('<link rel="canonical" href="">\n')
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'empty canonical')
    base, head = git(repo, 'rev-parse', 'HEAD~1'), git(repo, 'rev-parse', 'HEAD')
    c = cfg()
    c.content.packs = ['canonicals']
    plan = content_publications.manifest(str(repo), base, head, c, gitops.changed_files(str(repo), base, head))
    artifact = next(a for a in plan['artifacts'] if a['path'] == 'public/page.html')
    canonical = next(u for u in artifact['units'] if u['field'].startswith('link[rel=canonical]'))
    assert canonical['text'] == '' and canonical['line'] == 1
    calls = []
    class Client:
        def ask(self, state, questions):
            calls.append(state)
            return {key: .9 if key.startswith(('applies_', 'literal_')) else .1 for key in questions}
    result = content_review.review(str(repo), base, head, c, gitops.changed_files(str(repo), base, head), client=Client())
    assert calls and any(row.get('rule') == 'CG_CANONICAL_OUTPUT_INVALID' for row in result.coverage)


def test_canonical_conflict_state_tracks_sibling_declaration_relationship(repo):
    from rewardguard import content_publications, content_rules
    from rewardguard.content_evidence import EvidenceBundle
    base_html = '<link rel="canonical" href="/one">\n'
    (repo / 'public').mkdir()
    (repo / 'public/page.html').write_text(base_html)
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'one canonical')
    base = git(repo, 'rev-parse', 'HEAD')
    (repo / 'public/page.html').write_text(base_html + '<link rel="canonical" href="/two">\n')
    git(repo, 'commit', '-qam', 'conflicting canonical')
    c = cfg()
    conflict_plan = content_publications.manifest(str(repo), base, 'HEAD', c)
    conflict_artifact = next(a for a in conflict_plan['artifacts'] if a['path'] == 'public/page.html')
    rule = next(r for r in content_rules.all_rules() if r.id == 'CG_CANONICAL_CONFLICT')
    primary = next(u for u in conflict_artifact['units'] if u['text'] == '/one')
    conflict_state = content_review._rule_state(rule, primary, conflict_artifact, conflict_plan, EvidenceBundle(), '')
    (repo / 'public/page.html').write_text(base_html + '<a href="/two">other link</a>\n')
    git(repo, 'commit', '-qam', 'unrelated link')
    link_plan = content_publications.manifest(str(repo), base, 'HEAD', c)
    link_artifact = next(a for a in link_plan['artifacts'] if a['path'] == 'public/page.html')
    primary = next(u for u in link_artifact['units'] if u['text'] == '/one')
    link_state = content_review._rule_state(rule, primary, link_artifact, link_plan, EvidenceBundle(), '')
    assert conflict_state != link_state
    assert 'canonical_declarations' in conflict_state


@pytest.mark.parametrize('example', ['```yaml\ndraft: true\n```', '~~~yaml\npublished: false\n~~~', '> draft: true', 'draft: true'])
def test_body_draft_examples_do_not_exclude_public_markdown(repo, example):
    from rewardguard.content_publications import manifest
    (repo / 'page.md').write_text('---\ndraft: false\n---\n# Published guide\n\nReader paragraph.\n\n' + example + '\n')
    git(repo, 'commit', '-qam', 'document draft metadata')
    m = manifest(str(repo), 'HEAD~1', 'HEAD', cfg())
    assert [a['path'] for a in m['artifacts']] == ['page.md']
    assert 'Reader paragraph.' in str(m['artifacts'][0]['units'])


@pytest.mark.parametrize('metadata', ['draft: true', 'published: false'])
def test_actual_frontmatter_draft_still_excluded(repo, metadata):
    from rewardguard.content_publications import manifest
    (repo / 'page.md').write_text('---\n' + metadata + '\n---\nUnpublished reader paragraph.\n')
    git(repo, 'commit', '-qam', 'draft')
    m = manifest(str(repo), 'HEAD~1', 'HEAD', cfg())
    assert m['artifacts'] == []
    assert any(x['reason'] == 'Draft metadata requires explicit opt-in' for x in m['exclusions'])


def test_unbounded_mdx_omission_cannot_establish_complete_document_or_pass_ci(repo, monkeypatch, tmp_path):
    import argparse, json
    from rewardguard import cli, content_rules, report
    from rewardguard.models import Report
    (repo/'page.mdx').write_text('# Published\n\nVisible public claim.\n\nexport const unknown = {\nPRIVATE TAIL\n')
    git(repo,'add','.'); git(repo,'commit','-qm','partial MDX')
    c = cfg(); c.content.publications = [config.Publication('page',('page.mdx',),'page','/')]
    c.content.packs = ['writing']
    selected = [r for r in content_rules.all_rules() if r.id in {'CG_AMBIGUOUS_MEANING','CG_SECTION_PROMISE_MISMATCH'}]
    monkeypatch.setattr(content_rules,'all_rules',lambda:selected)
    calls=[]
    class Client:
        def ask(self,state,questions):
            assert 'PRIVATE TAIL' not in state
            calls.append((state,questions))
            return {k:.9 if k.startswith('applies_') else .1 for k in questions}
    result = content_review.review(str(repo),'HEAD~1','HEAD',c,gitops.changed_files(str(repo),'HEAD~1','HEAD'),client=Client())
    omissions = [r for r in result.coverage if r.get('omitted_to_end')]
    assert len(omissions) == 1 and omissions[0]['status'] == 'not_evaluated'
    assert omissions[0]['line'] == 5 and omissions[0]['end_line'] == 6
    assert any(r['status']=='evaluated' for r in result.coverage)
    complete = [r for r in result.coverage if r.get('rule')=='CG_SECTION_PROMISE_MISMATCH']
    assert complete and all(r['status']=='not_evaluated' and 'C' not in r['available'] for r in complete)
    for state, questions in calls:
        assert 'CG_SECTION_PROMISE_MISMATCH' not in questions
        if 'applies_CG_SECTION_PROMISE_MISMATCH' in questions:
            assert json.loads(state.split('\n',1)[1])['contract_C_available'] is False
    rep=Report(content=result.to_dict(),findings=result.findings,errors=result.errors)
    assert report.status(rep)=='incomplete'
    assert cli._finish(rep,argparse.Namespace(require_complete=True,json=str(tmp_path/'partial.json'),markdown=None))==3


def test_deep_valid_publication_dependencies_do_not_hit_python_recursion_limit(repo):
    from rewardguard.content_publications import manifest
    count=1100
    c=cfg()
    c.content.publications=[config.Publication(f'node{i}',('page.md',) if i==0 else (f'absent{i}.md',),
        'page',f'/{i}',dependencies=(f'node{i+1}',) if i+1<count else ()) for i in range(count)]
    artifact=manifest(str(repo),'HEAD','HEAD',c)['artifacts'][0]
    expected=sorted(f'node{i}' for i in range(1,count))
    assert artifact['resolved_dependencies']==expected
    assert artifact['missing_dependencies']==expected
