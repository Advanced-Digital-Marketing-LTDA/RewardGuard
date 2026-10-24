"""Resolve quoted PR task context without executing repository code."""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path
from dataclasses import dataclass

from . import gitops
from .models import RewardGuardError


@dataclass(frozen=True)
class TaskContext:
    text: str = ""
    scope_complete: bool = False
    full_pr_diff: bool = False

_MAX_BYTES = 8 * 1024 * 1024
_REPOSITORY = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+")
_COMMIT = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _get(repository: str, suffix: str):
    # The authentication header is sent only to the fixed hosted GitHub API.
    url = f"https://api.github.com/repos/{repository}/{suffix}"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "RewardGuard-PR-context"}
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.build_opener(_NoRedirect()).open(request, timeout=10) as response:
        raw = response.read(_MAX_BYTES + 1)
    if len(raw) > _MAX_BYTES:
        raise ValueError("GitHub PR context response exceeds its size limit")
    return json.loads(raw)


def _valid_pr(pr) -> bool:
    return (isinstance(pr, dict) and isinstance(pr.get("title", ""), str)
            and (pr.get("body") is None or isinstance(pr.get("body"), str)))


def _matches(pr, head: str) -> bool:
    if not _valid_pr(pr):
        return False
    pr_head = pr.get("head")
    head_sha = pr_head.get("sha") if isinstance(pr_head, dict) else None
    if pr.get("state") == "open":
        return head_sha == head
    return bool(pr.get("merged_at")) and (pr.get("merge_commit_sha") == head or head_sha == head)


def _text(title: str, body: str) -> str:
    title, body = title.strip(), body.strip()
    if title:
        return f"PR title: {title}\n\nPR description:\n{body or '(not provided)'}"
    return body


def _coverage(pr, repo: str | None, base: str | None, head: str | None,
              notes: list[str]) -> tuple[bool, bool]:
    pr_base = pr.get("base")
    pr_base_sha = pr_base.get("sha") if isinstance(pr_base, dict) else None
    if (not repo or not base or not head or not _COMMIT.fullmatch(head)
            or not isinstance(pr_base_sha, str) or not _COMMIT.fullmatch(pr_base_sha)):
        return False, False
    try:
        # GitHub's base SHA is the target tip, which can advance independently.
        # Compare the selected interval with the PR's actual merge-base interval.
        comparison_base = gitops.merge_base(repo, pr_base_sha, head)
        if base == comparison_base:
            return True, True
        # A contained incremental interval establishes task relevance, but omits
        # earlier PR work and cannot disprove claims about the complete PR.
        return gitops.merge_base(repo, comparison_base, base) == comparison_base, False
    except (OSError, RewardGuardError) as error:
        notes.append("PR interval coverage could not be established by Git "
                     f"({type(error).__name__}); intent-relative checks remain unverified.")
    return False, False


def resolve(args, *, repo: str | None = None, base: str | None = None,
            head: str | None = None, notes: list[str] | None = None) -> TaskContext:
    notes = notes if notes is not None else []
    explicit = getattr(args, "description", None)
    filename = getattr(args, "description_file", None)
    title = getattr(args, "title", None)
    if explicit or filename or title is not None:
        body = explicit or (Path(filename).read_text() if filename else "")
        notes.append("PR context: explicit CLI title/description.")
        return TaskContext(_text(title or "", body), True, True)

    # A local staged snapshot is not the commit named by an inherited CI event.
    if getattr(args, "staged", False):
        notes.append("PR context unavailable for this staged snapshot; supply --title/--description when known.")
        return TaskContext()
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        notes.append("PR context unavailable; no PR title or description was supplied.")
        return TaskContext()
    try:
        with Path(event_path).open("rb") as stream:
            raw = stream.read(_MAX_BYTES + 1)
        if len(raw) > _MAX_BYTES:
            raise ValueError("event exceeds its size limit")
        event = json.loads(raw)
        if not isinstance(event, dict):
            raise ValueError("invalid event")
    except (OSError, ValueError, UnicodeError):
        notes.append("PR context unavailable: GitHub event could not be read safely.")
        return TaskContext()

    repository = os.environ.get("GITHUB_REPOSITORY", "")
    valid_repository = bool(_REPOSITORY.fullmatch(repository)) and repository.split("/")[-1] not in {".", ".."}
    event_pr = event.get("pull_request")
    if _valid_pr(event_pr):
        # Preserve the event's revision-bound snapshot if its live PR has advanced.
        pr = event_pr
        number = pr.get("number")
        pr_head = pr.get("head")
        event_head = pr_head.get("sha") if isinstance(pr_head, dict) else None
        if head and event_head != head:
            notes.append("PR context unavailable: event PR does not match the reviewed head.")
            return TaskContext()
        if valid_repository and isinstance(number, int) and not isinstance(number, bool) and number > 0:
            try:
                live = _get(repository, f"pulls/{number}")
                if _valid_pr(live) and (not head or _matches(live, head)):
                    pr = live
                else:
                    notes.append("Live PR revision differs; using the reviewed event's title/description snapshot.")
            except (OSError, ValueError, UnicodeError):
                notes.append("Live PR metadata unavailable; using the event's title/description snapshot.")
        notes.append(f"PR context: GitHub PR #{number or '?'} title and description.")
        scope_complete, full_pr_diff = _coverage(pr, repo, base, head, notes)
        if not scope_complete:
            notes.append("The PR context does not establish the whole selected review range's scope.")
        elif not full_pr_diff:
            notes.append("The selected range is an incremental PR diff; whole-PR overclaim checks are unverified.")
        return TaskContext(_text(pr.get("title", ""), pr.get("body") or ""), scope_complete, full_pr_diff)

    # Push payloads have no pull_request object. Use an unambiguous association
    # matching the actual reviewed commit, never whichever PR happens to be first.
    if not valid_repository or not head or not _COMMIT.fullmatch(head):
        notes.append("PR context unavailable: no validated repository/head for PR association.")
        return TaskContext()
    try:
        prs = _get(repository, f"commits/{head}/pulls?per_page=100")
        if not isinstance(prs, list):
            raise ValueError("invalid PR association response")
        if len(prs) >= 100:
            notes.append("PR association coverage reached its limit; no unique association can be established.")
            return TaskContext()
        matches = [pr for pr in prs if _matches(pr, head)]
    except (OSError, ValueError, UnicodeError):
        notes.append("PR context unavailable: associated-PR lookup failed; intent-relative checks cannot infer scope.")
        return TaskContext()
    if len(matches) != 1:
        notes.append("PR context unavailable: no unique PR association matches the reviewed commit.")
        return TaskContext()
    pr = matches[0]
    notes.append(f"PR context: associated GitHub PR #{pr.get('number', '?')} title and description.")
    scope_complete, full_pr_diff = _coverage(pr, repo, base, head, notes)
    if not scope_complete:
        notes.append("Associated PR context may cover only part of this push; intent-relative scope/overclaim checks are unverified.")
    elif not full_pr_diff:
        notes.append("The push reviews only an incremental PR interval; whole-PR overclaim checks are unverified.")
    return TaskContext(_text(pr.get("title", ""), pr.get("body") or ""), scope_complete, full_pr_diff)
