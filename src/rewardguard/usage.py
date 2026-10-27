"""Aggregate provider usage without retaining prompts or credentials."""
from threading import Lock


class UsageTracker:
    def __init__(self):
        self._lock = Lock()
        self._phases = {}

    def record(self, phase, state, questions, data):
        usage = data.get('usage') if isinstance(data, dict) else None
        tokens = usage.get('input_tokens') if isinstance(usage, dict) else None
        valid = isinstance(tokens, int) and not isinstance(tokens, bool) and tokens >= 0
        with self._lock:
            row = self._phases.setdefault(phase, {'requests': 0, 'input_tokens': 0,
                'usage_missing': 0, 'state_characters': 0, 'question_characters': 0})
            row['requests'] += 1
            row['state_characters'] += len(state)
            row['question_characters'] += sum(map(len, questions.values()))
            if valid:
                row['input_tokens'] += tokens
            else:
                row['usage_missing'] += 1

    def snapshot(self):
        with self._lock:
            return {phase: dict(row) for phase, row in self._phases.items()}
