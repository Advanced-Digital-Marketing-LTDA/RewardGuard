"""Small glob matcher supporting **, *, ? and {a,b} against forward-slash paths."""
from __future__ import annotations

import re
from functools import lru_cache


def _expand_braces(pattern: str) -> list[str]:
    m = re.search(r"\{([^{}]*)\}", pattern)
    if not m:
        return [pattern]
    out: list[str] = []
    for alt in m.group(1).split(","):
        out.extend(_expand_braces(pattern[: m.start()] + alt + pattern[m.end():]))
    return out


def _to_regex(pattern: str) -> str:
    i, res = 0, ""
    while i < len(pattern):
        c = pattern[i]
        if pattern.startswith("**/", i):
            res += "(?:.*/)?"
            i += 3
        elif pattern.startswith("**", i):
            res += ".*"
            i += 2
        elif c == "*":
            res += "[^/]*"
            i += 1
        elif c == "?":
            res += "[^/]"
            i += 1
        else:
            res += re.escape(c)
            i += 1
    return res


@lru_cache(maxsize=1024)
def _compiled(pattern: str) -> re.Pattern[str]:
    parts = [_to_regex(p) for p in _expand_braces(pattern)]
    return re.compile("^(?:" + "|".join(parts) + ")$")


def match(path: str, patterns: list[str] | tuple[str, ...]) -> bool:
    path = path.replace("\\", "/")
    return any(_compiled(p).match(path) for p in patterns)
