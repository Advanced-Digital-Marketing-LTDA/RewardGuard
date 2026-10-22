from __future__ import annotations

import os
import re
import shlex
from pathlib import Path

_ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
_GIT_VALUE_OPTIONS = {"-c", "-C", "--config-env", "--exec-path", "--git-dir", "--namespace", "--work-tree"}


def _segments(command: str) -> list[list[str]]:
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|<>")
    lexer.whitespace_split = True
    lexer.commenters = ""
    try:
        tokens = list(lexer)
    except ValueError:
        return []
    groups: list[list[str]] = []
    current: list[str] = []
    for token in tokens:
        if token and all(char in ";&|<>" for char in token):
            if current:
                groups.append(current)
                current = []
        else:
            current.append(token)
    if current:
        groups.append(current)
    return groups


def _expanded_path(value: str, cwd: Path) -> Path:
    value = os.path.expanduser(os.path.expandvars(value))
    path = Path(value)
    if not path.is_absolute():
        path = cwd / path
    try:
        return path.resolve()
    except OSError:
        return path


def _git_commit_cwd(words: list[str], cwd: Path) -> Path | None:
    i = 0
    while i < len(words):
        word = words[i]
        if _ASSIGNMENT.match(word) or word in {"command", "exec", "env", "sudo", "time", "nohup", "nice"}:
            i += 1
        else:
            break
    if i >= len(words) or Path(words[i]).name.lower() not in {"git", "git.exe"}:
        return None

    i += 1
    git_cwd = cwd
    while i < len(words):
        word = words[i]
        if word == "commit":
            return git_cwd
        if word in _GIT_VALUE_OPTIONS:
            if i + 1 >= len(words):
                return None
            value = words[i + 1]
            if word == "-C":
                git_cwd = _expanded_path(value, git_cwd)
            i += 2
            continue
        if word.startswith(("--git-dir=", "--work-tree=", "--namespace=", "--exec-path=")):
            i += 1
            continue
        if word.startswith("-"):
            i += 1
            continue
        return None
    return None


def commit_repo(command: str, cwd: str) -> str | None:
    """Return the repository cwd for a plainly expressed git commit command, if present."""
    current = Path(cwd).expanduser().resolve()
    previous: Path | None = None
    for words in _segments(command):
        if words and words[0] in {"cd", "pushd"}:
            i = 1
            if i < len(words) and words[i] == "--":
                i += 1
            while i < len(words) and words[i].startswith("-") and words[i] != "-":
                i += 1
            if i < len(words):
                target = words[i]
                if target == "-" and previous is not None:
                    current, previous = previous, current
                else:
                    path = _expanded_path(target or os.environ.get("HOME", str(current)), current)
                    previous, current = current, path
            else:
                previous, current = current, Path(os.environ.get("HOME", str(current))).expanduser().resolve()
            continue
        if words and words[0] == "popd" and previous is not None:
            current, previous = previous, current
            continue
        repo = _git_commit_cwd(words, current)
        if repo is not None:
            return str(repo)
    return None
