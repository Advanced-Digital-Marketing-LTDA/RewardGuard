"""Aggregate provider usage without retaining prompts or credentials."""
from threading import Lock
from copy import deepcopy
from .models import RewardGuardError


class UsageTracker:
    def __init__(self):
        self._lock = Lock()
        self._phases = {}
        self._limits = None
        self._attempts = 0
        self._request_bytes = 0

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
