from rewardguard import config, judge
from conftest import FakeJev
import json
import pytest


def test_clean_review_is_reused_across_clients(tmp_path, monkeypatch):
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    cfg = config.parse('run_tests = false\n')
    api = FakeJev()
    for _ in range(2):
        assert judge.JevClient(cfg, api_key='test-key', opener=api).ask('same evidence', {'q': 'same rule'}) == {'q': .02}
    assert len(api.calls) == 1
    judge.JevClient(cfg, api_key='test-key', opener=api).ask('changed evidence', {'q': 'same rule'})
    assert len(api.calls) == 2


def test_validated_findings_are_cached(tmp_path, monkeypatch):
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    cfg = config.parse('run_tests = false\n')
    api = FakeJev(rules={('q', 'evidence'): .9})
    for _ in range(2):
        assert judge.JevClient(cfg, api_key='key', opener=api).ask('evidence', {'q': 'rule'}) == {'q': .9}
    assert len(api.calls) == 1


def test_tampered_cache_and_changed_key_are_not_trusted(tmp_path, monkeypatch):
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    cfg = config.parse('run_tests = false\n')
    api = FakeJev()
    judge.JevClient(cfg, api_key='key', opener=api).ask('evidence', {'q': 'rule'})
    import json
    for path in tmp_path.glob('*.json'):
        record = json.loads(path.read_text())
        record['payload'] = json.dumps({'answers': {'q': {'type': 'noul', 'noul': 0.0}}})
        path.write_text(json.dumps(record))
    assert judge.JevClient(cfg, api_key='key', opener=api).ask('evidence', {'q': 'rule'}) == {'q': .02}
    assert judge.JevClient(cfg, api_key='different', opener=api).ask('evidence', {'q': 'rule'}) == {'q': .02}
    assert len(api.calls) == 3


def test_changed_question_and_endpoint_invalidate_cache(tmp_path, monkeypatch):
    from dataclasses import replace
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    cfg = config.parse('run_tests = false\n')
    api = FakeJev()
    judge.JevClient(cfg, api_key='key', opener=api).ask('evidence', {'q': 'rule'})
    judge.JevClient(cfg, api_key='key', opener=api).ask('evidence', {'q': 'new rule'})
    judge.JevClient(replace(cfg, api_url='https://other.example'), api_key='key', opener=api).ask('evidence', {'q': 'rule'})
    assert len(api.calls) == 3


def test_routing_reuses_positive_classification(tmp_path, monkeypatch):
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    cfg = config.parse('run_tests = false\n')
    api = FakeJev(rules={('content_task', 'evidence'): .99})
    for _ in range(2):
        assert judge.JevClient(cfg, api_key='key', opener=api).ask('evidence', {'content_task': 'classify'}) == {'content_task': .99}
    assert len(api.calls) == 1


def test_metadata_batches_reduce_repeated_context_without_dropping_questions():
    from rewardguard.content_review import _batches
    questions = [(str(i), 'question') for i in range(40)]
    batches = list(_batches(questions, state='short context'))
    assert len(batches) == 1
    assert [q for batch in batches for q in batch] == questions


def test_invalid_response_never_becomes_a_cached_pass(tmp_path, monkeypatch):
    import pytest
    from rewardguard.models import RewardGuardError
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    cfg = config.parse('run_tests = false\n')
    api = FakeJev(raw={'answers': {}})
    for _ in range(2):
        with pytest.raises(RewardGuardError, match="no usable answer"):
            judge.JevClient(cfg, api_key='key', opener=api).ask('evidence', {'q': 'rule'})
    assert len(api.calls) == 2
    assert not list(tmp_path.glob('*.json'))


def test_large_metadata_batches_preserve_all_questions():
    from rewardguard.content_review import _batches
    questions = [(str(i), 'é' * 1000) for i in range(40)]
    batches = list(_batches(questions, state='state'))
    assert len(batches) > 1
    assert [q for batch in batches for q in batch] == questions


