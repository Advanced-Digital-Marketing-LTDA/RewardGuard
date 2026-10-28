"""Aggregate provider usage without retaining prompts or credentials."""
from threading import Lock
from copy import deepcopy
from .models import RewardGuardError

_CATEGORIES = {'request', 'result_cache_lookup', 'result_cache_validation', 'result_cache_write',
               'http_attempt', 'retry', 'response_validation', 'budget'}
_REASONS = {'started', 'disabled', 'invalid_timestamp', 'integrity_failure', 'clock_unavailable',
            'future_timestamp', 'expired', 'hit', 'not_found_or_identity_changed', 'read_failed',
            'malformed', 'invalid_response', 'saved', 'write_failed', 'cleanup_failed',
            'finding_not_cacheable', 'exhausted', 'response_received', 'retryable_http_error',
            'permanent_http_error', 'scheduled', 'transport_failure', 'invalid_json'}
_NUMBERS = {'state_characters', 'question_characters', 'question_count', 'request_bytes', 'attempt',
            'input_tokens_available', 'output_tokens_available', 'cached_input_tokens_available',
            'input_tokens', 'output_tokens', 'cached_input_tokens', 'http_status'}


class UsageTracker:
    def __init__(self):
        self._lock = Lock()
        self._phases = {}
        self._limits = None
        self._attempts = 0
        self._request_bytes = 0
        self._events = []
        self._events_dropped = 0
        self._request_id = 0

    def start_request(self, phase, stage, state, questions, request_bytes):
        with self._lock:
            self._request_id += 1
            request_id = self._request_id
        self.event(request_id, phase, stage, 'request', 'started',
                   state_characters=len(state), question_characters=sum(map(len, questions.values())),
                   question_count=len(questions), request_bytes=request_bytes)
        return request_id

    def event(self, request_id, phase, stage, category, reason, **numbers):
        # Only fixed internal labels and nonnegative integer counters belong in
        # diagnostics. Never retain request contents, credentials or hashes.
        row = {'request_id': request_id if type(request_id) is int and request_id >= 0 else 0,
               'phase': phase if phase in ('code', 'content') else 'other',
               'stage': stage if stage in ('classification', 'routing', 'applicability', 'evaluation') else 'other',
               'category': category if isinstance(category, str) and category in _CATEGORIES else 'other',
               'reason': reason if isinstance(reason, str) and reason in _REASONS else 'other'}
        row.update({k: v for k, v in numbers.items() if k in _NUMBERS and type(v) is int and v >= 0})
        with self._lock:
            if len(self._events) < 10000:
                self._events.append(row)
            else:
                self._events_dropped += 1

    def diagnostics(self):
        with self._lock:
            return {'events': deepcopy(self._events), 'events_dropped': self._events_dropped,
                    'provider_cached_tokens': 'unavailable unless explicitly reported on a response',
                    'provider_billed_tokens': 'unavailable'}

    def configure(self, max_attempts, max_request_bytes):
        """Bind one shared run to one set of limits before any provider calls."""
        limits = (max_attempts, max_request_bytes)
        if any(value is not None and (type(value) is not int or value <= 0) for value in limits):
            raise RewardGuardError('Jev request budgets must be positive integers')
        with self._lock:
            if self._limits is not None and self._limits != limits:
                raise RewardGuardError('Inconsistent Jev budgets in one review; review incomplete')
            self._limits = limits

    @staticmethod
    def _empty():
        return {'requests': 0, 'input_tokens': 0,
            'usage_missing': 0, 'state_characters': 0, 'question_characters': 0,
            'attempts': 0, 'request_bytes': 0, 'cache_hits': 0, 'budget_denials': 0}

    def _rows(self, phase, stage):
        aggregate = self._phases.setdefault(phase, self._empty())
        if stage is None:
            return (aggregate,)
        stages = aggregate.setdefault('stages', {})
        return aggregate, stages.setdefault(stage, self._empty())

    def cache_hit(self, phase, stage=None):
        with self._lock:
            for row in self._rows(phase, stage):
                row['cache_hits'] += 1

    def reserve(self, phase, request_bytes, stage=None):
        """Count each HTTP attempt before sending, including retries and failed calls."""
        with self._lock:
            rows = self._rows(phase, stage)
            max_attempts, max_bytes = self._limits or (None, None)
            reason = None
            if max_attempts is not None and self._attempts >= max_attempts:
                reason = f'judge.max_attempts ({max_attempts})'
            elif max_bytes is not None and self._request_bytes + request_bytes > max_bytes:
                reason = f'judge.max_request_bytes ({max_bytes})'
            if reason:
                for row in rows:
                    row['budget_denials'] += 1
                raise RewardGuardError(f'Jev request budget {reason} exhausted; review incomplete')
            self._attempts += 1
            self._request_bytes += request_bytes
            for row in rows:
                row['attempts'] += 1
                row['request_bytes'] += request_bytes

    def record(self, phase, state, questions, data, stage=None):
        usage = data.get('usage') if isinstance(data, dict) else None
        tokens = usage.get('input_tokens') if isinstance(usage, dict) else None
        valid = isinstance(tokens, int) and not isinstance(tokens, bool) and tokens >= 0
        with self._lock:
            for row in self._rows(phase, stage):
                row['requests'] += 1
                row['state_characters'] += len(state)
                row['question_characters'] += sum(map(len, questions.values()))
                if valid:
                    row['input_tokens'] += tokens
                else:
                    row['usage_missing'] += 1

    def snapshot(self):
        with self._lock:
            return deepcopy(self._phases)
