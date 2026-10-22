from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field

from .models import RewardGuardError


def git(repo: str, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    # errors="replace": binary or non-UTF-8 files (images, fixtures) must not crash the check
    proc = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, errors="replace")
    if check and proc.returncode != 0:
        raise RewardGuardError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc


def rev_parse(repo: str, rev: str) -> str:
    return git(repo, "rev-parse", "--verify", f"{rev}^{{commit}}").stdout.strip()


def merge_base(repo: str, a: str, b: str) -> str:
    return git(repo, "merge-base", a, b).stdout.strip()


def default_base(repo: str, fallback: str) -> str:
    """Find a local default-branch ref for trusted policy; fall back to the current base."""
    remote_head = git(repo, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD", check=False)
    refs = [remote_head.stdout.strip()] if remote_head.returncode == 0 else []
    refs.extend([
        "refs/remotes/origin/main", "refs/remotes/origin/master",
        "refs/heads/main", "refs/heads/master",
    ])
    for ref in dict.fromkeys(refs):
        commit = git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}", check=False)
        if commit.returncode == 0:
            return commit.stdout.strip()
    return rev_parse(repo, fallback)


def _commit_tree(repo: str, tree: str, parent: str | None, message: str) -> str:
    command = [
        "git", "-C", repo,
        "-c", "user.name=RewardGuard",
        "-c", "user.email=rewardguard@localhost",
        "commit-tree", tree,
    ]
    if parent:
        command.extend(["-p", parent])
    command.extend(["-m", message])
    proc = subprocess.run(command, capture_output=True, text=True, errors="replace")
    if proc.returncode != 0:
        raise RewardGuardError(f"git commit-tree failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def staged_snapshot(repo: str) -> tuple[str, str]:
    """Return (base, staged snapshot) without moving refs or changing the index/worktree."""
    head = git(repo, "rev-parse", "--verify", "HEAD^{commit}", check=False)
    if head.returncode == 0:
        base = head.stdout.strip()
    else:
        empty = subprocess.run(
            ["git", "-C", repo, "mktree"],
            input="", capture_output=True, text=True, errors="replace",
        )
        if empty.returncode != 0:
            raise RewardGuardError(f"Cannot create empty Git tree: {empty.stderr.strip()}")
        base = _commit_tree(repo, empty.stdout.strip(), None, "RewardGuard empty baseline")

    staged_tree = git(repo, "write-tree").stdout.strip()
    base_tree = git(repo, "rev-parse", f"{base}^{{tree}}").stdout.strip()
    if staged_tree == base_tree:
        return base, base
    return base, _commit_tree(repo, staged_tree, base, "RewardGuard staged snapshot")


def is_dirty(repo: str) -> bool:
    return bool(git(repo, "status", "--porcelain", "--untracked-files=no").stdout.strip())


def show_file(repo: str, commit: str, path: str) -> str | None:
    proc = git(repo, "show", f"{commit}:{path}", check=False)
    return proc.stdout if proc.returncode == 0 else None


def show_bytes(repo: str, commit: str, path: str) -> bytes:
    """Exact file contents, for copying files into a worktree."""
    proc = subprocess.run(["git", "-C", repo, "show", f"{commit}:{path}"], capture_output=True)
    if proc.returncode != 0:
        raise RewardGuardError(f"git show {commit[:12]}:{path} failed: {proc.stderr.decode(errors='replace').strip()}")
    return proc.stdout


def list_files(repo: str, commit: str) -> list[str]:
    return git(repo, "ls-tree", "-r", "--name-only", commit).stdout.splitlines()


@dataclass
class ChangedFile:
    status: str  # A, M, D, R
    path: str  # new path (old path for deletions)
    old_path: str | None = None


def changed_files(repo: str, base: str, head: str) -> list[ChangedFile]:
    out = git(repo, "diff", "--name-status", "-M", "-z", base, head).stdout
    parts = out.split("\0")
    files: list[ChangedFile] = []
    i = 0
    while i < len(parts) and parts[i]:
        status = parts[i]
        code = status[0]
        if code in ("R", "C"):
            files.append(ChangedFile("R", parts[i + 2], parts[i + 1]))
            i += 3
        else:
            files.append(ChangedFile(code, parts[i + 1]))
            i += 2
    return files


@dataclass
class Hunk:
    header: str
    new_start: int
    lines: list[str] = field(default_factory=list)  # raw diff lines with +/-/space prefix

    @property
    def added(self) -> list[tuple[int, str]]:
        """(line number in new file, text) for every added line."""
        out, n = [], self.new_start
        for line in self.lines:
            if line.startswith("+"):
                out.append((n, line[1:]))
                n += 1
            elif line.startswith("-"):
                continue
            else:
                n += 1
        return out

    @property
    def removed(self) -> list[str]:
        return [l[1:] for l in self.lines if l.startswith("-")]

    def text(self) -> str:
        return self.header + "\n" + "\n".join(self.lines)


_HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@.*$")


def file_hunks(repo: str, base: str, head: str, path: str, context: int, old_path: str | None = None) -> list[Hunk]:
    paths = [old_path, path] if old_path else [path]
    out = git(repo, "diff", f"-U{context}", "-M", "--no-color", base, head, "--", *paths).stdout
    hunks: list[Hunk] = []
    cur: Hunk | None = None
    for line in out.splitlines():
        m = _HUNK_RE.match(line)
        if line.startswith("diff --git "):
            cur = None
        elif m:
            cur = Hunk(header=line, new_start=int(m.group(1)))
            hunks.append(cur)
        elif cur is not None and (line[:1] in ("+", "-", " ") or line == ""):
            cur.lines.append(line if line else " ")
        elif line.startswith("\\"):
            continue
    return hunks
