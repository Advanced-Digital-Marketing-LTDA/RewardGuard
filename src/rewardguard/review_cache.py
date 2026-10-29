"""Authenticated, input-addressed Jev results; never store source text or API keys."""
import hashlib
import hmac
import json
import logging
import math
import os
import re
import sys
import tempfile
import time
from pathlib import Path
import subprocess
from threading import Lock
from contextlib import contextmanager
from copy import deepcopy
from .models import RewardGuardError

def _valid_timestamp(value):
    try:
        return type(value) in (int, float) and math.isfinite(value) and value >= 0
    except OverflowError:
        return False


def _clock(diagnostic=None):
    def note(reason):
        # logging.LogRecord reads time.time(), which may be the failing clock.
        try:
            sys.stderr.write("RewardGuard cache clock unavailable; reviewing again\n")
        except (OSError, ValueError):
            if diagnostic:
                diagnostic('clock_warning_write_failed')
        if diagnostic:
            diagnostic(reason)
    try:
        now = time.time()
    except OSError:
        note('clock_system_error')
        return None
    except (OverflowError, ValueError):
        note('clock_invalid_value')
        return None
    except Exception:
        # Cache failure must fall back to a fresh review. Never log exception
        # text: runtime errors can contain paths or other sensitive values.
        note('clock_unexpected_error')
        return None
    if not _valid_timestamp(now):
        note('clock_invalid_value')
        return None
    return now


def repository_identity(repo=None):
    repository = os.environ.get('GITHUB_REPOSITORY')
    if repository and repo is None:
        return repository.strip().lower().removesuffix('.git')
    try:
        remote = subprocess.run(['git', '-C', str(repo or Path.cwd()), 'config', '--get', 'remote.origin.url'],
                                capture_output=True, text=True, timeout=5, check=False).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        remote = ''
    remote = re.sub(r'^git@([^:]+):', r'https://\1/', remote)
    remote = re.sub(r'^https?://(?:[^/@]+@)?', '', remote)
    return remote.lower().rstrip('/').removesuffix('.git') or str(Path(repo or Path.cwd()).resolve())


