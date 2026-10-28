"""Offline tests for diagnostics emitted by the checked-in composite action."""
import os
import json
from pathlib import Path
import subprocess

import pytest
import yaml


@pytest.fixture
def steps():
    action = yaml.safe_load((Path(__file__).parents[1] / 'action.yml').read_text())
    return {step['name']: step for step in action['runs']['steps'] if 'name' in step}


def invoke(step, **extra):
    result = subprocess.run(['bash', '-euo', 'pipefail', '-c', step['run']],
                            env={**os.environ, **extra}, capture_output=True, text=True, check=True)
    return result.stdout


def test_diagnostic_steps_use_cache_outputs_and_never_change_review_verdict(steps):
    restore = steps['Restore authenticated Jev results']
    save = steps['Save authenticated Jev results']
    restore_report = steps['Report Jev archive restore']
    save_report = steps['Report Jev archive save']
    assert restore['id'] == 'jev_restore' and save['id'] == 'jev_save'
    assert restore['continue-on-error'] is True and save['continue-on-error'] is True
    for step in (restore_report, save_report):
        assert step['continue-on-error'] is True
        assert "always()" in step['if'] and "inputs.mode == 'check'" in step['if']
        assert 'secrets.' not in str(step.get('env', {}))
    assert restore_report['env']['CACHE_MATCHED'] == '${{ steps.jev_restore.outputs.cache-matched-key }}'
    assert restore_report['env']['CACHE_HIT'] == '${{ steps.jev_restore.outputs.cache-hit }}'
    assert restore_report['env']['CACHE_OUTCOME'] == '${{ steps.jev_restore.outcome }}'
    assert save_report['env']['CACHE_OUTCOME'] == '${{ steps.jev_save.outcome }}'
    assert restore['with']['key'] == save['with']['key'] == restore_report['env']['CACHE_REQUESTED']
    assert save_report['env']['CACHE_REQUESTED'] == save['with']['key']
    assert save_report['env']['CACHE_PREFIX'] == restore_report['env']['CACHE_PREFIX']
    assert restore['with']['restore-keys'].strip() == restore_report['env']['CACHE_PREFIX']
    assert steps['Run rewardguard']['env']['REWARDGUARD_EVENT_ACTION'] == '${{ github.event.action }}'
    assert steps['Run rewardguard']['env']['REWARDGUARD_ACTION_REVISION'] == '${{ github.action_ref }}'


@pytest.mark.parametrize('matched,hit,expected', [
    ('rewardguard-jev-v1-Linux-123-1', 'true', 'exact hit'),
    ('rewardguard-jev-v1-Linux-122-1', 'false', 'prefix hit'),
    ('rewardguard-jev-v1-Linux-122-1', '', 'restored; match type unavailable'),
])
def test_restore_hit_reports_archive_and_counts_regular_entry_files(steps, tmp_path, matched, hit, expected):
    (tmp_path / ('a' * 64 + '.json')).write_text('not read')
    (tmp_path / ('b' * 64 + '.json')).symlink_to(tmp_path / ('a' * 64 + '.json'))
    (tmp_path / 'other.txt').write_text('not read')
    out = invoke(steps['Report Jev archive restore'], CACHE_REQUESTED='rewardguard-jev-v1-Linux-123-1',
                 CACHE_PREFIX='rewardguard-jev-v1-Linux-', CACHE_MATCHED=matched, CACHE_HIT=hit,
                 CACHE_OUTCOME='success', CACHE_DIR=str(tmp_path))
    assert 'Jev archive requested key: rewardguard-jev-v1-Linux-123-1' in out
    assert 'Jev archive restore prefix: rewardguard-jev-v1-Linux-' in out
    assert 'Jev archive matched key: ' + matched in out
    assert 'Jev archive restore: ' + expected in out
    assert 'Jev archive restored entry files: 1 (not authenticated-result hits)' in out
    rows = [json.loads(line) for line in out.splitlines() if line.startswith('{')]
    assert rows == [{'kind': 'jev_archive_restore', 'requested_key': 'rewardguard-jev-v1-Linux-123-1',
                     'prefix': 'rewardguard-jev-v1-Linux-', 'matched_key': matched, 'outcome': 'success',
                     'status': expected, 'restored_count': 1, 'entry_count_error': None}]


