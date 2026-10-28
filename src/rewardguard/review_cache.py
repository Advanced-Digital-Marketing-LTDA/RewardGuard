"""Authenticated, input-addressed Jev results; never store source text or API keys."""
import hashlib
import hmac
import json
import logging
import math
import os
import re
import tempfile
import time
from pathlib import Path
from . import __version__
from .models import RewardGuardError

def _valid_timestamp(value):
    try:
        return type(value) in (int, float) and math.isfinite(value) and value >= 0
    except OverflowError:
        return False


def _clock(diagnostic=None):
    def note(reason):
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


class ReviewCache:
    def __init__(self, api_key, endpoint, epoch='v1', max_age_seconds=None):
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

    def identity(self, body):
        return hmac.new(self.key, b'rewardguard-cache-v2\0' + __version__.encode() + b'\0' + self.endpoint.encode() + b'\0' + self.epoch.encode() + b'\0' + body,
                        hashlib.sha256).hexdigest()

    def _signature(self, identity, created_at, payload):
        signed = json.dumps({'identity': identity, 'created_at': created_at, 'payload': payload},
                            sort_keys=True, separators=(',', ':')).encode()
        return hmac.new(self.key, signed, hashlib.sha256).hexdigest()

    def load(self, body, diagnostic=None):
        def note(reason):
            if diagnostic:
                diagnostic(reason)
        if self.root is None:
            note('disabled')
            return None
        identity = self.identity(body)
        try:
            record = json.loads((self.root / (identity + '.json')).read_text())
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
            note('hit')
            return result
        except FileNotFoundError:
            note('not_found_or_identity_changed')
            return None
        except OSError:
            note('read_failed')
            logging.warning("RewardGuard could not read or validate a cache entry; reviewing again")
            return None
        except (ValueError, KeyError, TypeError):
            note('malformed')
            logging.warning("RewardGuard could not read or validate a cache entry; reviewing again")
            return None

    def save(self, body, data, diagnostic=None):
        def note(reason):
            if diagnostic:
                diagnostic(reason)
        if self.root is None:
            note('disabled')
            return
        created_at = _clock(diagnostic=note)
        if created_at is None:
            note('clock_unavailable')
            return
        identity = self.identity(body)
        payload = json.dumps(data, sort_keys=True)
        record = {'payload': payload, 'created_at': created_at,
                  'signature': self._signature(identity, created_at, payload)}
        temporary = None
        try:
            self.root.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(mode='w', dir=self.root, delete=False) as stream:
                temporary = stream.name
                json.dump(record, stream)
            os.replace(temporary, self.root / (identity + '.json'))
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