class ReviewCache:
    def __init__(self, api_key, endpoint, epoch='v1', max_age_seconds=None, *, namespace='default', repository=None):
        if not isinstance(epoch, str) or not re.fullmatch(r'[A-Za-z0-9_.-]{1,64}', epoch):
            raise RewardGuardError('Jev cache epoch must be 1-64 letters, digits, dots, underscores or hyphens')
        if max_age_seconds is not None and (type(max_age_seconds) is not int or max_age_seconds <= 0):
            raise RewardGuardError('Jev cache maximum age must be a positive integer')
        root = os.environ.get('REWARDGUARD_CACHE_DIR')
        self.root = Path(root) if root else None
        self.key = api_key.encode()
        self.endpoint = endpoint
        self.epoch = epoch
        self.max_age_seconds = max_age_seconds
        self.namespace = namespace
        self.repository = repository if repository is not None else repository_identity()
        self._guard = Lock()
        self._locks = {}
        self._memory = {}
        self._rejected = set()

    @contextmanager
    def coordinate(self, body):
        identity = self.identity(body)
        with self._guard:
            lock = self._locks.setdefault(identity, Lock())
        with lock:
            yield


    def identity(self, body):
        try:
            body = json.dumps(json.loads(body), sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
        except (ValueError, TypeError, UnicodeDecodeError):
            pass
        identity = json.dumps({'format': 3, 'revision': 'results-1', 'endpoint': self.endpoint,
                               'repository': self.repository, 'scope': self.namespace,
                               'epoch': self.epoch}, sort_keys=True, separators=(',', ':')).encode()
        return hmac.new(self.key, identity + b'\0' + body, hashlib.sha256).hexdigest()

    def _signature(self, identity, created_at, payload):
        signed = json.dumps({'identity': identity, 'created_at': created_at, 'payload': payload},
                            sort_keys=True, separators=(',', ':')).encode()
        return hmac.new(self.key, signed, hashlib.sha256).hexdigest()

    def _metadata(self, note):
        # Advisory only: restored/missing metadata never authorizes a result.
        scope = json.dumps([self.repository, self.namespace], separators=(',', ':')).encode()
        path = self.root / ('.key-' + hashlib.sha256(scope).hexdigest())
        key_id = hmac.new(self.key, b'rewardguard-signing-key-id', hashlib.sha256).hexdigest()
        temporary = None
        try:
            try:
                previous = path.read_text() if path.exists() else None
            except UnicodeError:
                note('metadata_invalid')
                previous = None
            if previous is not None and previous != key_id:
                note('signing_key_changed')
            if previous != key_id:
                self.root.mkdir(parents=True, exist_ok=True)
                with tempfile.NamedTemporaryFile(mode='w', dir=self.root, delete=False) as stream:
                    temporary = stream.name
                    stream.write(key_id)
                os.replace(temporary, path)
        except OSError:
            note('metadata_unavailable')
        finally:
            if temporary:
                try:
                    Path(temporary).unlink(missing_ok=True)
                except OSError:
                    note('cleanup_failed')

    def reject(self, body):
        identity = self.identity(body)
        self._rejected.add(identity)
        self._memory.pop(identity, None)

    def _local(self, body, note):
        entry = self._memory.get(self.identity(body))
        if entry is None:
            return None
        created_at, result = entry
        now = _clock(diagnostic=note)
        if now is None or created_at > now:
            return None
        if self.max_age_seconds is not None and now - created_at >= self.max_age_seconds:
            note('expired')
            return None
        note('local_reuse')
        return deepcopy(result)

    def load(self, body, diagnostic=None):
        def note(reason):
            if diagnostic:
                diagnostic(reason)
        if self.root is None:
            note('disabled')
            return self._local(body, note)
        self._metadata(note)
        identity = self.identity(body)
        try:
            record = json.loads((self.root / (identity + '.json')).read_text())
            if not isinstance(record, dict):
                note('malformed')
                return None
            if record.get('format') != 3:
                note('format_changed')
                return None
            payload = record['payload']
            created_at = record['created_at']
            if not _valid_timestamp(created_at):
                note('invalid_timestamp')
                return None
            signature = self._signature(identity, created_at, payload)
            if not hmac.compare_digest(signature, record['signature']):
                logging.warning("RewardGuard ignored a cache entry with an invalid signature")
                note('integrity_failure')
                return None
            now = _clock(diagnostic=note)
            if now is None:
                note('clock_unavailable')
                return None
            if created_at > now:
                note('future_timestamp')
                return None
            if self.max_age_seconds is not None and now - created_at >= self.max_age_seconds:
                note('expired')
                return None
            result = json.loads(payload)
            self._memory[identity] = (created_at, deepcopy(result))
            note('hit')
            return result
        except FileNotFoundError:
            note('not_found_or_identity_changed')
            return None
        except OSError:
            note('read_failed')
            logging.warning("RewardGuard could not read or validate a cache entry; reviewing again")
            return self._local(body, note)
        except (ValueError, KeyError, TypeError):
            note('malformed')
            logging.warning("RewardGuard could not read or validate a cache entry; reviewing again")
            return None

    def save(self, body, data, diagnostic=None):
        def note(reason):
            if diagnostic:
                diagnostic(reason)
        identity = self.identity(body)
        if identity not in self._rejected and self.root is not None and self.load(body) is not None:
            note('immutable_existing')
            return
        created_at = _clock(diagnostic=note)
        if created_at is None:
            note('clock_unavailable')
            return
        self._memory[identity] = (created_at, deepcopy(data))
        if self.root is None:
            note('disabled')
            self._rejected.discard(identity)
            return
        payload = json.dumps(data, sort_keys=True)
        record = {'format': 3, 'payload': payload, 'created_at': created_at,
                  'signature': self._signature(identity, created_at, payload)}
        temporary = None
        try:
            self.root.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(mode='w', dir=self.root, delete=False) as stream:
                temporary = stream.name
                json.dump(record, stream)
            os.replace(temporary, self.root / (identity + '.json'))
            self._rejected.discard(identity)
            note('saved')
        except OSError:
            note('write_failed')
            logging.warning("RewardGuard could not save a cache entry; verdict unchanged")
        finally:
            if temporary:
                try:
                    Path(temporary).unlink(missing_ok=True)
                except OSError:
                    note('cleanup_failed')
                    logging.warning("RewardGuard could not remove a temporary cache file")