def test_restore_count_failure_reports_safe_reason_without_path(steps, tmp_path):
    missing = tmp_path / 'sensitive-folder-name'
    out = invoke(steps['Report Jev archive restore'], CACHE_REQUESTED='rewardguard-jev-v1-Linux-123-1',
                 CACHE_PREFIX='rewardguard-jev-v1-Linux-', CACHE_MATCHED='rewardguard-jev-v1-Linux-123-1',
                 CACHE_HIT='true', CACHE_OUTCOME='success', CACHE_DIR=str(missing))
    assert 'Jev archive entry count failure: directory_missing' in out
    assert 'sensitive-folder-name' not in out
    row = json.loads(out.splitlines()[-1])
    assert row['entry_count_error'] == 'directory_missing' and row['restored_count'] is None


def test_restore_count_filesystem_error_does_not_expose_path(steps, tmp_path):
    not_a_directory = tmp_path / 'sensitive-file-name'
    not_a_directory.write_text('')
    out = invoke(steps['Report Jev archive restore'], CACHE_REQUESTED='rewardguard-jev-v1-Linux-123-1',
                 CACHE_PREFIX='rewardguard-jev-v1-Linux-', CACHE_MATCHED='rewardguard-jev-v1-Linux-123-1',
                 CACHE_HIT='true', CACHE_OUTCOME='success', CACHE_DIR=str(not_a_directory))
    assert 'sensitive-file-name' not in out
    row = json.loads(out.splitlines()[-1])
    assert row['entry_count_error'] == 'filesystem_error' and row['restored_count'] is None


def test_miss_and_failed_restore_do_not_claim_a_cache_hit(steps, tmp_path):
    common = dict(CACHE_REQUESTED='rewardguard-jev-v1-Linux-123-1', CACHE_PREFIX='rewardguard-jev-v1-Linux-',
                  CACHE_MATCHED='', CACHE_HIT='', CACHE_DIR=str(tmp_path))
    out = invoke(steps['Report Jev archive restore'], CACHE_OUTCOME='success', **common)
    assert 'Jev archive restore: miss (no matched key reported)' in out
    assert 'Jev archive restored entry files: unavailable' in out
    row = json.loads(out.splitlines()[-1])
    assert row['matched_key'] is None and row['restored_count'] is None
    assert row['status'] == 'miss (no matched key reported)' and row['outcome'] == 'success'
    out = invoke(steps['Report Jev archive restore'], CACHE_OUTCOME='failure', **common)
    assert 'Jev archive restore step outcome: failure' in out
    assert 'Jev archive restore: unavailable' in out
    row = json.loads(out.splitlines()[-1])
    assert row['matched_key'] is None and row['restored_count'] is None
    assert row['status'] == 'unavailable' and row['outcome'] == 'failure'


def test_untrusted_keys_cannot_inject_log_commands_and_save_status_is_not_confirmation(steps, tmp_path):
    out = invoke(steps['Report Jev archive restore'], CACHE_REQUESTED='rewardguard-jev-v1-Linux-123-1',
                 CACHE_PREFIX='rewardguard-jev-v1-Linux-', CACHE_MATCHED='::error::do-not-print',
                 CACHE_HIT='false', CACHE_OUTCOME='success', CACHE_DIR=str(tmp_path))
    assert '::error::do-not-print' not in out
    assert 'Jev archive matched key: unavailable' in out
    assert 'Jev archive restore: unavailable' in out
    row = json.loads(out.splitlines()[-1])
    assert row['matched_key'] is None and row['restored_count'] is None
    out = invoke(steps['Report Jev archive save'], CACHE_OUTCOME='success',
                 CACHE_REQUESTED='rewardguard-jev-v1-Linux-123-1', CACHE_PREFIX='rewardguard-jev-v1-Linux-')
    assert 'Jev archive save step outcome: success' in out
    assert 'Jev archive save confirmation: unavailable from action outputs' in out
    row = json.loads(out.splitlines()[-1])
    assert row == {'kind': 'jev_archive_save', 'requested_key': 'rewardguard-jev-v1-Linux-123-1',
                   'prefix': 'rewardguard-jev-v1-Linux-', 'matched_key': None, 'outcome': 'success',
                   'status': 'unavailable', 'restored_count': None}


def test_save_json_handles_unknown_values_without_disclosing_them(steps):
    out = invoke(steps['Report Jev archive save'], CACHE_OUTCOME='unexpected',
                 CACHE_REQUESTED='some-secret', CACHE_PREFIX='invalid-prefix')
    assert 'some-secret' not in out and 'invalid-prefix' not in out and 'unexpected' not in out
    row = json.loads(out.splitlines()[-1])
    assert row['outcome'] == 'unavailable' and row['status'] == 'unavailable'
    assert row['prefix'] is None and row['requested_key'] is None
