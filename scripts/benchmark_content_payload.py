#!/usr/bin/env python3
"""Compare old and deduplicated content payloads with deterministic offline answers.

Usage: python scripts/benchmark_content_payload.py REPO BASE HEAD [--description-stdin]
This does not contact any provider or establish semantic model parity.
"""
import json
import sys
from collections import Counter

from rewardguard import config, content_evidence, content_review, gitops

MAX_DESCRIPTION_BYTES = 256_000


def read_description(stream):
    """Read only explicitly supplied bounded input, never an arbitrary pathname."""
    data = stream.read(MAX_DESCRIPTION_BYTES + 1)
    if len(data) > MAX_DESCRIPTION_BYTES:
        raise SystemExit('Description input exceeds 256000 bytes')
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        raise SystemExit('Description input must be UTF-8') from None


class OfflineJudge:
    def __init__(self):
        self.calls = []

    def ask(self, state, questions):
        self.calls.append((state, questions))
        # Stable independent answers exercise routing, evidence readiness and
        # proposition grading without pretending to simulate model judgments.
        return {key: (.9 if key == 'content_task' or key == 'pack_writing' or
                      key.startswith(('applies_', 'ready_')) else .01) for key in questions}


def exercise(repo, base, head, description, deduplicate):
    cfg = config.load_from_commit(repo, base, allow_missing=True)
    client = OfflineJudge()
    original = content_evidence.collect

    def collect(*args, **kwargs):
        kwargs['deduplicate'] = deduplicate
        return original(*args, **kwargs)

    content_evidence.collect = collect
    try:
        result = content_review.review(repo, base, head, cfg, gitops.changed_files(repo, base, head),
                                       description, client=client, log=lambda _: None)
    finally:
        content_evidence.collect = original
    totals = {'requests': len(client.calls), 'state_characters': 0,
              'question_characters': 0, 'serialized_body_bytes': 0}
    for state, questions in client.calls:
        totals['state_characters'] += len(state)
        totals['question_characters'] += sum(len(q) for q in questions.values())
        body = {'model': cfg.model, 'state': state,
                'questions': {key: {'type': 'noul', 'instructions': value} for key, value in questions.items()}}
        totals['serialized_body_bytes'] += len(json.dumps(body).encode())
    totals['distinct_states'] = len({state for state, _ in client.calls})
    totals['distinct_state_characters'] = sum(map(len, {state for state, _ in client.calls}))
    totals['routing_boundary_occurrences'] = sum(question.count(content_review.ROUTING_BOUNDARY)
                                                  for _, questions in client.calls for question in questions.values())
    totals['routing_boundary_characters'] = totals['routing_boundary_occurrences'] * len(content_review.ROUTING_BOUNDARY)
    questions = Counter((key, question) for _, batch in client.calls for key, question in batch.items())
    return totals, result.to_dict(), questions


def main():
    if len(sys.argv) not in (4, 5) or (len(sys.argv) == 5 and sys.argv[4] != '--description-stdin'):
        raise SystemExit(__doc__)
    repo, base, head = sys.argv[1:4]
    description = read_description(sys.stdin.buffer) if len(sys.argv) == 5 else ''
    before, old_result, old_questions = exercise(repo, base, head, description, False)
    after, new_result, new_questions = exercise(repo, base, head, description, True)
    if old_result != new_result or old_questions != new_questions:
        raise SystemExit('Offline questions, coverage, omissions or provenance changed; investigate before interpreting savings.')
    saved = before['serialized_body_bytes'] - after['serialized_body_bytes']
    print(json.dumps({'baseline': before, 'deduplicated': after, 'bytes_saved': saved,
                      'bytes_saved_percent': round(100 * saved / before['serialized_body_bytes'], 2)
                      if before['serialized_body_bytes'] else 0,
                      'offline_coverage_provenance_omissions_equal': True,
                      'offline_questions_equal': True,
                      'limitation': 'Synthetic answers only; not provider tokens, cost or model-quality parity.'}, indent=2))


if __name__ == '__main__':
    main()
