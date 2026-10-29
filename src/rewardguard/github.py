"""Bounded hosted GitHub transport. Credentials never follow redirects."""
from __future__ import annotations
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from .models import RewardGuardError

MAX_JSON = 16 * 1024 * 1024


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def strict_json(raw):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError('duplicate JSON key')
            out[key] = value
        return out
    def invalid(value):
        raise ValueError('nonfinite JSON value')
    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)
    except (ValueError, UnicodeError, RecursionError) as error:
        raise RewardGuardError('Invalid bounded JSON document') from error


def bounded_read(response, limit=MAX_JSON):
    raw = response.read(limit + 1)
    if len(raw) > limit:
        raise RewardGuardError('Response exceeds size limit')
    return raw


class Client:
    def __init__(self, repository, token=None, opener=None):
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository) or any(x in {'.', '..'} for x in repository.split('/')):
            raise RewardGuardError('Invalid GitHub repository')
        self.repository = repository
        self.token = token if token is not None else os.environ.get('GH_TOKEN', os.environ.get('GITHUB_TOKEN', ''))
        if not self.token or any(ord(c) < 33 or ord(c) > 126 for c in self.token):
            raise RewardGuardError('GitHub token is missing or invalid')
        self.opener = opener or urllib.request.build_opener(NoRedirect())

    def request(self, suffix, method='GET', data=None):
        if suffix.startswith('/') or '..' in suffix or '\\' in suffix or '#' in suffix:
            raise RewardGuardError('Invalid GitHub API path')
        req = urllib.request.Request('https://api.github.com/repos/' + self.repository + '/' + suffix,
            method=method, data=None if data is None else json.dumps(data, allow_nan=False).encode(),
            headers={'Authorization': 'Bearer ' + self.token, 'Accept': 'application/vnd.github+json',
                     'Content-Type': 'application/json', 'X-GitHub-Api-Version': '2022-11-28',
                     'User-Agent': 'RewardGuard'})
        return self.opener.open(req, timeout=30)

    def get(self, suffix):
        with self.request(suffix) as response:
            return strict_json(bounded_read(response))

    def write(self, suffix, data, method='POST'):
        with self.request(suffix, method, data) as response:
            raw = bounded_read(response)
            return strict_json(raw) if raw else None

    def pages(self, suffix, field=None):
        rows = []
        separator = '&' if '?' in suffix else '?'
        for page in range(1, 101):
            data = self.get(f'{suffix}{separator}per_page=100&page={page}')
            batch = data.get(field) if field and isinstance(data, dict) else data
            if not isinstance(batch, list) or not all(isinstance(r, dict) for r in batch):
                raise RewardGuardError('Malformed GitHub collection')
            rows.extend(batch)
            if len(batch) < 100:
                return rows
        raise RewardGuardError('GitHub pagination limit; complete association unavailable')

    def archive(self, artifact_id, limit):
        # Redirect is authenticated by the fixed API, but storage is a fresh unauthenticated request.
        try:
            with self.request(f'actions/artifacts/{artifact_id}/zip') as response:
                return bounded_read(response, limit)
        except urllib.error.HTTPError as error:
            if error.code != 302:
                raise
            location = error.headers.get('Location', '')
            error.close()
        parsed = urllib.parse.urlsplit(location)
        host = parsed.hostname or ''
        if (parsed.scheme != 'https' or parsed.username or parsed.password or parsed.fragment
                or parsed.port not in (None, 443)
                or not (host.endswith('.blob.core.windows.net') or host.endswith('.actions.githubusercontent.com'))):
            raise RewardGuardError('Unsupported GitHub artifact storage redirect')
        request = urllib.request.Request(location, headers={'User-Agent': 'RewardGuard-artifact'})
        # New opener also refuses second redirects; no API Authorization or cookies copied.
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=30) as response:
            return bounded_read(response, limit)
