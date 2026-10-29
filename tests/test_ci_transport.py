import hashlib
import io
import json
import zipfile
import pytest
from rewardguard.models import RewardGuardError


def test_artifact_digest_and_schema_are_verified():
    from rewardguard.run_artifacts import decode_archive
    payload = {'schema_version': 1, 'base': 'a'*40, 'head': 'b'*40, 'policy': 'c'*40,
               'repository': 'o/r', 'run_id': '123', 'run_attempt': '1', 'event': 'pull_request',
               'event_sha': 'd'*40, 'findings': [], 'errors': []}
    blob = io.BytesIO()
    with zipfile.ZipFile(blob, 'w') as archive:
        archive.writestr('rewardguard-run.json', json.dumps(payload))
    raw = blob.getvalue()
    digest = 'sha256:' + hashlib.sha256(raw).hexdigest()
    assert decode_archive(raw, digest, {k: v for k,v in payload.items() if k not in {'findings', 'errors'}}) == payload
    with pytest.raises(RewardGuardError, match='digest'):
        decode_archive(raw, 'sha256:' + '0'*64, {})
    with pytest.raises(RewardGuardError, match='head'):
        decode_archive(raw, digest, {'head': 'e'*40})


@pytest.mark.parametrize('change', [
    {'rule': 'SECRET_ADDED'}, {'severity': 'success'}, {'source': 'judge'}, {'line': True},
    {'probability': float('nan')}, {'message': {}}, {'details': []},
])
def test_run_finding_schema_rejects_branch_inventions(change):
    from rewardguard.run_artifacts import validate_results
    f = {'rule': 'NEW_FAILURES', 'severity': 'fail', 'source': 'run', 'message': 'known test failed'}
    f.update(change)
    with pytest.raises(RewardGuardError):
        validate_results({'base': 'a'*40, 'head': 'b'*40, 'findings': [f], 'errors': []}, {'base': 'a'*40, 'head': 'b'*40})


def test_publication_rejects_wrong_report_head_before_network():
    from rewardguard.publisher import publish
    class Client:
        def get(self, *a):
            raise AssertionError('network must not run')
    with pytest.raises(RewardGuardError, match='head'):
        publish(Client(), {'run_identity': {'head': 'a'*40}}, 'b'*40)


def test_publication_stale_head_makes_no_writes():
    from rewardguard.publisher import publish
    class Client:
        def get(self, suffix):
            assert suffix == 'pulls/1'
            return {'head': {'sha': 'b'*40}}
    assert publish(Client(), {'run_identity': {'head': 'a'*40}}, 'a'*40, pr=1) == 'stale'


def _archive(payload, name='rewardguard-run.json', duplicate=False):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w') as z:
        z.writestr(name, payload)
        if duplicate:
            z.writestr('other.json', payload)
    raw = out.getvalue()
    return raw, 'sha256:' + hashlib.sha256(raw).hexdigest()


@pytest.mark.parametrize('payload,name,duplicate', [
    ('{}', '../rewardguard-run.json', False), ('{}', 'rewardguard-run.json', True),
    ('{"base":"a","base":"b"}', 'rewardguard-run.json', False),
    ('{"x":NaN}', 'rewardguard-run.json', False),
])
def test_archive_rejects_ambiguous_members_and_json(payload, name, duplicate):
    from rewardguard.run_artifacts import decode_archive
    raw, digest = _archive(payload, name, duplicate)
    with pytest.raises(RewardGuardError):
        decode_archive(raw, digest, {})


def test_storage_redirect_never_receives_api_token(monkeypatch):
    import urllib.error
    from rewardguard import github
    calls = []
    class Api:
        def open(self, req, timeout):
            assert req.get_header('Authorization') == 'Bearer private-token'
            raise urllib.error.HTTPError(req.full_url, 302, 'redirect',
                {'Location': 'https://test.blob.core.windows.net/archive?sig=opaque'}, None)
    class Storage:
        def open(self, req, timeout):
            calls.append(req)
            return io.BytesIO(b'zip-bytes')
    monkeypatch.setattr(github.urllib.request, 'build_opener', lambda *a: Storage())
    assert github.Client('o/r', 'private-token', Api()).archive(12, 100) == b'zip-bytes'
    assert calls[0].get_header('Authorization') is None
    assert calls[0].get_header('Cookie') is None


