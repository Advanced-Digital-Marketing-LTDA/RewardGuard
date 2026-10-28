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

## Further offline analysis

In the same synthetic replay, 16 requests contained 287,464 state characters.
Four distinct states totalled 71,866 characters; 215,598 characters repeated
those states across stages. The 475-character routing boundary appeared in 240
questions (114,000 question characters). Moving that boundary into the state
once per request reduced simulated payload from 475,860 to 376,932 bytes, but
changes the per-question instruction contract. It is not implemented: offline
question and coverage parity cannot prove model adherence, independence or
injection resistance.

Increasing evaluation batches from 16 to 21 jobs saved nothing on this replay.
A hypothetical classification/routing fusion fit two of four synthetic states
and saved 30,241 bytes (6.36% of the optimized payload), but would also route
non-content changes and change request composition. Its quality and cost are
unverified, so it is not implemented. A synthetic all-packs stress case also
showed a 58,984-byte serialized request despite the existing nominal 56,000-byte
routing batch allowance; the estimate omits JSON wrapping and escaping. A future
change should measure actual serialized bodies and explicitly handle an oversized
individual question, with non-ASCII and escaping tests. This is an existing local
batching bound, not a demonstrated provider limit.

`python scripts/benchmark_cache_age.py` simulates 16 identical clean requests
every four hours for seven days, assuming every archive is restored. No age limit
requires 16 fresh requests and yields 656 hits; a 24-hour limit requires 112
fresh requests and yields 560 hits. This is a controlled reuse scenario, not a
production forecast. A mandatory 24-hour expiry is not necessary to invalidate
changed request bytes, model identifier, key or epoch. It only bounds exposure
to undisclosed provider changes under a stable model alias, which it cannot
detect, and can increase usage. Expiry is therefore optional; when no expiry is
set, maintainers must increment the model epoch for such changes.
