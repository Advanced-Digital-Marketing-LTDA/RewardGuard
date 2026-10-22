from __future__ import annotations

import os
import re
import shlex
from pathlib import Path

_ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
_GIT_VALUE_OPTIONS = {"-c", "-C", "--config-env", "--exec-path", "--git-dir", "--namespace", "--work-tree"}
_CONTENT_CHANGING_COMMIT_OPTIONS = {
    "-a", "--all", "-i", "--include", "-o", "--only", "-p", "--patch", "--interactive",
}
_COMMIT_VALUE_OPTIONS = {
    "-m", "--message", "-F", "--file", "-c", "--reedit-message", "-C", "--reuse-message",
    "--author", "--date", "--cleanup", "--trailer", "--template", "--fixup", "--squash",
}


def _split_unquoted_newlines(command: str) -> str:
    """Normalize shell line continuations, comments, and unquoted command newlines."""
    parts: list[str] = []
    quote: str | None = None
    escaped = False
    at_word_start = True
    i = 0
    while i < len(command):
        char = command[i]
        if escaped:
            parts.append(char)
            escaped = False
            at_word_start = False
            i += 1
            continue
        if char == "\\\\" and quote != "'":
            if i + 1 < len(command) and command[i + 1] == "\\n":
                i += 2
                continue
            parts.append(char)
            escaped = True
            at_word_start = False
            i += 1
            continue
        if quote == "'":
            if char == "'":
                quote = None
            parts.append(char)
            at_word_start = False
            i += 1
            continue
        if quote == '"':
            if char == '"':
                quote = None
            parts.append(char)
            at_word_start = False
            i += 1
            continue
        if char == "#" and at_word_start:
            while i < len(command):
                if command[i] == "\\\\" and i + 1 < len(command) and command[i + 1] == "\\n":
                    i += 2
                    continue
                if command[i] == "\\n":
                    break
                i += 1
            if i < len(command):
                parts.append(";")
                at_word_start = True
                i += 1
            continue
        if char == "'":
            quote = "'"
            at_word_start = False
        elif char == '"':
            quote = '"'
            at_word_start = False
        elif char == "\\n":
            parts.append(";")
            at_word_start = True
            i += 1
            continue
        elif char.isspace() or char in ";&|<>":
            at_word_start = True
        else:
            at_word_start = False
        parts.append(char)
        i += 1
    return "".join(parts)

def _segments(command: str) -> list[list[str]]:
    lexer = shlex.shlex(_split_unquoted_newlines(command), posix=True, punctuation_chars=";&|<>")
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


def _git_subcommand(words: list[str], cwd: Path) -> tuple[Path, str, list[str], bool] | None:
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
    explicit_repository_override = False
    while i < len(words):
        word = words[i]
        if word.startswith("-") and word not in _GIT_VALUE_OPTIONS and not any(
            word.startswith(option + "=") for option in _GIT_VALUE_OPTIONS if option.startswith("--")
        ):
            i += 1
            continue
        if word in _GIT_VALUE_OPTIONS:
            if i + 1 >= len(words):
                return None
            value = words[i + 1]
            if word == "-C":
                git_cwd = _expanded_path(value, git_cwd)
            elif word in {"--git-dir", "--work-tree"}:
                explicit_repository_override = True
            i += 2
            continue
        if word.startswith(("--git-dir=", "--work-tree=", "--namespace=", "--exec-path=")):
            if word.startswith(("--git-dir=", "--work-tree=")):
                explicit_repository_override = True
            i += 1
            continue
        return git_cwd, word, words[i + 1 :], explicit_repository_override
    return None


def _commit_content_reason(args: list[str]) -> str | None:
    i = 0
    while i < len(args):
        word = args[i]
        if word == "--":
            if i + 1 < len(args):
                return "git commit pathspecs select working-tree content outside the checked index"
            return None
        if word in _CONTENT_CHANGING_COMMIT_OPTIONS or any(
            word.startswith(option + "=")
            for option in ("--all", "--include", "--only", "--patch", "--interactive")
        ):
            return "git commit options such as -a, --only, --include, or --patch select content outside the checked index"
        if word.startswith(("--pathspec-from-file",)):
            return "git commit options select content outside the checked index"
        if word in _COMMIT_VALUE_OPTIONS:
            i += 2
            continue
        if word.startswith("--"):
            i += 1
            continue
        if word.startswith("-") and not word.startswith("--") and len(word) > 1:
            short_options = word[1:]
            for position, option in enumerate(short_options):
                if option in "aiop":
                    return "git commit options such as -a, --only, --include, or --patch select content outside the checked index"
                if option in "mFcC":
                    # Consume a separate value only when the option is last in the bundle.
                    i += 1 if position < len(short_options) - 1 else 2
                    break
            else:
                i += 1
            continue
        return "git commit pathspecs select working-tree content outside the checked index"
    return None

def commit_context(command: str, cwd: str) -> tuple[str, str | None] | None:
    """Return the first repo to check plus a reason if the command can change its commit tree."""
    current = Path(cwd).expanduser().resolve()
    previous: Path | None = None
    first_repo: str | None = None
    blocked_reason: str | None = None
    stage_mutation_seen = False

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

        invocation = _git_subcommand(words, current)
        if invocation is None:
            continue
        git_cwd, subcommand, args, explicit_repository_override = invocation
        if subcommand == "add":
            stage_mutation_seen = True
            continue
        if subcommand != "commit":
            continue

        repo = str(git_cwd)
        if first_repo is None:
            first_repo = repo
        elif repo != first_repo and blocked_reason is None:
            blocked_reason = "multiple repositories are committed in one Bash call; commit in separate calls so each repository is checked"

        if explicit_repository_override:
            reason = "git repository override via --git-dir or --work-tree cannot be safely validated by RewardGuard"
        else:
            reason = _commit_content_reason(args)
        if reason is None and stage_mutation_seen:
            reason = "this Bash call runs git add before git commit; stage in a separate call, then commit in another call"
        if reason is not None and blocked_reason is None:
            blocked_reason = reason

    return None if first_repo is None else (first_repo, blocked_reason)


def commit_repo(command: str, cwd: str) -> str | None:
    """Return the repository cwd for a plainly expressed git commit command, if present."""
    context = commit_context(command, cwd)
    return None if context is None else context[0]
