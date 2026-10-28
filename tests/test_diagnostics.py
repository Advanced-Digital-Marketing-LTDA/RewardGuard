import io
import json
import urllib.error

import pytest

from conftest import FakeJev
from rewardguard import config, judge, review_cache
from rewardguard.models import RewardGuardError
from rewardguard.usage import UsageTracker


def events(usage):
    return usage.diagnostics()['events']


def test_result_cache_events_distinguish_miss_hit_integrity_and_do_not_leak(tmp_path, monkeypatch):
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    usage = UsageTracker()
    client = judge.JevClient(config.parse('run_tests = false\n'), api_key='private-key',
                             opener=FakeJev(), usage=usage, phase='content')
    for _ in range(2):
        client.ask('private-customer-source', {'content_task': 'private-prompt'})
    path = next(tmp_path.glob('*.json'))
    record = json.loads(path.read_text())
    record['signature'] = 'bad-signature'
    path.write_text(json.dumps(record))
    client.ask('private-customer-source', {'content_task': 'private-prompt'})
    client.ask('different-source', {'content_task': 'private-prompt'})
    lookup = [e['reason'] for e in events(usage) if e['category'] == 'result_cache_lookup']
    assert lookup == ['not_found_or_identity_changed', 'hit', 'integrity_failure', 'not_found_or_identity_changed']
    assert [e['request_id'] for e in events(usage) if e['category'] == 'request'] == [1, 2, 3, 4]
    response = next(e for e in events(usage) if e['reason'] == 'response_received')
    assert response['input_tokens'] == 1 and response['output_tokens'] == 0
    assert response['cached_input_tokens_available'] == 0 and 'cached_input_tokens' not in response
    output = json.dumps(usage.diagnostics())
    for private in ('private-key', 'private-customer-source', 'private-prompt', 'bad-signature', str(path)):
        assert private not in output


def test_cache_expiry_and_write_failure_are_visible_without_exception_details(tmp_path, monkeypatch, caplog):
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    now = [100.0]
    monkeypatch.setattr(review_cache.time, 'time', lambda: now[0])
    usage = UsageTracker()
    cfg = config.parse('run_tests = false\n[judge]\ncache_max_age_seconds = 5\n')
    client = judge.JevClient(cfg, api_key='key', opener=FakeJev(), usage=usage)
    client.ask('state', {'q': 'question'})
    now[0] += 5
    monkeypatch.setattr(review_cache.os, 'replace', lambda *_: (_ for _ in ()).throw(OSError('private-error')))
    client.ask('state', {'q': 'question'})
    assert any(e['reason'] == 'expired' for e in events(usage))
    assert any(e['reason'] == 'write_failed' for e in events(usage))
    assert 'private-error' not in json.dumps(usage.diagnostics()) + caplog.text


def test_retry_and_budget_events_are_counted_and_safe(monkeypatch):
    monkeypatch.delenv('REWARDGUARD_CACHE_DIR', raising=False)
    monkeypatch.setattr(judge.time, 'sleep', lambda _: None)
    usage = UsageTracker()
    client = judge.JevClient(config.parse('run_tests = false\n[judge]\nmax_attempts = 2\n'),
                             api_key='key', opener=FakeJev(status=429), usage=usage)
    with pytest.raises(RewardGuardError, match='review incomplete'):
        client.ask('private-state', {'q': 'private-question'})
    assert [e['reason'] for e in events(usage)].count('retryable_http_error') == 2
    assert [e['reason'] for e in events(usage)].count('scheduled') == 2
    assert any(e['category'] == 'budget' and e['reason'] == 'exhausted' for e in events(usage))
    assert usage.snapshot()['code']['attempts'] == 2
    assert 'private-state' not in json.dumps(usage.diagnostics())


