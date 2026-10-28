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

CACHE_MAX_AGE_SECONDS = 24 * 60 * 60


def _valid_timestamp(value):
    try:
        return type(value) in (int, float) and math.isfinite(value) and value >= 0
    except OverflowError:
        return False


def _clock():
    try:
        now = time.time()
    except Exception:
        return None
    if not _valid_timestamp(now):
        return None
    return now


class ReviewCache:
    def __init__(self, api_key, endpoint, epoch='v1'):
        if not isinstance(epoch, str) or not re.fullmatch(r'[A-Za-z0-9_.-]{1,64}', epoch):
            raise RewardGuardError('Jev cache epoch must be 1-64 letters, digits, dots, underscores or hyphens')
        root = os.environ.get('REWARDGUARD_CACHE_DIR')
        self.root = Path(root) if root else None
        self.key = api_key.encode()
        self.endpoint = endpoint
        self.epoch = epoch

    def identity(self, body):
        return hmac.new(self.key, b'rewardguard-cache-v2\0' + __version__.encode() + b'\0' + self.endpoint.encode() + b'\0' + self.epoch.encode() + b'\0' + body,
                        hashlib.sha256).hexdigest()

    def _signature(self, identity, created_at, payload):
        signed = json.dumps({'identity': identity, 'created_at': created_at, 'payload': payload},
                            sort_keys=True, separators=(',', ':')).encode()
        return hmac.new(self.key, signed, hashlib.sha256).hexdigest()

    def load(self, body):
        if self.root is None:
            return None
        identity = self.identity(body)
        try:
            record = json.loads((self.root / (identity + '.json')).read_text())
            payload = record['payload']
            created_at = record['created_at']
            if not _valid_timestamp(created_at):
                return None
            signature = self._signature(identity, created_at, payload)
            if not hmac.compare_digest(signature, record['signature']):
                logging.warning("RewardGuard ignored a cache entry with an invalid signature")
                return None
            now = _clock()
            if now is None or created_at > now or now - created_at >= CACHE_MAX_AGE_SECONDS:
                return None
            return json.loads(payload)
        except FileNotFoundError:
            return None
        except (OSError, ValueError, KeyError, TypeError):
            logging.warning("RewardGuard could not read or validate a cache entry; reviewing again")
            return None

    def save(self, body, data):
        if self.root is None:
            return
        created_at = _clock()
        if created_at is None:
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
        except OSError:
            logging.warning("RewardGuard could not save a cache entry; verdict unchanged")
        finally:
            if temporary:
                try:
                    Path(temporary).unlink(missing_ok=True)
                except OSError:
                    logging.warning("RewardGuard could not remove a temporary cache file")
