from rewardguard import config, judge
from conftest import FakeJev


def test_clean_review_is_reused_across_clients(tmp_path, monkeypatch):
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    cfg = config.parse('run_tests = false\n')
    api = FakeJev()
    for _ in range(2):
        judge.JevClient(cfg, api_key='test-key', opener=api).ask('same evidence', {'q': 'same rule'})
    assert len(api.calls) == 1
    judge.JevClient(cfg, api_key='test-key', opener=api).ask('changed evidence', {'q': 'same rule'})
    assert len(api.calls) == 2


def test_findings_are_not_cached(tmp_path, monkeypatch):
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    cfg = config.parse('run_tests = false\n')
    api = FakeJev(rules={('q', 'evidence'): .9})
    for _ in range(2):
        judge.JevClient(cfg, api_key='key', opener=api).ask('evidence', {'q': 'rule'})
    assert len(api.calls) == 2


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
    judge.JevClient(cfg, api_key='key', opener=api).ask('evidence', {'q': 'rule'})
    judge.JevClient(cfg, api_key='different', opener=api).ask('evidence', {'q': 'rule'})
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
        judge.JevClient(cfg, api_key='key', opener=api).ask('evidence', {'content_task': 'classify'})
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
        with pytest.raises(RewardGuardError):
            judge.JevClient(cfg, api_key='key', opener=api).ask('evidence', {'q': 'rule'})
    assert len(api.calls) == 2
    assert not list(tmp_path.glob('*.json'))


def test_large_metadata_batches_preserve_all_questions():
    from rewardguard.content_review import _batches
    questions = [(str(i), 'é' * 1000) for i in range(40)]
    batches = list(_batches(questions, state='state'))
    assert len(batches) > 1
    assert [q for batch in batches for q in batch] == questions
