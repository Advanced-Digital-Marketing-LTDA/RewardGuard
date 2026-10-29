import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

import pytest

from conftest import FakeJev
from rewardguard import config, judge
from rewardguard.models import RewardGuardError
from rewardguard.usage import UsageTracker


@pytest.mark.parametrize('setting', ['max_attempts', 'max_request_bytes'])
@pytest.mark.parametrize('value', ['0', '-1', 'true', '1.5', '"100"'])
def test_invalid_budgets_fail_config_validation(setting, value):
    with pytest.raises(RewardGuardError, match='positive integer'):
        config.parse(f'run_tests = false\n[judge]\n{setting} = {value}\n')


def test_global_budget_spans_content_and_code_and_counts_cache_hits(tmp_path, monkeypatch):
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path))
    cfg = config.parse('run_tests = false\n[judge]\nmax_attempts = 1\n[[content.publications]]\nid="page"\nsources=["page.md"]\ntype="page"\nroute="/"\n')
    usage, api = UsageTracker(), FakeJev()
    content = judge.JevClient(cfg, api_key='key', opener=api, usage=usage, phase='content', cache_namespace='shared-test')
    code = judge.JevClient(cfg, api_key='key', opener=api, usage=usage, phase='code', cache_namespace='shared-test')
    assert content.ask('same', {'q': 'question'}) == {'q': .02}
    assert code.ask('same', {'q': 'question'}) == {'q': .02}  # authenticated cache hit
    with pytest.raises(RewardGuardError, match='max_attempts.*review incomplete'):
        code.ask('new state', {'q': 'question'})
    assert len(api.calls) == 1
    assert usage.snapshot()['content']['attempts'] == 1
    assert usage.snapshot()['code']['cache_hits'] == 1
    assert usage.snapshot()['code']['budget_denials'] == 1
    assert usage.snapshot()['code']['attempts'] == 0


def test_byte_budget_uses_actual_serialized_body_and_is_checked_before_send(monkeypatch):
    monkeypatch.delenv('REWARDGUARD_CACHE_DIR', raising=False)
    state, questions = 'é', {'q': 'question'}
    body_size = len(json.dumps({'model': 'jev-1.13.0', 'state': state,
                               'questions': {'q': {'type': 'noul', 'instructions': 'question'}}}).encode())
    cfg = config.parse(f'run_tests = false\n[judge]\nmax_request_bytes = {body_size}\n')
    tracker, api = UsageTracker(), FakeJev()
    client = judge.JevClient(cfg, api_key='key', opener=api, usage=tracker)
    client.ask(state, questions)
    with pytest.raises(RewardGuardError, match='max_request_bytes.*review incomplete'):
        client.ask(state + "changed", questions)
    assert len(api.calls) == 1
    assert tracker.snapshot()['code']['request_bytes'] == body_size


def test_retry_attempts_consume_budget_and_failed_calls_remain_visible(monkeypatch):
    monkeypatch.delenv('REWARDGUARD_CACHE_DIR', raising=False)
    monkeypatch.setattr(judge.time, 'sleep', lambda _: None)
    cfg = config.parse('run_tests = false\n[judge]\nmax_attempts = 2\n')
    tracker, api = UsageTracker(), FakeJev(status=429)
    client = judge.JevClient(cfg, api_key='key', opener=api, usage=tracker)
    with pytest.raises(RewardGuardError, match='max_attempts.*review incomplete'):
        client.ask('state', {'q': 'question'})
    assert len(api.calls) == 2
    row = tracker.snapshot()['code']
    assert row['attempts'] == 2 and row['requests'] == 0 and row['budget_denials'] == 1
    assert row['request_bytes'] > 0


def test_shared_reservations_are_atomic_under_concurrency():
    tracker = UsageTracker()
    tracker.configure(5, 50)

    def reserve(_):
        try:
            tracker.reserve('code', 10)
            return True
        except RewardGuardError:
            return False

    with ThreadPoolExecutor(max_workers=20) as pool:
        results = list(pool.map(reserve, range(40)))
    assert sum(results) == 5
    row = tracker.snapshot()['code']
    assert row['attempts'] == 5 and row['request_bytes'] == 50 and row['budget_denials'] == 35


