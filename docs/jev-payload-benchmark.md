# Offline content payload benchmark

`scripts/benchmark_content_payload.py REPO BASE HEAD [DESCRIPTION_FILE]` compares
the previous evidence representation with self-contained references to identical
redacted text. Both runs use the same trusted-base configuration, selected files,
evidence admission limits and diff-chunk budgets. The script checks equality of
the question multiset, synthetic coverage, provenance and omissions before
printing JSON request-body byte counts. It does not contact Jev or Haiku.

The judge in this benchmark supplies fixed synthetic answers. Identical offline
coverage does not establish equal model probabilities, actual detection quality,
provider token counts, provider cache hits or billing. The comparison excludes
code review and network retries. Reproduce with local Git objects and, optionally,
a UTF-8 file containing the exact task context to compare:

```sh
python scripts/benchmark_content_payload.py /path/to/repository BASE_SHA HEAD_SHA /path/to/context.txt
```

On 28 October 2026, using AI-Comment-Moderation PR #25 base
`f171e856fbe6cbbad027ba8012db7c5c0990ccdb` and head
`2694b51a495d09495fdcc6b4d025b8db7f7fc6a5`, with the then-current PR
title and body, the offline fixture produced 17 baseline requests totaling
556,340 serialized JSON bytes and 16 optimized requests totaling 475,860 bytes:
80,480 bytes (14.47%) fewer. Synthetic answer routing differs from the actual
historical run, so this is not a reconstruction of its token use. The 50% goal
remains unmet; use measured stage data and adversarial review before further
changes to batching or evidence selection. Event-level deduplication requires a
separate design preserving current-head required checks and default-branch
coverage.
