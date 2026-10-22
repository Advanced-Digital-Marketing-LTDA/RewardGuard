"""The one exception to CHECKER_CONFIG_CHANGED: a trusted person approved this exact commit.

CI workflows and the rewardguard config sometimes have to change. Such a PR passes only when a
person named in the base branch's CODEOWNERS (individual @users; teams can't be resolved without
extra token scopes, so they don't count) has an approving review on the current head commit, and
that person is not the PR's author. The trusted list is read from the base commit with git, so a
branch can't add itself to it, and a new push makes earlier approvals stale.

Fails closed: any GitHub API error stops the check."""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.request

from . import gitops
from .models import RewardGuardError

# Own handle, so tests can fake GitHub separately from the Jev HTTP client
_urlopen = urllib.request.urlopen

# GitHub's own lookup order for CODEOWNERS
CODEOWNERS_PATHS = (".github/CODEOWNERS", "CODEOWNERS", "docs/CODEOWNERS")
_USER = re.compile(r"^@([A-Za-z0-9](?:[A-Za-z0-9-]{0,38}))$")


def code_owners(repo: str, base: str) -> set[str]:
    """Lower-cased individual users named anywhere in the base commit's CODEOWNERS."""
    for path in CODEOWNERS_PATHS:
        text = gitops.show_file(repo, base, path)
        if text is None:
            continue
        owners = set()
        for line in text.splitlines():
            line = line.split("#", 1)[0].strip()
            for token in line.split()[1:]:
                m = _USER.match(token)
                if m:
                    owners.add(m.group(1).lower())
        return owners
    return set()


class GitHubReviews:
    def __init__(self, api_url: str, repository: str, token: str, opener=None):
        self.base = f"{api_url.rstrip('/')}/repos/{repository}"
        self.token = token
        self.opener = opener or _urlopen

    def _get(self, path: str):
        req = urllib.request.Request(self.base + path, headers={
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })
        try:
            with self.opener(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            raise RewardGuardError(f"GitHub API returned HTTP {e.code} for {path}") from e
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            raise RewardGuardError(f"GitHub API request failed for {path}: {e}") from e

    def reviews(self, pr_number: int) -> list[dict]:
        out, page = [], 1
        while True:
            batch = self._get(f"/pulls/{pr_number}/reviews?per_page=100&page={page}")
            if not isinstance(batch, list):
                raise RewardGuardError(f"GitHub API returned an unexpected reviews payload: {str(batch)[:200]}")
            out.extend(batch)
            if len(batch) < 100:
                return out
            page += 1


def trusted_approvers(reviews: list[dict], owners: set[str], author: str, head_sha: str) -> list[str]:
    """Owners (not the author, not bots) whose latest decisive review approves head_sha."""
    latest: dict[str, dict] = {}
    for r in reviews:  # chronological; a later approve / request-changes / dismissal replaces an earlier one
        if r.get("state") in ("APPROVED", "CHANGES_REQUESTED", "DISMISSED"):
            latest[(r.get("user") or {}).get("login", "").lower()] = r
    return sorted(
        login for login, r in latest.items()
        if r["state"] == "APPROVED"
        and r.get("commit_id") == head_sha
        and (r.get("user") or {}).get("type") == "User"
        and login in owners
        and login != author.lower()
    )