def test_owned_checks_reconciled_foreign_checks_and_human_comments_untouched():
    from rewardguard.publisher import publish, PREFIX
    from rewardguard.report import MARKER
    head = 'a'*40
    class Client:
        def __init__(self): self.writes = []
        def get(self, suffix): return {'head': {'sha': head}}
        def pages(self, suffix, field=None):
            if field:
                return [
                    {'id': 1, 'head_sha': head, 'app': {'slug': 'github-actions'}, 'external_id': PREFIX+'contentguard / eligibility'},
                    {'id': 2, 'head_sha': head, 'app': {'slug': 'github-actions'}, 'external_id': PREFIX+'contentguard / OLD'},
                    {'id': 3, 'head_sha': head, 'app': {'slug': 'other-app'}, 'external_id': PREFIX+'contentguard / BAD'},
                ]
            return [{'id': 4, 'body': MARKER, 'user': {'login': 'human', 'type': 'User'}},
                    {'id': 5, 'body': MARKER, 'user': {'login': 'github-actions[bot]', 'type': 'Bot'}}]
        def write(self, *args): self.writes.append(args)
    client = Client()
    data = {'run_identity': {'head': head}, 'content': {'status': 'skipped', 'coverage': []}, 'findings': [], 'notes': []}
    assert publish(client, data, head, pr=1, comment=True) == 'published'
    assert {x[0] for x in client.writes} == {'check-runs/1', 'check-runs/2', 'issues/comments/5'}
    assert next(x for x in client.writes if x[0] == 'check-runs/2')[1]['conclusion'] == 'neutral'


@pytest.mark.parametrize('bad', ['run', 'event', 'head', 'repository', 'attempt', 'digest', 'duplicate', 'expired'])
def test_authenticated_artifacts_bind_run_event_and_archive(monkeypatch, bad):
    from rewardguard.run_artifacts import load_authenticated, identity
    for key, value in {'GITHUB_REPOSITORY': 'o/r', 'GITHUB_RUN_ID': '123', 'GITHUB_RUN_ATTEMPT': '1',
                       'GITHUB_EVENT_NAME': 'pull_request', 'GITHUB_SHA': 'd'*40}.items():
        monkeypatch.setenv(key, value)
    payload = dict(identity('a'*40, 'b'*40, 'c'*40), findings=[], errors=[])
    raw, digest = _archive(json.dumps(payload))
    run = {'id': 123, 'run_attempt': 1, 'event': 'pull_request', 'head_sha': 'd'*40,
           'repository': {'id': 8, 'full_name': 'o/r'}, 'head_repository': {'id': 9}}
    artifact = {'id': 99, 'name': 'rewardguard-run-123-1', 'expired': False, 'digest': digest,
                'size_in_bytes': len(raw), 'workflow_run': {'id': 123, 'head_sha': 'd'*40, 'repository_id': 8, 'head_repository_id': 9}}
    if bad == 'run': run['id'] = 124
    if bad == 'event': run['event'] = 'push'
    if bad == 'head': run['head_sha'] = 'e'*40
    if bad == 'repository': run['repository']['full_name'] = 'evil/r'
    if bad == 'attempt': run['run_attempt'] = 2
    if bad == 'digest': artifact['digest'] = 'sha256:'+'0'*64
    if bad == 'expired': artifact['expired'] = True
    class Client:
        def get(self, suffix): return run
        def pages(self, *a): return [artifact, artifact] if bad == 'duplicate' else [artifact]
        def archive(self, *a): return raw
    with pytest.raises(RewardGuardError):
        load_authenticated('a'*40, 'b'*40, 'c'*40, Client())


@pytest.mark.parametrize('field,value', [('rule', []), ('rule', {}), ('severity', []), ('severity', {})])
def test_artifact_rejects_nonscalar_rule_and_severity_as_controlled_error(field, value):
    from rewardguard.run_artifacts import validate_results
    finding = {'rule':'NEW_FAILURES', 'severity':'fail', 'source':'run', 'message':'test result'}
    finding[field] = value
    with pytest.raises(RewardGuardError):
        validate_results({'findings':[finding], 'errors':[]}, {})


def test_incomplete_low_probability_scope_cannot_publish_success():
    from rewardguard.content_checks import build_checks
    checks = build_checks({'content': {'status':'reviewed', 'coverage':[
        {'rule':'CG_TEST', 'file':'page.md', 'status':'evaluated', 'probability':.1, 'result_complete':False}]},
        'findings':[], 'notes':[]})
    assert next(c for c in checks if c['name'] == 'contentguard / CG_TEST')['conclusion'] == 'neutral'
