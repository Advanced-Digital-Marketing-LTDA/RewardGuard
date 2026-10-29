from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
import pytest
from rewardguard import cli, config, gitops, judge, report
from rewardguard.models import Finding, Report, RewardGuardError


def git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), *args], check=True, text=True, capture_output=True).stdout.strip()


@pytest.fixture
def history(tmp_path):
    git(tmp_path, 'init', '-q', '-b', 'main')
    git(tmp_path, 'config', 'user.name', 't')
    git(tmp_path, 'config', 'user.email', 't@t.test')
    (tmp_path / '.rewardguard.toml').write_text('run_tests = false\n')
    (tmp_path / 'a.py').write_text('value = 0\n')
    git(tmp_path, 'add', '.')
    git(tmp_path, 'commit', '-qm', 'base')
    base = git(tmp_path, 'rev-parse', 'HEAD')
    git(tmp_path, 'checkout', '-qb', 'feature')
    (tmp_path / 'a.py').write_text('value = 1\n')
    git(tmp_path, 'commit', '-qam', 'before')
    before = git(tmp_path, 'rev-parse', 'HEAD')
    git(tmp_path, 'checkout', '-qB', 'replacement', base)
    (tmp_path / 'a.py').write_text('value = 2\n')
    git(tmp_path, 'commit', '-qam', 'head')
    return tmp_path, base, before, git(tmp_path, 'rev-parse', 'HEAD')


def test_explicit_push_keeps_divergent_before_and_separate_policy(history):
    repo, policy, before, head = history
    args = argparse.Namespace(base=before, head=head, allow_dirty=False, comparison_mode='explicit', policy_base=policy)
    base, actual_head, cfg = cli._resolve(str(repo), args)
    assert (base, actual_head, args.config_base) == (before, head, policy)
    assert cfg.run_tests is False


def test_plan_never_constructs_provider_or_resolves_network_context(history, monkeypatch, capsys):
    from rewardguard import pr_context
    repo, base, _, head = history
    def forbidden(*a, **kw):
        raise AssertionError('provider/context constructed')
    monkeypatch.setattr(judge, 'JevClient', forbidden)
    monkeypatch.setattr(cli.explainer, 'HaikuExplainer', forbidden)
    monkeypatch.setattr(pr_context, 'resolve', forbidden)
    assert cli.main(['check', '--repo', str(repo), '--base', base, '--head', head, '--plan']) == 0
    data = json.loads(capsys.readouterr().out)
    assert data['status'] == 'planned'
    assert data['run_identity']['head'] == head
    assert data['content']['cache']['availability'] in {'disabled', 'configured'}
    assert (data['code']['selected'] + data['code']['excluded'])[0]['path'] == 'a.py'


def test_git_reads_never_run_selected_helpers(history, tmp_path):
    repo, base, _, head = history
    sentinel = repo / 'executed'
    helper = repo / 'driver.sh'
    helper.write_text('#!/bin/sh\ntouch "' + str(sentinel) + '"\ncat "$1"\n')
    helper.chmod(0o755)
    (repo / '.gitattributes').write_text('*.py diff=evil\n')
    git(repo, 'config', 'diff.evil.textconv', str(helper))
    git(repo, 'config', 'diff.evil.command', str(helper))
    git(repo, 'config', 'core.fsmonitor', str(helper))
    assert gitops.file_hunks(str(repo), base, head, 'a.py', 3)
    gitops.is_dirty(str(repo))
    assert gitops.show_file(str(repo), head, 'a.py') == 'value = 2\n'
    assert not sentinel.exists()


def test_partial_judge_and_explanation_failures_preserve_grade(history):
    repo, base, _, head = history
    cfg = config.parse('run_tests = false\n[judge]\nconcurrency = 1\n')
    changed = gitops.changed_files(str(repo), base, head)
    class Jev:
        def ask(self, state, questions):
            if 'scope_creep' in questions:
                raise RewardGuardError('later scope failed')
            return {key: .91 if key == 'hardcoded' else .1 for key in questions}
    class Haiku:
        def explain(self, *a, **kw):
            raise RewardGuardError('explanation failed')
    result = judge.run(str(repo), base, head, cfg, changed, {'a.py': 'source'}, 'task', Jev(), Haiku())
    assert result.findings and result.findings[0].probability == .91
    assert any('later scope failed' in e for e in result.errors)
    assert any('explanation failed' in e for e in result.errors)


