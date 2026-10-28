from concurrent.futures import ThreadPoolExecutor
from rewardguard import config, judge, review_cache, explainer
from conftest import FakeJev


def test_canonical_repository_and_scope_identity(monkeypatch):
    monkeypatch.setenv('GITHUB_REPOSITORY', 'Owner/Repo')
    a = review_cache.ReviewCache('key', 'endpoint', namespace='content')
    b = review_cache.ReviewCache('key', 'endpoint', namespace='code')
    assert a.identity(b'{"b":2,"a":1}') == a.identity(b'{"a":1,"b":2}')
    assert a.identity(b'{}') != b.identity(b'{}')
    monkeypatch.setenv('GITHUB_REPOSITORY', 'other/repo')
    assert a.identity(b'{}') != review_cache.ReviewCache('key', 'endpoint', namespace='content').identity(b'{}')


def test_disabled_cache_still_coalesces_requests(monkeypatch):
    monkeypatch.delenv('REWARDGUARD_CACHE_DIR', raising=False)
    api = FakeJev()
    client = judge.JevClient(config.parse('run_tests = false\n'), api_key='key', opener=api)
    with ThreadPoolExecutor(max_workers=8) as pool:
        answers = list(pool.map(lambda _: client.ask('same', {'q': 'rule'}), range(12)))
    assert answers == [{'q': .02}] * 12
    assert len(api.calls) == 1


def test_haiku_environment_is_allowlisted(monkeypatch):
    monkeypatch.setattr(explainer, '_which', lambda _: '/usr/bin/claude')
    monkeypatch.setenv('TYPESAFE_API_KEY', 'signing-key')
    monkeypatch.setenv('CUSTOM_SECRET', 'secret')
    client = explainer.HaikuExplainer(config.Config(install=None, suites=[]), token='oauth')
    assert 'TYPESAFE_API_KEY' not in client._env()
    assert 'CUSTOM_SECRET' not in client._env()
    assert client._env()['CLAUDE_CODE_OAUTH_TOKEN'] == 'oauth'


def test_explanations_reuse_validated_results(monkeypatch, tmp_path):
    import json
    import subprocess
    calls = []
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    monkeypatch.setattr(explainer, '_which', lambda _: '/usr/bin/claude')
    def run(cmd, **kwargs):
        calls.append(kwargs)
        return subprocess.CompletedProcess(cmd, 0, json.dumps({'structured_output': {'issues': []}}), '')
    monkeypatch.setattr(explainer, '_run', run)
    cfg = config.Config(install=None, suites=[])
    for _ in range(2):
        client = explainer.HaikuExplainer(cfg, token='oauth')
        assert client.explain_content('private prompt', 'CG_RULE', 'statement', 'rubric') == []
    assert len(calls) == 1
    assert 'private prompt' not in ''.join(p.read_text() for p in tmp_path.glob('*.json'))


def test_rotated_key_has_explicit_diagnostic_and_metadata_recovers(monkeypatch, tmp_path):
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    cache = review_cache.ReviewCache('old', 'endpoint')
    cache.save(b'body', {'ok': True})
    events = []
    rotated = review_cache.ReviewCache('new', 'endpoint')
    assert rotated.load(b'body', diagnostic=events.append) is None
    assert 'signing_key_changed' in events
    for path in tmp_path.glob('.key-*'):
        path.unlink()
    assert cache.load(b'body') == {'ok': True}