def test_mixed_staged_and_unstaged_usage_counts_each_request_once():
    tracker = UsageTracker()
    tracker.configure(3, 100)
    for stage, size, tokens in ((None, 10, 2), ('routing', 20, 3), ('routing', 30, 5)):
        tracker.reserve('content', size, stage)
        tracker.record('content', 'abc', {'q': 'xy'}, {'usage': {'input_tokens': tokens}}, stage)
        tracker.cache_hit('content', stage)
    with pytest.raises(RewardGuardError, match='max_attempts'):
        tracker.reserve('content', 1, None)
    with pytest.raises(RewardGuardError, match='max_attempts'):
        tracker.reserve('content', 1, 'routing')
    total = tracker.snapshot()['content']
    stage = total['stages']['routing']
    assert (total['attempts'], total['request_bytes'], total['requests'], total['input_tokens'], total['cache_hits'], total['budget_denials']) == (3, 60, 3, 10, 3, 2)
    assert (stage['attempts'], stage['request_bytes'], stage['requests'], stage['input_tokens'], stage['cache_hits'], stage['budget_denials']) == (2, 50, 2, 8, 2, 1)
    assert (total['state_characters'], total['question_characters']) == (9, 6)
    assert (stage['state_characters'], stage['question_characters']) == (6, 4)


def test_unstaged_usage_does_not_create_a_stage_or_double_count():
    tracker = UsageTracker()
    tracker.configure(None, None)
    tracker.reserve('code', 7)
    tracker.record('code', 'a', {'q': 'b'}, {'usage': {'input_tokens': 1}})
    tracker.cache_hit('code')
    row = tracker.snapshot()['code']
    assert 'stages' not in row
    assert (row['attempts'], row['requests'], row['cache_hits'], row['request_bytes']) == (1, 1, 1, 7)


def test_content_stages_measure_each_request_without_recording_content(monkeypatch):
    monkeypatch.delenv('REWARDGUARD_CACHE_DIR', raising=False)
    cfg = config.parse('run_tests = false\n')
    tracker, api = UsageTracker(), FakeJev()
    client = judge.JevClient(cfg, api_key='key', opener=api, usage=tracker, phase='content')
    for key in ('content_task', 'pack_writing', 'applies_rule', 'CG_RULE'):
        client.ask('private source', {key: 'private question'})
    summary = tracker.snapshot()['content']
    assert summary['attempts'] == 4 and summary['requests'] == 4
    assert set(summary['stages']) == {'classification', 'routing', 'applicability', 'evaluation'}
    assert sum(row['request_bytes'] for row in summary['stages'].values()) == summary['request_bytes']
    assert all(row['requests'] == 1 and row['input_tokens'] == 1 for row in summary['stages'].values())
    assert 'private source' not in str(summary) and 'private question' not in str(summary)
    summary['stages']['routing']['attempts'] = 999
    assert tracker.snapshot()['content']['stages']['routing']['attempts'] == 1


def test_budget_exhaustion_fails_the_content_check(tmp_path, monkeypatch):
    from rewardguard import cli
    monkeypatch.delenv('REWARDGUARD_CACHE_DIR', raising=False)

    def git(*args):
        return subprocess.run(['git', '-C', str(tmp_path), *args], text=True,
                              capture_output=True, check=True).stdout.strip()
    git('init', '-q', '-b', 'main')
    git('config', 'user.name', 'Test')
    git('config', 'user.email', 'test@example.test')
    (tmp_path / '.rewardguard.toml').write_text('run_tests = false\n[judge]\nmax_attempts = 1\n[[content.publications]]\nid="page"\nsources=["page.md"]\ntype="page"\nroute="/"\n')
    (tmp_path / 'page.md').write_text('# Product\nOld promise.\n')
    git('add', '.')
    git('commit', '-qm', 'base')
    git('checkout', '-qb', 'change')
    (tmp_path / 'page.md').write_text('# Product\nNew promise.\n')
    git('add', '.')
    git('commit', '-qm', 'change')

    api = FakeJev(rules={('content_task', 'New promise'): .9})
    original_init = judge.JevClient.__init__

    def fake_init(self, cfg, *args, **kwargs):
        return original_init(self, cfg, *args, api_key='fake', opener=api, **kwargs)

    monkeypatch.setattr(judge.JevClient, '__init__', fake_init)
    result_path = tmp_path / 'result.json'
    assert cli.main(['check', '--repo', str(tmp_path), '--base', 'main', '--content-only',
                     '--json', str(result_path)]) == 2
    result = json.loads(result_path.read_text())
    assert result['failed']
    assert result['content']['status'] == 'error'
    assert any('max_attempts' in error and 'review incomplete' in error for error in result['errors'])
    assert len(api.calls) == 1