def test_required_gaps_incomplete_but_unchanged_is_not():
    rep = Report(content={'status': 'reviewed', 'coverage': [{'status': 'not_evaluated', 'reason': 'missing evidence'}]})
    assert 'INCOMPLETE' in report.terminal(rep)
    assert json.loads(report.as_json(rep))['status'] == 'incomplete'
    rep.content = {'status': 'skipped', 'coverage': [{'status': 'unchanged'}]}
    assert json.loads(report.as_json(rep))['status'] == 'skipped'


def test_independent_inputs_reuse_across_cosmetic_pr_edits(history):
    repo, base, _, head = history
    cfg = config.parse('run_tests = false\n')
    class Jev:
        def __init__(self): self.calls = []
        def ask(self, state, questions):
            self.calls.append((state, questions))
            return {k: .1 for k in questions}
    class Haiku:
        def explain(self, *a, **kw): raise AssertionError('clean grades need no explanation')
    clients = [Jev(), Jev()]
    for description, client in zip(('first title', 'cosmetically edited title'), clients):
        judge.run(str(repo), base, head, cfg, gitops.changed_files(str(repo), base, head),
                  {'a.py': 'source'}, description, client, Haiku())
    independent = [[c for c in client.calls if 'hardcoded' in c[1]] for client in clients]
    assert independent[0] == independent[1]
    dependent = [[c for c in client.calls if 'scope_creep' in c[1]] for client in clients]
    assert dependent[0] != dependent[1]
    assert all(any('overclaim' in key for _, q in c.calls for key in q) for c in clients)


def test_output_failure_preserves_original_error_and_writes_json(tmp_path, capsys):
    rep = Report(errors=['original provider error'], findings=[Finding('HARDCODED_OUTPUT', 'fail', 'retained', probability=.9)])
    args = argparse.Namespace(markdown=str(tmp_path/'missing'/'report.md'), json=str(tmp_path/'report.json'))
    assert cli._finish(rep, args) == 2
    data = json.loads((tmp_path/'report.json').read_text())
    assert data['errors'][0] == 'original provider error'
    assert len(data['errors']) == 2
    assert data['findings'][0]['probability'] == .9


def test_later_chunk_failure_keeps_completed_raw_grade(history, monkeypatch):
    repo, base, _, head = history
    cfg = config.parse('run_tests = false\n[judge]\nconcurrency = 1\n')
    chunks = [judge.Chunk('first.js', 'source', 'first', 1, 'first'),
              judge.Chunk('later.js', 'source', 'later', 1, 'later')]
    monkeypatch.setattr(judge, 'build_chunks', lambda *a: chunks)
    class Jev:
        def ask(self, state, questions):
            if state == 'later': raise RewardGuardError('later chunk failed')
            return {key: .9 if key == 'hardcoded' else .1 for key in questions}
    class Haiku:
        def explain(self, state, statements, **kw): return {key: [] for key in statements}
    result = judge.run(str(repo), base, head, cfg, [], {'first.js':'source'}, '', Jev(), Haiku())
    assert [(f.rule, f.probability) for f in result.findings] == [('HARDCODED_OUTPUT', .9)]
    assert any('later chunk failed' in e for e in result.errors)


def test_expected_justification_failure_retains_score(history, monkeypatch):
    repo, base, _, head = history
    cfg = config.parse('run_tests = false\n')
    monkeypatch.setattr(judge, 'build_chunks', lambda *a: [judge.Chunk('a.test.js', 'test', 'test', 1, 'diff')])
    class Jev:
        def ask(self, state, questions):
            if 'justified' in questions: raise RewardGuardError('justification unavailable')
            return {key: .9 if key == 'expected_changed' else .1 for key in questions}
    class Haiku:
        def explain(self, state, statements, **kw): return {key: [] for key in statements}
    result = judge.run(str(repo), base, head, cfg, [], {'a.test.js':'test', 'code.js':'source'}, 'complete task', Jev(), Haiku())
    assert any(f.rule == 'EXPECTED_VALUE_CHANGED' and f.probability == .9 for f in result.findings)
    assert any('justification unavailable' in e for e in result.errors)


