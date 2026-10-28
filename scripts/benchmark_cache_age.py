#!/usr/bin/env python3
"""Simulate identical clean-result reuse without provider calls or real source."""
import json
import os
import tempfile
from unittest.mock import patch

from rewardguard.review_cache import ReviewCache


def simulate(max_age_seconds):
    now = [100_000.0]
    with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {'REWARDGUARD_CACHE_DIR': directory}), \
            patch('rewardguard.review_cache._clock', side_effect=lambda **_: now[0]):
        cache = ReviewCache('synthetic-key', 'https://synthetic.invalid', max_age_seconds=max_age_seconds)
        requests, hits = 0, 0
        for run in range(42):  # Every four hours for seven days.
            for index in range(16):
                body = json.dumps({'synthetic_request': index}).encode()
                if cache.load(body) is None:
                    requests += 1
                    cache.save(body, {'answers': {'synthetic': .01}})
                else:
                    hits += 1
            now[0] += 4 * 60 * 60
    return {'fresh_requests': requests, 'cache_hits': hits}


if __name__ == '__main__':
    print(json.dumps({'unlimited_age': simulate(None), 'age_24h': simulate(86400),
                      'assumptions': '16 identical clean keys, 42 runs every four hours, successful archive restore',
                      'limitation': 'Synthetic cache simulation; not observed provider usage or billing.'}, indent=2))
