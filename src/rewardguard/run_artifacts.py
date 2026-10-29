"""Verify test-result transport, not the honesty/effectiveness of branch tests."""
from __future__ import annotations
import hashlib
import io
import os
import re
import stat
import zipfile
from pathlib import Path
from .github import Client, strict_json
from .models import Finding, RewardGuardError

MAX_BYTES = 8 * 1024 * 1024
RUN_RULES = frozenset({'NO_TESTS_RAN', 'RUN_TEST_TOTAL_DROP', 'RUN_SKIPPED_INCREASE', 'NEW_FAILURES',
                       'PREEXISTING_FAILURES', 'ORIGINAL_TESTS_FAIL', 'NEW_TESTS_PASS_ON_BASE'})


def identity(base, head, policy):
    return {'schema_version': 1, 'base': base, 'head': head, 'policy': policy,
            'repository': os.environ.get('GITHUB_REPOSITORY', ''),
            'run_id': os.environ.get('GITHUB_RUN_ID', ''), 'run_attempt': os.environ.get('GITHUB_RUN_ATTEMPT', ''),
            'event': os.environ.get('GITHUB_EVENT_NAME', ''), 'event_sha': os.environ.get('GITHUB_SHA', '')}


def validate_results(data, expected):
    if not isinstance(data, dict):
        raise RewardGuardError('Run results must be an object')
    for key, value in expected.items():
        if data.get(key) != value:
            raise RewardGuardError(f'Run results are not for base/head snapshot ({key} mismatch)')
    allowed = {'schema_version', 'base', 'head', 'policy', 'repository', 'run_id', 'run_attempt', 'event', 'event_sha', 'findings', 'errors'}
    if set(data) - allowed:
        raise RewardGuardError('Unknown run-result fields')
    findings, errors = data.get('findings'), data.get('errors')
    if not isinstance(findings, list) or len(findings) > 10000 or not isinstance(errors, list) or len(errors) > 1000:
        raise RewardGuardError('Malformed run result lists')
    if not all(isinstance(e, str) and len(e) <= 100000 for e in errors):
        raise RewardGuardError('Malformed run errors')
    for f in findings:
        if not isinstance(f, dict) or not {'rule', 'severity', 'source', 'message'} <= set(f):
            raise RewardGuardError('Run results hold a malformed finding')
        if (not isinstance(f, dict) or set(f) - {'rule', 'severity', 'source', 'message', 'file', 'line', 'evidence'}
                or not isinstance(f.get('rule'), str) or f['rule'] not in RUN_RULES
                or not isinstance(f.get('severity'), str) or f['severity'] not in {'warn', 'fail'} or f.get('source') != 'run'
                or not isinstance(f.get('message'), str) or len(f['message']) > 100000):
            raise RewardGuardError('Run results hold an invalid finding schema/rule')
        for key in ('file', 'evidence'):
            if key in f and (not isinstance(f[key], str) or len(f[key]) > 100000):
                raise RewardGuardError('Invalid run finding text')
        if 'line' in f and (type(f['line']) is not int or not 1 <= f['line'] <= 100000000):
            raise RewardGuardError('Invalid run finding line')
    return [Finding(**f) for f in findings], errors


def decode_archive(raw, digest, expected):
    if len(raw) > MAX_BYTES or not isinstance(digest, str) or not re.fullmatch(r'sha256:[0-9a-f]{64}', digest):
        raise RewardGuardError('Missing/invalid artifact digest or archive size')
    if hashlib.sha256(raw).hexdigest() != digest[7:]:
        raise RewardGuardError('Artifact digest mismatch')
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            entries = archive.infolist()
            if len(entries) != 1:
                raise RewardGuardError('Artifact must contain exactly one result file')
            entry = entries[0]
            mode = entry.external_attr >> 16
            if (entry.filename != 'rewardguard-run.json' or entry.is_dir() or stat.S_ISLNK(mode)
                    or entry.flag_bits & 1 or entry.file_size > MAX_BYTES
                    or entry.compress_type not in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}):
                raise RewardGuardError('Unsafe artifact ZIP member')
            with archive.open(entry) as stream:
                raw_json = stream.read(MAX_BYTES + 1)
                if len(raw_json) > MAX_BYTES:
                    raise RewardGuardError('Artifact JSON size limit')
    except (zipfile.BadZipFile, RuntimeError, OSError) as error:
        raise RewardGuardError('Invalid artifact ZIP') from error
    data = strict_json(raw_json)
    validate_results(data, expected)
    return data


def load_local(path, base, head):
    with Path(path).open('rb') as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise RewardGuardError('Run results size limit')
    return validate_results(strict_json(raw), {'base': base, 'head': head})


def load_authenticated(base, head, policy, client=None):
    expected = identity(base, head, policy)
    for key in ('run_id', 'run_attempt'):
        if not re.fullmatch(r'[1-9][0-9]{0,19}', expected[key]):
            raise RewardGuardError('Authenticated test results require current GitHub run identity')
    if not re.fullmatch(r'[0-9a-f]{40}', expected['event_sha']):
        raise RewardGuardError('Missing GitHub event SHA')
    client = client or Client(expected['repository'])
    run = client.get('actions/runs/' + expected['run_id'])
    # PR run metadata may name the source head or GitHub's synthetic merge SHA.
    # Both are independently supplied by the immutable trusted event/snapshot.
    allowed_run_heads = {expected['event_sha']}
    if expected['event'] in {'pull_request', 'pull_request_target'}:
        allowed_run_heads.add(head)
    if (not isinstance(run, dict) or str(run.get('id')) != expected['run_id']
            or str(run.get('run_attempt')) != expected['run_attempt'] or run.get('event') != expected['event']
            or run.get('head_sha') not in allowed_run_heads
            or (run.get('repository') or {}).get('full_name') != expected['repository']):
        raise RewardGuardError('GitHub workflow run origin/event mismatch')
    name = f"rewardguard-run-{expected['run_id']}-{expected['run_attempt']}"
    artifacts = client.pages('actions/runs/' + expected['run_id'] + '/artifacts', 'artifacts')
    matches = [a for a in artifacts if a.get('name') == name]
    if len(matches) != 1:
        raise RewardGuardError('Expected exactly one same-run test artifact')
    artifact = matches[0]
    origin = artifact.get('workflow_run') or {}
    if (artifact.get('expired') is not False or type(artifact.get('id')) is not int
            or artifact['id'] <= 0 or str(origin.get('id')) != expected['run_id']
            or origin.get('head_sha') != run.get('head_sha')
            or type((run.get('repository') or {}).get('id')) is not int
            or type((run.get('head_repository') or {}).get('id')) is not int
            or origin.get('repository_id') != (run.get('repository') or {}).get('id')
            or origin.get('head_repository_id') != (run.get('head_repository') or {}).get('id')
            or type(artifact.get('size_in_bytes')) is not int or artifact['size_in_bytes'] > MAX_BYTES):
        raise RewardGuardError('Test artifact origin/size/expiration mismatch')
    data = decode_archive(client.archive(artifact['id'], MAX_BYTES), artifact.get('digest'), expected)
    return validate_results(data, expected)
