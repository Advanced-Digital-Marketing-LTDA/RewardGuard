import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
import pytest
from rewardguard import config, judge, explainer, review_cache
from rewardguard.models import RewardGuardError
from conftest import FakeJev


def test_disk_outage_coalesces_but_memory_still_expires(tmp_path, monkeypatch):
    root = tmp_path / 'file'
    root.write_text('not a directory')
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(root))
    clock = [100.]
    monkeypatch.setattr(review_cache.time, 'time', lambda: clock[0])
    api = FakeJev()
    client = judge.JevClient(config.parse('run_tests=false\n[judge]\ncache_max_age_seconds=10\n'), api_key='key', opener=api)
    with ThreadPoolExecutor(max_workers=6) as pool:
        assert list(pool.map(lambda _: client.ask('state', {'q': 'question'}), range(6))) == [{'q': .02}] * 6
    assert len(api.calls) == 1
    clock[0] = 110.
    client.ask('state', {'q': 'question'})
    assert len(api.calls) == 2


@pytest.mark.parametrize('envelope', [[], 1, None, 'string'])
def test_non_object_records_are_rejected(tmp_path, monkeypatch, envelope):
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    cache = review_cache.ReviewCache('key', 'endpoint')
    (tmp_path / (cache.identity(b'body') + '.json')).write_text(json.dumps(envelope))
    assert cache.load(b'body') is None


def test_corrupt_metadata_recovers_without_losing_authenticated_result(tmp_path, monkeypatch):
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    cache = review_cache.ReviewCache('key', 'endpoint')
    cache.save(b'body', {'ok': True})
    marker = next(tmp_path.glob('.key-*'))
    marker.write_bytes(b'\xff')
    events = []
    assert cache.load(b'body', diagnostic=events.append) == {'ok': True}
    assert 'metadata_invalid' in events
    marker.read_text()


def client(monkeypatch, tmp_path, issues):
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    monkeypatch.setenv('TYPESAFE_API_KEY', 'separate-key')
    monkeypatch.setattr(explainer, '_which', lambda _: 'claude')
    calls = []
    def run(cmd, **kwargs):
        calls.append(kwargs)
        return subprocess.CompletedProcess(cmd, 0, json.dumps({'structured_output': {'issues': issues}}), '')
    monkeypatch.setattr(explainer, '_run', run)
    return explainer.HaikuExplainer(config.Config(install=None, suites=[]), token='oauth'), calls


@pytest.mark.parametrize('content,bad', [(True, {}), (False, []), (False, {'other': []})])
def test_semantically_invalid_signed_cache_is_refreshed(monkeypatch, tmp_path, content, bad):
    obj, calls = client(monkeypatch, tmp_path, [])
    original = obj.cache.load
    bodies = []
    def capture(body, **kwargs):
        bodies.append(body)
        return original(body, **kwargs)
    obj.cache.load = capture
    invoke = lambda: obj.explain_content('@@ -1 +1 @@\n+changed', 'q', 'statement', 'rubric') if content else obj.explain('@@ -1 +1 @@\n+changed', {'q': 'statement'})
    expected = [] if content else {'q': []}
    assert invoke() == expected
    path = tmp_path / (obj.cache.identity(bodies[0]) + '.json')
    path.unlink()
    obj.cache.save(bodies[0], bad)
    assert invoke() == expected
    assert len(calls) == 2
    assert original(bodies[0]) == expected


def test_live_malformed_and_ungrounded_details(monkeypatch, tmp_path):
    bad = {'rule': 'q', 'line': 0, 'code': False, 'problem': [], 'fix': None}
    obj, _ = client(monkeypatch, tmp_path, [bad])
    with pytest.raises(RewardGuardError, match='malformed'):
        obj.explain('@@ -1 +1 @@\n+changed', {'q': 'statement'})
    obj, _ = client(monkeypatch, tmp_path, [{**bad, 'line': 999, 'code': 'absent', 'problem': 'p', 'fix': 'f'}])
    assert obj.explain('@@ -1 +1 @@\n+changed', {'q': 'statement'}) == {'q': []}
    assert all('absent' not in p.read_text() for p in tmp_path.glob('*.json'))


def test_oauth_is_never_signing_material(monkeypatch, tmp_path):
    obj, _ = client(monkeypatch, tmp_path, [])
    monkeypatch.delenv('TYPESAFE_API_KEY')
    obj = explainer.HaikuExplainer(config.Config(install=None, suites=[]), token='oauth')
    assert obj.cache.key != b'oauth'
    assert obj.cache.root is None
    assert obj.explain('state', {'q': 'statement'}) == {'q': []}
    assert obj.explain('state', {'q': 'statement'}) == {'q': []}
    assert obj.usage.snapshot()['code']['explanations']['invocations'] == 1


def test_valid_grounding_is_preserved_and_instruction_changes_invalidate(monkeypatch, tmp_path):
    issue = {'rule': 'q', 'line': 7, 'code': 'changed', 'problem': 'p', 'fix': 'f'}
    obj, calls = client(monkeypatch, tmp_path, [issue])
    state = '@@ -7 +7 @@\n+changed'
    assert obj.explain(state, {'q': 'statement'})['q'][0]['line'] == 7
    assert obj.explain(state, {'q': 'statement'})['q'][0]['code'] == 'changed'
    assert len(calls) == 1
    monkeypatch.setattr(explainer, 'INSTRUCTION', 'Revised instruction')
    assert obj.explain(state, {'q': 'statement'})['q']
    assert len(calls) == 2


def test_outage_after_restored_hit_reuses_completed_result(tmp_path, monkeypatch):
    root = tmp_path / 'cache'
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(root))
    producer = review_cache.ReviewCache('key', 'endpoint')
    producer.save(b'body', {'ok': True})
    consumer = review_cache.ReviewCache('key', 'endpoint')
    assert consumer.load(b'body') == {'ok': True}
    for path in root.iterdir():
        path.unlink()
    root.rmdir()
    root.write_text('storage outage')
    assert consumer.load(b'body') == {'ok': True}


def test_explicit_signing_key_cannot_equal_oauth(monkeypatch, tmp_path):
    client(monkeypatch, tmp_path, [])
    obj = explainer.HaikuExplainer(config.Config(install=None, suites=[]), token='oauth', cache_signing_key='oauth')
    assert obj.cache.root is None
    assert obj.cache.key != b'oauth'