def test_completed_confirmation_survives_later_confirmation_failure(history, monkeypatch):
    repo, base, _, head = history
    cfg = config.parse('run_tests = false\n')
    monkeypatch.setattr(judge, '_file_chunks', lambda repo, base, head, cfg, cf, kind, desc:
                        [judge.Chunk(cf.path, kind, cf.path, 1, 'diff')])
    changes = [gitops.ChangedFile('M', 'first.js'), gitops.ChangedFile('M', 'later.js')]
    class Jev:
        def ask(self, state, questions):
            if state == 'later.js': raise RewardGuardError('later confirmation unavailable')
            return {k: .9 for k in questions}
    errors, coverage = [], []
    findings, _ = judge.confirm(str(repo), base, head, cfg, changes, {'first.js':'source', 'later.js':'source'}, '',
                               Jev(), [], [Finding('TYPE_ESCAPE', 'warn', 'first', file='first.js'),
                                           Finding('TYPE_ESCAPE', 'warn', 'later', file='later.js')], [], errors, coverage)
    assert len(findings) == 1 and findings[0].file == 'first.js' and findings[0].probability == .9
    assert errors and any(r['status'] == 'error' for r in coverage)


def test_ci_required_completeness_returns_nonzero_with_no_fake_error(tmp_path):
    rep = Report(content={'status': 'reviewed', 'coverage': [{'status': 'not_evaluated', 'reason': 'required source absent'}]})
    args = argparse.Namespace(markdown=None, json=str(tmp_path/'report.json'), require_complete=True)
    assert cli._finish(rep, args) == 3
    data = json.loads((tmp_path/'report.json').read_text())
    assert data['status'] == 'incomplete' and data['errors'] == []


def test_incomplete_task_context_cannot_suppress_expected_value_grade(history, monkeypatch):
    repo, base, _, head = history
    cfg = config.parse('run_tests = false\n')
    monkeypatch.setattr(judge, 'build_chunks', lambda *a: [judge.Chunk('a.test.js', 'test', 'test', 1, 'diff')])
    calls = []
    class Jev:
        def ask(self, state, questions):
            calls.append(questions)
            return {key: .99 if key == 'justified' else .9 if key == 'expected_changed' else .1 for key in questions}
    class Haiku:
        def explain(self, state, statements, **kw): return {key: [] for key in statements}
    result = judge.run(str(repo), base, head, cfg, [], {'a.test.js':'test', 'code.js':'source'},
                       'partial task fragment', Jev(), Haiku(), task_context_complete=False)
    assert any(f.rule == 'EXPECTED_VALUE_CHANGED' and f.probability == .9 for f in result.findings)
    assert not any('justified' in q for q in calls)
    assert any(r.get('stage') == 'justification' and r['status'] == 'not_evaluated' for r in result.coverage)


def test_malformed_artifact_preserves_earlier_content_findings(history, monkeypatch, tmp_path):
    from types import SimpleNamespace
    from rewardguard import content_review, run_artifacts
    repo, base, _, head = history
    cfg = config.parse('run_tests = false\n')
    cfg.run_tests = True
    def resolve(repo, args):
        args.config_base = base
        return base, head, cfg
    monkeypatch.setattr(cli, '_resolve', resolve)
    finding = Finding('CG_TEST', 'fail', 'completed content finding', source='content', probability=.9)
    monkeypatch.setattr(content_review, 'review', lambda *a, **kw: SimpleNamespace(
        findings=[finding], notes=[], errors=[], to_dict=lambda: {'status':'reviewed', 'coverage':[]}))
    monkeypatch.setattr(cli.static_checks, 'run', lambda *a: ([], {}))
    monkeypatch.setattr(cli.judge, 'JevClient', lambda *a, **kw: SimpleNamespace(cache_hits=0, models_seen=[]))
    monkeypatch.setattr(cli.explainer, 'HaikuExplainer', lambda *a, **kw: object())
    monkeypatch.setattr(cli.judge, 'run', lambda *a, **kw: judge.JudgeResult())
    def invalid(*a):
        return run_artifacts.validate_results({'findings': [{'rule': [], 'severity': 'fail', 'source':'run', 'message':'malformed'}], 'errors': []}, {})
    monkeypatch.setattr(run_artifacts, 'load_authenticated', invalid)
    target = tmp_path/'retained.json'
    markdown = tmp_path/'retained.md'
    assert cli.main(['check', '--repo', str(repo), '--test-artifact', '--json', str(target), '--markdown', str(markdown)]) == 2
    data = json.loads(target.read_text())
    assert data['findings'][0]['probability'] == .9
    assert any('artifact' in e for e in data['errors'])
    assert 'completed content finding' in markdown.read_text()
