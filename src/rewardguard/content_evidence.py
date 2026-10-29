"""Bounded repository evidence, read exclusively from Git objects.

Evidence codes describe the supplied material, not universal readiness of every rule.
In particular, a file inventory is not a URL inventory and source is not a render.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import PurePosixPath

from . import judge


@dataclass
class EvidenceBundle:
    text: str = ''
    by_code: dict[str, list[str]] = field(default_factory=dict)
    available: set[str] = field(default_factory=set)
    provenance: list[dict] = field(default_factory=list)
    omissions: list[dict] = field(default_factory=list)
    source_observations: list[dict] = field(default_factory=list)
    # Compatibility metric for callers that report admitted evidence size.
    budgeted_characters: int = 0


# Even explicitly configured paths cannot opt credentials or private exports in.
_DENIED_PARTS = {
    '.git', 'node_modules', 'vendor', '.venv', 'venv', 'dist', 'build', 'coverage',
    '.next', '.nuxt', '.svelte-kit', '.astro', 'out', '.output', '__pycache__',
    '.aws', '.ssh', '.gnupg', 'secrets', 'credentials', 'private', 'backups',
    'exports', 'logs', 'test-results', '__snapshots__', 'generated', '.cache',
}


def _safe_path(path: str) -> bool:
    if not isinstance(path, str) or not path or '\\' in path or ':' in path:
        return False
    p = PurePosixPath(path)
    if p.is_absolute() or any(part in ('', '.', '..') for part in path.split('/')):
        return False
    if any(ord(c) < 32 or ord(c) == 127 for c in path):
        return False
    lower = [part.lower() for part in p.parts]
    if any(part in _DENIED_PARTS or part.startswith('.env') for part in lower):
        return False
    name = lower[-1]
    if (name.startswith('.env') or re.search(r'(?:secret|credential|private[-_]?key|'
            r'customer[-_]?export|user[-_]?export|database[-_]?dump)', name)
            or name.endswith(('.pem', '.key', '.p12', '.pfx', '.sqlite', '.db', '.log', '.csv', '.lock'))
            or '.min.' in name):
        return False
    return True


def _safe(text: str) -> str:
    # Apply line redaction before any excerpt so private-key block boundaries survive.
    lines, _ = judge._redact_lines(text.splitlines())
    text = '\n'.join(lines)
    return re.sub(r'([a-z][a-z0-9+.-]*://)[^\s/<>"\']*@', r'\1[credential redacted]@', text, flags=re.I)


def collect(repo, trusted_base, head, path, cfg, *, max_chars=18000,
            shared_artifact=None, deduplicate=True) -> EvidenceBundle:
    """Only explicitly bound trusted-base context; no automatic docs/import/history.

    Provenance retains real source coordinates outside model state. `by_code`
    contains self-contained evidence content without volatile Git/path labels.
    Public dependency reader units are resolved by the publication manifest.
    """
    from .content_publications import publication_for, safe_source, tree, read_blob
    bundle = EvidenceBundle()
    publication, reason = publication_for(path, cfg)
    if publication is None:
        bundle.omissions.append({'path': path, 'reason': reason})
        return bundle
    resolved, entries = tree(repo, trusted_base)
    remaining = max_chars
    for code in publication.evidence:
        paths = cfg.content.context.get(code, [])
        if not paths:
            bundle.omissions.append({'path': path, 'code': code, 'reason': 'Bound context code has no configured source'})
        for source in paths:
            reason = None
            text = None
            if not safe_source(source, cfg, evidence=True):
                reason = 'Required or configured evidence exclusion'
            elif source not in entries:
                reason = 'Bound evidence is absent from trusted base'
            else:
                text, reason = read_blob(repo, entries[source])
            if text is not None and not text.strip():
                reason = 'Bound evidence is empty'
                text = None
            if text is not None and len(text) > remaining:
                reason = 'Whole bound evidence exceeds remaining allowance'
                text = None
            if text is None:
                bundle.omissions.append({'path': source, 'code': code, 'reason': reason})
                continue
            remaining -= len(text)
            bundle.available.add(code)
            bundle.by_code.setdefault(code, []).append(text)
            bundle.provenance.append({'path': source, 'commit': resolved, 'role': 'configured_context',
                'codes': [code], 'scope': 'explicit_publication_binding', 'start_line': 1,
                'end_line': len(text.splitlines()), 'complete': True, 'trusted_policy': True,
                'independently_verified': False, 'claim_status': 'repository_assertion'})
    bundle.text = json.dumps(bundle.by_code, sort_keys=True, ensure_ascii=True)
    bundle.budgeted_characters = len(bundle.text)
    return bundle