def test_cache_expires_at_24_hours(tmp_path, monkeypatch):
    from rewardguard import review_cache
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    now = [100_000.0]
    monkeypatch.setattr(review_cache.time, 'time', lambda: now[0])
    cfg, api = config.parse('run_tests = false\n[judge]\ncache_max_age_seconds = 86400\n'), FakeJev()
    client = judge.JevClient(cfg, api_key='key', opener=api)
    client.ask('source', {'q': 'question'})
    now[0] += 24 * 60 * 60 - 0.001
    client.ask('source', {'q': 'question'})
    assert len(api.calls) == 1
    now[0] += 0.001
    client.ask('source', {'q': 'question'})
    assert len(api.calls) == 2


def test_default_cache_does_not_expire_solely_with_age(tmp_path, monkeypatch):
    from rewardguard import review_cache
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    now = [100_000.0]
    monkeypatch.setattr(review_cache.time, 'time', lambda: now[0])
    client = judge.JevClient(config.parse('run_tests = false\n'), api_key='key', opener=FakeJev())
    client.ask('source', {'q': 'question'})
    now[0] += 7 * 24 * 60 * 60
    client.ask('source', {'q': 'question'})
    assert client.cache_hits == 1


@pytest.mark.parametrize('value', ['0', '-1', 'true', '1.5', '"86400"'])
def test_invalid_cache_max_age_rejected(value):
    from rewardguard.models import RewardGuardError
    with pytest.raises(RewardGuardError, match='cache_max_age_seconds.*positive integer'):
        config.parse(f'run_tests = false\n[judge]\ncache_max_age_seconds = {value}\n')


def test_timestamp_is_authenticated_and_legacy_records_are_not_reused(tmp_path, monkeypatch):
    from rewardguard import review_cache
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    monkeypatch.setattr(review_cache.time, 'time', lambda: 100_000.0)
    cfg, api = config.parse('run_tests = false\n'), FakeJev()
    client = judge.JevClient(cfg, api_key='key', opener=api)
    client.ask('sensitive source text', {'q': 'rule'})
    path = next(tmp_path.glob('*.json'))
    record = json.loads(path.read_text())
    assert 'sensitive source text' not in path.read_text() and '"key"' not in path.read_text()
    record['created_at'] -= 1
    path.write_text(json.dumps(record))
    client.ask('sensitive source text', {'q': 'rule'})
    assert len(api.calls) == 2
    record = json.loads(path.read_text())
    del record['created_at']
    path.write_text(json.dumps(record))
    client.ask('sensitive source text', {'q': 'rule'})
    assert len(api.calls) == 3


def test_cache_epoch_forces_fresh_request_and_rejects_copied_entry(tmp_path, monkeypatch):
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    old = config.parse('run_tests = false\n[judge]\ncache_epoch = "provider-2026a"\n')
    new = config.parse('run_tests = false\n[judge]\ncache_epoch = "provider-2026b"\n')
    api = FakeJev()
    a = judge.JevClient(old, api_key='key', opener=api)
    b = judge.JevClient(new, api_key='key', opener=api)
    a.ask('state', {'q': 'question'})
    old_path = next(tmp_path.glob('*.json'))
    body = json.dumps({'model': new.model, 'state': 'state',
                       'questions': {'q': {'type': 'noul', 'instructions': 'question'}}}).encode()
    (tmp_path / (b.cache.identity(body) + '.json')).write_bytes(old_path.read_bytes())
    b.ask('state', {'q': 'question'})
    assert len(api.calls) == 2
    a.ask('state', {'q': 'question'})
    b.ask('state', {'q': 'question'})
    assert len(api.calls) == 2


@pytest.mark.parametrize('epoch', ['""', '"contains space"', 'true', '123', '"' + 'x' * 65 + '"'])
def test_cache_epoch_rejects_invalid_trusted_config(epoch):
    from rewardguard.models import RewardGuardError
    with pytest.raises(RewardGuardError, match='cache_epoch'):
        config.parse(f'run_tests = false\n[judge]\ncache_epoch = {epoch}\n')


