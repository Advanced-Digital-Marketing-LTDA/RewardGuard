"""Regressions from the complete RewardGuard report on PR 29, head eeed0c4."""
import io
import json
import logging
import os
from pathlib import Path
import subprocess
import pytest
import yaml
from rewardguard import content_syntax, content_publications, review_cache, content_checks, github


def test_stale_head_is_incomplete_and_never_a_green_required_check(tmp_path):
    action = yaml.safe_load((Path(__file__).parents[1] / 'action.yml').read_text())
    final = next(s for s in action['runs']['steps'] if s.get('id') == 'final_result')
    output = tmp_path / 'output'
    result = subprocess.run(['bash', '-euo', 'pipefail', '-c', final['run']], capture_output=True, text=True,
        env={**os.environ, 'GITHUB_OUTPUT': str(output), 'FRESHNESS':'stale', 'JUDGE_EXIT':'',
             'PUBLISH_OUTCOME':'skipped', 'PUBLISH_ENABLED':'true', 'EVIDENCE_OUTCOME':'skipped'})
    assert result.returncode == 3
    assert output.read_text().splitlines()[-1] == 'result=incomplete'


def test_mdx_omission_preserves_specific_reason_and_entire_region():
    text = 'export const x = 1; trailingUnknown\n\nPRIVATE IMPLEMENTATION\n'
    extracted, limits = content_syntax.omit_mdx_regions(text)
    assert not extracted.strip()
    assert limits == [{'line': 1, 'end_line': 3, 'status':'not_evaluated',
                       'reason':'Unsupported MDX ESM/expression region: Unexamined MDX ESM statement tail',
                       'omitted_to_end': True}]


def test_invalid_link_dependency_has_explicit_source_limitation():
    artifact = {'route':'/page', 'units':[{'kind':'link', 'text':'http://[', 'line':7}], 'limitations':[]}
    assert content_publications.referenced_routes(artifact) == set()
    assert artifact['limitations'] == [{'line':7, 'status':'not_evaluated',
                                       'reason':'Invalid literal URL; public route dependency could not be resolved'}]
    content_publications.referenced_routes(artifact)
    assert len(artifact['limitations']) == 1


def test_cache_raw_identity_fallback_is_visible_without_payload(caplog):
    cache = review_cache.ReviewCache('key', 'endpoint', repository='test/repo')
    with caplog.at_level(logging.WARNING):
        first = cache.identity(b'private-input-not-json')
    assert len(first) == 64
    assert 'raw-byte identity' in caplog.text
    assert 'private-input' not in caplog.text


@pytest.mark.parametrize('failure', ['exception', 'exit'])
def test_git_identity_lookup_failure_is_visible_without_paths(monkeypatch, caplog, tmp_path, failure):
    def run(*a, **kw):
        if failure == 'exception': raise OSError('private-token/path')
        return subprocess.CompletedProcess(a, 128, '', 'private-token/path')
    monkeypatch.setattr(review_cache.subprocess, 'run', run)
    with caplog.at_level(logging.WARNING):
        assert review_cache.repository_identity(tmp_path) == str(tmp_path.resolve())
    assert 'repository identity' in caplog.text
    assert 'private-token' not in caplog.text


@pytest.mark.parametrize('field,value', [('head','bad'), ('repo','../repo'), ('token','bad\nheader'), ('token','')])
def test_legacy_publisher_rejects_invalid_identity_before_http(monkeypatch, field, value):
    arguments = {'head':'a'*40, 'repo':'owner/repo', 'token':'valid-token'}
    arguments[field] = value
    monkeypatch.setenv('GH_TOKEN', arguments['token'])
    monkeypatch.setattr(github.urllib.request, 'build_opener', lambda *a: pytest.fail('invalid input reached HTTP client'))
    assert content_checks.main(['--preflight','--head',arguments['head'],'--repo',arguments['repo']]) == 2


def test_legacy_publisher_ignores_untrusted_api_endpoint(monkeypatch):
    monkeypatch.setenv('GH_TOKEN','valid-token')
    monkeypatch.setenv('GITHUB_API_URL','https://evil.invalid/leak')
    seen = []
    class Opener:
        def open(self, request, **kw):
            seen.append(request.full_url)
            return io.BytesIO(json.dumps({'head':{'sha':'a'*40}}).encode())
    monkeypatch.setattr(github.urllib.request, 'build_opener', lambda *a: Opener())
    assert content_checks.main(['--preflight','--head','a'*40,'--repo','owner/repo','--pr','29']) == 0
    assert seen == ['https://api.github.com/repos/owner/repo/pulls/29']
