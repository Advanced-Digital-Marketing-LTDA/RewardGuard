import argparse
import json
import subprocess

from rewardguard import cli, config, report
from rewardguard.models import Report


def test_identity_keeps_valid_commit_and_model_fields_and_rejects_arbitrary_text(monkeypatch):
    monkeypatch.setenv('GITHUB_EVENT_NAME', 'pull_request')
    monkeypatch.setenv('REWARDGUARD_EVENT_ACTION', 'synchronize')
    monkeypatch.setenv('REWARDGUARD_ACTION_REVISION', 'd' * 40)
    monkeypatch.setenv('GITHUB_RUN_ID', '123456789')
    monkeypatch.setenv('GITHUB_RUN_ATTEMPT', '2')
    identity = cli._run_identity(argparse.Namespace(staged=False, content_only=True),
                                 base='a' * 40, head='b' * 40, policy='c' * 40,
                                 cfg=config.Config(install=None, suites=[]))
    assert identity == {'event': 'pull_request', 'action': 'synchronize',
                        'action_revision': 'd' * 40, 'base': 'a' * 40, 'head': 'b' * 40,
                        'trusted_policy': 'c' * 40, 'model': 'jev-1.13.0',
                        'review_mode': 'content_only', 'run_id': '123456789', 'run_attempt': '2'}
    monkeypatch.setenv('GITHUB_EVENT_NAME', 'private/secret')
    monkeypatch.setenv('REWARDGUARD_EVENT_ACTION', 'token=secret')
    monkeypatch.setenv('REWARDGUARD_ACTION_REVISION', 'refs/private/secret')
    monkeypatch.setenv('GITHUB_RUN_ID', 'token=secret')
    monkeypatch.setenv('GITHUB_RUN_ATTEMPT', '0' * 40)
    identity = cli._run_identity(argparse.Namespace(), base='private/path', head='short',
                                 policy='password', cfg=config.Config(install=None, suites=[], model='secret-model'))
    assert all(value == 'unknown' for key, value in identity.items() if key != 'review_mode')
    assert identity['review_mode'] == 'full'


def test_evidence_diagnostics_count_known_reasons_without_copying_paths_or_unknown_text():
    content = {'status': 'reviewed', 'coverage': [
        {'status': 'skipped', 'file': 'secret-page'},
        {'status': 'not_evaluated', 'reason': 'private source text'},
        {'status': 'evaluated'}, {'status': 'not_applicable'}, {'status': 'secret-status'}],
        'omissions': [{'reason': 'File not available at revision', 'path': 'secret-file'},
                      {'reason': 'File not available at revision'},
                      {'reason': 'Whole evidence unit exceeds per-file or remaining total budget'},
                      {'reason': 'private source text', 'path': 'secret-file'}]}
    summary = report.evidence_diagnostics(content)
    assert summary['coverage'] == {'eligible': 0, 'evaluated': 1, 'skipped': 1,
                                   'not_applicable': 1, 'not_evaluated': 1, 'unknown': 1}
    assert summary['omission_reasons'] == {'unavailable_at_revision': 2, 'unit_budget': 1,
                                          'other_or_unknown': 1}
    assert summary['omission_count'] == 4
    rep = Report(content=content)
    encoded = json.loads(report.as_json(rep))
    assert encoded['diagnostics']['evidence'] == summary
    assert 'secret' not in json.dumps(encoded['diagnostics'])
    assert 'secret' not in report.terminal(rep)
    assert 'skipped=1' in report.terminal(rep)
    assert 'unavailable_at_revision=2' in report.terminal(rep)
    assert summary['not_evaluated_reasons'] == {'unknown': 1}


def test_coverage_gap_reasons_are_fixed_labels_with_unknown_text_hidden():
    summary = report.evidence_diagnostics({'status': 'not_evaluated', 'coverage': [
        {'status': 'not_evaluated', 'reason': 'Relevant check lacks specific supporting evidence after repository discovery'},
        {'status': 'not_evaluated', 'reason': 'Supplied sources do not establish this specific target/claim or required condition'},
        {'status': 'not_evaluated', 'reason': 'No textual source; binary/visual evidence is unavailable'},
        {'status': 'not_evaluated', 'reason': 'secret-path: secret-prompt'},
        {'status': 'not_evaluated'},
        {'status': 'skipped', 'reason': 'secret-prompt'}]})
    assert summary['not_evaluated_reasons'] == {'missing_evidence_after_discovery': 1,
                                              'insufficient_target_evidence': 1,
                                              'binary_or_no_text': 1, 'unknown': 2}
    assert 'secret' not in json.dumps(summary)


def test_cli_no_changes_still_records_safe_identity_and_diagnostics(tmp_path, monkeypatch):
    def git(*args):
        return subprocess.run(['git', '-C', str(tmp_path), *args], check=True,
                              text=True, capture_output=True).stdout.strip()
    git('init', '-q', '-b', 'main')
    git('config', 'user.name', 'Test')
    git('config', 'user.email', 'test@example.test')
    (tmp_path / '.rewardguard.toml').write_text('run_tests = false\n')
    git('add', '.')
    git('commit', '-qm', 'base')
    commit = git('rev-parse', 'HEAD')
    monkeypatch.setenv('GITHUB_EVENT_NAME', 'push')
    monkeypatch.delenv('REWARDGUARD_EVENT_ACTION', raising=False)
    target = tmp_path / 'report.json'
    assert cli.main(['check', '--repo', str(tmp_path), '--base', 'main',
                     '--content-only', '--json', str(target)]) == 0
    data = json.loads(target.read_text())
    assert data['run_identity']['base'] == data['run_identity']['head'] == commit
    assert data['run_identity']['trusted_policy'] == commit
    assert data['run_identity']['event'] == 'push'
    assert data['run_identity']['action'] == 'unknown'
    assert data['diagnostics']['provider_cache_accounting'] == 'only when explicitly returned per response; otherwise unavailable'
    assert data['diagnostics']['evidence']['status'] == 'skipped'


def test_terminal_prints_each_sanitized_diagnostic_event_without_sensitive_values(monkeypatch):
    from rewardguard.usage import UsageTracker
    tracker = UsageTracker()
    tracker.event(1, 'content', 'classification', 'request', 'started',
                  state_characters=200, question_count=1, secret='private-prompt')
    tracker.event(2, 'private-path', 'private-prompt', 'private-category', 'private-reason',
                  request_bytes=100, private_key=123)
    rep = Report(diagnostics=tracker.diagnostics())
    terminal = report.terminal(rep)
    lines = [json.loads(line.removeprefix('diag   ')) for line in terminal.splitlines()
             if line.startswith('diag   {')]
    assert len(lines) == 2
    assert lines[0]['request_id'] == 1 and lines[0]['state_characters'] == 200
    assert lines[1]['phase'] == lines[1]['stage'] == lines[1]['category'] == lines[1]['reason'] == 'other'
    assert 'private' not in terminal
    assert 'private' not in json.dumps(json.loads(report.as_json(rep))['diagnostics'])
    assert '0 events dropped' in terminal