def test_provider_error_body_and_invalid_response_are_not_printed(monkeypatch):
    monkeypatch.delenv('REWARDGUARD_CACHE_DIR', raising=False)
    def failure(req, timeout):
        raise urllib.error.HTTPError(req.full_url, 400, 'bad', {}, io.BytesIO(b'private-provider-response'))
    client = judge.JevClient(config.parse('run_tests = false\n'), api_key='key', opener=failure)
    with pytest.raises(RewardGuardError) as error:
        client.ask('state', {'q': 'question'})
    assert 'HTTP 400' in str(error.value)
    assert 'private-provider-response' not in str(error.value)
    bad = judge.JevClient(config.parse('run_tests = false\n'), api_key='key',
                          opener=FakeJev(raw={'answers': {'q': {'type': 'noul', 'noul': 'private-response'}}}))
    with pytest.raises(RewardGuardError) as error:
        bad.ask('state', {'q': 'question'})
    assert 'not a probability' in str(error.value)
    assert 'private-response' not in str(error.value)


def test_unknown_diagnostic_labels_and_fields_are_not_retained():
    usage = UsageTracker()
    usage.event('secret-id', 'secret-phase', 'secret-stage', 'secret-category', 'secret-reason',
                secret_field=42, attempt=1)
    rendered = json.dumps(usage.diagnostics())
    assert 'secret' not in rendered
    assert events(usage)[0]['attempt'] == 1
    assert events(usage)[0]['request_id'] == 0


def test_only_explicit_provider_cache_tokens_are_reported(monkeypatch):
    monkeypatch.delenv('REWARDGUARD_CACHE_DIR', raising=False)
    payload = {'model': 'jev-1.13.0', 'answers': {'q': {'type': 'noul', 'noul': .01}},
               'usage': {'input_tokens': 20, 'cached_input_tokens': 12}}
    usage = UsageTracker()
    client = judge.JevClient(config.parse('run_tests = false\n'), api_key='key',
                             opener=FakeJev(raw=payload), usage=usage)
    client.ask('state', {'q': 'question'})
    response = next(e for e in events(usage) if e['reason'] == 'response_received')
    assert response['cached_input_tokens_available'] == 1 and response['cached_input_tokens'] == 12
    assert response['output_tokens_available'] == 0 and 'output_tokens' not in response


def test_cache_clock_failure_records_safe_specific_reason_and_falls_back(tmp_path, monkeypatch):
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    monkeypatch.setattr(review_cache.time, 'time', lambda: 100.0)
    usage, api = UsageTracker(), FakeJev()
    client = judge.JevClient(config.parse('run_tests = false\n'), api_key='key', opener=api, usage=usage)
    client.ask('state', {'q': 'question'})

    def broken_clock():
        raise OSError('private clock detail')

    monkeypatch.setattr(review_cache.time, 'time', broken_clock)
    client.ask('state', {'q': 'question'})
    assert len(api.calls) == 2
    reasons = [e['reason'] for e in events(usage)]
    assert 'clock_system_error' in reasons and 'clock_unavailable' in reasons
    assert 'private clock detail' not in json.dumps(usage.diagnostics())


def test_broken_clock_warning_stream_is_reported_in_structured_diagnostics(tmp_path, monkeypatch):
    from types import SimpleNamespace

    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    usage, api = UsageTracker(), FakeJev()
    client = judge.JevClient(config.parse('run_tests = false\n'), api_key='key', opener=api, usage=usage)
    client.ask('state', {'q': 'question'})

    def fail(*args):
        raise OSError('private stream or clock detail')

    monkeypatch.setattr(review_cache, 'time', SimpleNamespace(time=fail))
    monkeypatch.setattr(review_cache, 'sys', SimpleNamespace(stderr=SimpleNamespace(write=fail)))
    client.ask('state', {'q': 'question'})
    reasons = [e['reason'] for e in events(usage)]
    assert len(api.calls) == 2
    assert 'clock_warning_write_failed' in reasons and 'clock_system_error' in reasons
    assert 'private stream or clock detail' not in json.dumps(usage.diagnostics())
