"""Authenticated, input-addressed Jev results; never store source text or API keys."""
import hashlib
import hmac
import json
import os
import tempfile
from pathlib import Path
from . import __version__


class ReviewCache:
    def __init__(self, api_key, endpoint):
        root = os.environ.get('REWARDGUARD_CACHE_DIR')
        self.root = Path(root) if root else None
        self.key = api_key.encode()
        self.endpoint = endpoint

    def identity(self, body):
        return hmac.new(self.key, b'rewardguard-cache-v1\0' + __version__.encode() + b'\0' + self.endpoint.encode() + b'\0' + body,
                        hashlib.sha256).hexdigest()

    def load(self, body):
        if self.root is None:
            return None
        identity = self.identity(body)
        try:
            record = json.loads((self.root / (identity + '.json')).read_text())
            payload = record['payload']
            signature = hmac.new(self.key, (identity + payload).encode(), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(signature, record['signature']):
                return None
            return json.loads(payload)
        except (OSError, ValueError, KeyError, TypeError):
            return None

    def save(self, body, data):
        if self.root is None:
            return
        identity = self.identity(body)
        payload = json.dumps(data, sort_keys=True)
        record = {'payload': payload, 'signature': hmac.new(
            self.key, (identity + payload).encode(), hashlib.sha256).hexdigest()}
        temporary = None
        try:
            self.root.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(mode='w', dir=self.root, delete=False) as stream:
                temporary = stream.name
                json.dump(record, stream)
            os.replace(temporary, self.root / (identity + '.json'))
        except OSError:
            pass  # Cache availability never changes the verdict.
        finally:
            if temporary:
                try:
                    Path(temporary).unlink(missing_ok=True)
                except OSError:
                    pass
