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

    else:
        assert normal.by_code == {} and normal.available == set() and normal.provenance == []
        assert normal.text == '{}' and normal.budgeted_characters == 2
        assert normal.omissions == [{'path':'facts.md','code':code,
            'reason':'Whole bound evidence exceeds remaining allowance'} for code in ('B','P','S')]


@pytest.mark.parametrize('budget,admitted', [(20,1),(100,3)])
def test_multiple_bound_units_keep_exact_base_provenance_and_budget_omissions(tmp_path,budget,admitted):
    fixture_repo(tmp_path)
    texts=['Fact one exact.','Fact two exact.','Fact three exact.']
    paths=['fact1.md','fact2.md','fact3.md']
    for path,text in zip(paths,texts): (tmp_path/path).write_text(text+'\n')
    git(tmp_path,'add','.');git(tmp_path,'commit','-qm','trusted facts');base=git(tmp_path,'rev-parse','HEAD')
    (tmp_path/'fact2.md').write_text('PROPOSED TAMPERING\n')
    git(tmp_path,'commit','-qam','proposed facts');head=git(tmp_path,'rev-parse','HEAD')
    cfg=configured();cfg.content.publications=[config.Publication('page',('page.html',),'page','/',evidence=('B',))]
    cfg.content.context={'B':paths}
    bundle=content_evidence.collect(str(tmp_path),base,head,'page.html',cfg,max_chars=budget)
    expected={'B':texts[:admitted]}
    assert bundle.by_code==expected and bundle.text==json.dumps(expected,sort_keys=True,ensure_ascii=True)
    assert bundle.budgeted_characters==len(bundle.text)
    assert bundle.provenance==[{'path':path,'commit':base,'role':'configured_context','codes':['B'],
        'scope':'explicit_publication_binding','start_line':1,'end_line':1,'complete':True,
        'trusted_policy':True,'independently_verified':False,'claim_status':'repository_assertion'} for path in paths[:admitted]]
    assert bundle.omissions==[{'path':path,'code':'B','reason':'Whole bound evidence exceeds remaining allowance'} for path in paths[admitted:]]
    assert 'PROPOSED' not in bundle.text


def test_long_publication_preserves_every_whole_unit_and_bound_evidence(tmp_path,monkeypatch):
    from rewardguard import content_rules
    base,_=fixture_repo(tmp_path)
    paragraphs=[f'Public offer {n}: '+('Complete reader sentence. '*25).strip() for n in range(40)]
    (tmp_path/'page.html').write_text('\n'.join('<p>'+p+'</p>' for p in paragraphs)+'\n')
    git(tmp_path,'commit','-qam','many whole reader units');head=git(tmp_path,'rev-parse','HEAD')
    cfg=configured();cfg.content.packs=['proof'];cfg.max_state_chars=12000
    rule=next(r for r in content_rules.all_rules() if r.id=='CG_PRODUCT_FACT_CONFLICT')
    monkeypatch.setattr(content_rules,'all_rules',lambda:[rule])
    states=[]
    class Client:
        def ask(self,state,questions):
            data=json.loads(state.split('\n',1)[1])
            states.append(data)
            return {k:.9 if k.startswith(('applies_','ready_')) else .1 for k in questions}
    result=content_review.review(str(tmp_path),base,head,cfg,gitops.changed_files(str(tmp_path),base,head),client=Client())
    assert result.errors==[] and result.findings==[]
    assert len([r for r in result.coverage if r['status']=='evaluated'])==40
    assert {s['unit']['text'] for s in states}==set(paragraphs)
    assert all(s['trusted_bound_evidence']['B']==[(tmp_path/'facts.md').read_text().rstrip('\n')] for s in states)
    assert all('content_task' not in s for s in states)
    assert len(states)==80  # One applicability and one grading request per complete unit.