@pytest.mark.parametrize('bad_clock', [float('nan'), float('inf'), -1, None])
def test_invalid_clock_disables_cache_read_and_write(tmp_path, monkeypatch, bad_clock):
    from rewardguard import review_cache
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    monkeypatch.setattr(review_cache.time, 'time', lambda: 100_000.0)
    cfg, api = config.parse('run_tests = false\n'), FakeJev()
    client = judge.JevClient(cfg, api_key='key', opener=api)
    client.ask('state', {'q': 'question'})
    path = next(tmp_path.glob('*.json'))
    before = path.read_bytes()
    monkeypatch.setattr(review_cache.time, 'time', lambda: bad_clock)
    client.ask('state', {'q': 'question'})
    assert len(api.calls) == 2
    assert path.read_bytes() == before


def test_clock_error_and_backwards_clock_miss_safely(tmp_path, monkeypatch):
    from rewardguard import review_cache
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    monkeypatch.setattr(review_cache.time, 'time', lambda: 100_000.0)
    cfg, api = config.parse('run_tests = false\n'), FakeJev()
    client = judge.JevClient(cfg, api_key='key', opener=api)
    client.ask('state', {'q': 'question'})
    monkeypatch.setattr(review_cache.time, 'time', lambda: 99_999.0)
    client.ask('state', {'q': 'question'})
    assert len(api.calls) == 2
    path = next(tmp_path.glob('*.json'))
    before = path.read_bytes()
    def broken_clock():
        raise OSError('clock unavailable')
    monkeypatch.setattr(review_cache.time, 'time', broken_clock)
    client.ask('state', {'q': 'question'})
    assert len(api.calls) == 3
    assert path.read_bytes() == before


@pytest.mark.parametrize('error,reason', [
    (OSError('private-path'), 'clock_system_error'),
    (ValueError('private-value'), 'clock_invalid_value'),
    (RuntimeError('private-detail'), 'clock_unexpected_error'),
])
def test_clock_exceptions_are_reported_without_sensitive_detail(monkeypatch, error, reason):
    from rewardguard import review_cache

    def broken_clock():
        raise error

    monkeypatch.setattr(review_cache.time, 'time', broken_clock)
    events = []
    assert review_cache._clock(diagnostic=events.append) is None
    assert events == [reason]


def test_clock_failure_warns_without_callback_or_secret_details(tmp_path, monkeypatch, capsys):
    from types import SimpleNamespace
    from rewardguard import review_cache

    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    cache = review_cache.ReviewCache('key', 'endpoint')
    cache.save(b'body', {'ok': True})

    def broken_clock():
        raise RuntimeError('private-path-and-value')

    monkeypatch.setattr(review_cache, 'time', SimpleNamespace(time=broken_clock))
    assert cache.load(b'body') is None
    cache.save(b'other', {'ok': True})
    assert len(list(tmp_path.glob('*.json'))) == 1
    output = capsys.readouterr().err
    assert output.count('RewardGuard cache clock unavailable; reviewing again') == 2
    assert 'private-path-and-value' not in output


def test_broken_warning_stream_does_not_break_clock_fallback(monkeypatch):
    from types import SimpleNamespace
    from rewardguard import review_cache

    def fail(*args):
        raise OSError('private error')

    monkeypatch.setattr(review_cache, 'time', SimpleNamespace(time=fail))
    monkeypatch.setattr(review_cache, 'sys', SimpleNamespace(stderr=SimpleNamespace(write=fail)))
    events = []
    assert review_cache._clock(diagnostic=events.append) is None
    assert events == ['clock_warning_write_failed', 'clock_system_error']


def test_overflowing_cache_timestamp_reports_invalidation(tmp_path, monkeypatch):
    from rewardguard import review_cache

    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    cache = review_cache.ReviewCache('key', 'endpoint')
    cache.save(b'body', {'ok': True})
    path = next(tmp_path.glob('*.json'))
    record = json.loads(path.read_text())
    record['created_at'] = 10 ** 400
    path.write_text(json.dumps(record))
    events = []
    assert cache.load(b'body', diagnostic=events.append) is None
    assert events == ['invalid_timestamp']
