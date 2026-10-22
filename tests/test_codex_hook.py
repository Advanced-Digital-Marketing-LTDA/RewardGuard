from __future__ import annotations

import argparse
import io
import json
import subprocess
from pathlib import Path

import pytest

from rewardguard import cli, codex_hook, config, gitops
from rewardguard.models import RewardGuardError


def _git(repo: Path, *args: str):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)


def test_staged_snapshot_uses_index_and_preserves_repository_state(sample_repo):
    repo = sample_repo.path
    base = gitops.rev_parse(str(repo), "HEAD")
    staged_path = repo / "src" / "staged.js"
    staged_path.write_text("export const value = 'staged';\n")
    _git(repo, "add", "--", "src/staged.js")
    staged_path.write_text("export const value = 'unstaged edit';\n")
    (repo / "src" / "unstaged.js").write_text("export const value = 'untracked';\n")

    index_before = gitops.git(str(repo), "write-tree").stdout.strip()
    head_before = gitops.rev_parse(str(repo), "HEAD")
    status_before = gitops.git(str(repo), "status", "--porcelain").stdout
    actual_base, staged_head = gitops.staged_snapshot(str(repo))

    assert actual_base == base
    assert gitops.show_file(str(repo), staged_head, "src/staged.js") == "export const value = 'staged';\n"
    assert gitops.show_file(str(repo), staged_head, "src/unstaged.js") is None
    assert [change.path for change in gitops.changed_files(str(repo), actual_base, staged_head)] == ["src/staged.js"]
    worktree = repo.parent / "staged-worktree"
    try:
        gitops.git(str(repo), "worktree", "add", "--detach", str(worktree), staged_head)
        assert (worktree / "src" / "staged.js").read_text() == "export const value = 'staged';\n"
    finally:
        gitops.git(str(repo), "worktree", "remove", "--force", str(worktree), check=False)
    assert gitops.git(str(repo), "write-tree").stdout.strip() == index_before
    assert gitops.rev_parse(str(repo), "HEAD") == head_before
    assert gitops.git(str(repo), "status", "--porcelain").stdout == status_before


def test_staged_snapshot_supports_repository_before_first_commit(tmp_path):
    repo = tmp_path / "new-repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    (repo / "first.py").write_text("value = 1\n")
    _git(repo, "add", "first.py")

    base, head = gitops.staged_snapshot(str(repo))

    assert gitops.show_file(str(repo), head, "first.py") == "value = 1\n"
    assert [(change.status, change.path) for change in gitops.changed_files(str(repo), base, head)] == [("A", "first.py")]
    assert gitops.git(str(repo), "rev-parse", "--verify", "HEAD^{commit}", check=False).returncode != 0


def test_missing_project_config_uses_global_precommit_defaults(sample_repo):
    sample_repo.branch("without-config", {".rewardguard.toml": None})
    repo = str(sample_repo.path)
    head = gitops.rev_parse(repo, "HEAD")

    cfg = config.load_from_commit(repo, head, allow_missing=True)

    assert cfg.run_tests is False
    assert cfg.suites == []
    with pytest.raises(RewardGuardError, match="not found on the base commit"):
        config.load_from_commit(repo, head)


@pytest.mark.parametrize(("command", "suffix"), [
    ("git commit -m 'first'", "."),
    ("git -C nested commit -m x", "nested"),
    ("cd nested && git commit", "nested"),
    ("git status; env FLAG=1 git -c user.name=Codex commit", "."),
    ("git status\ngit commit -m change", "."),
    ("git \\\n commit -m x", "."),
    ("git status # comment\ngit commit -m x", "."),
    ("echo 'first line\ngit commit'", None),
    ("git status", None),
    ("echo 'git commit'", None),
    ("python -c 'git commit'", None),
])
def test_codex_hook_finds_only_commit_commands(command, suffix, tmp_path):
    expected = None if suffix is None else str((tmp_path / suffix).resolve())
    assert codex_hook.commit_repo(command, str(tmp_path)) == expected


def test_codex_hook_ignores_non_commit_bash(monkeypatch, tmp_path):
    event = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "cwd": str(tmp_path),
        "tool_input": {"command": "git status"},
    }
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(event)))
    monkeypatch.setattr(cli, "check", lambda _args: pytest.fail("check should not run"))

    assert cli.codex_precommit() == 0


def test_codex_hook_denies_commit_when_check_fails(monkeypatch, tmp_path, capsys):
    _git(tmp_path, "init", "-q", "-b", "main")
    event = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "cwd": str(tmp_path),
        "tool_input": {"command": "git commit -m x"},
    }
    captured = []
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(event)))

    def fail(args):
        captured.append(args)
        return 1

    monkeypatch.setattr(cli, "check", fail)

    assert cli.codex_precommit() == 2
    assert captured[0].staged is True
    assert captured[0].repo == str(tmp_path.resolve())
    assert "commit blocked" in capsys.readouterr().err


def test_staged_config_is_loaded_from_default_branch(sample_repo):
    sample_repo.branch("config-weakened", {".rewardguard.toml": "run_tests = false\n"})
    repo = str(sample_repo.path)
    args = argparse.Namespace(staged=True)

    _base, _head, cfg = cli._resolve(repo, args)

    assert cfg.run_tests is True
    assert gitops.rev_parse(repo, args.config_base) == gitops.rev_parse(repo, "main")


def test_staged_check_uses_staged_version_without_project_config(tmp_path, fake_jev, capsys):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "test")
    (repo / "README.md").write_text("base\n")
    _git(repo, "add", "README.md")
    _git(repo, "commit", "-qm", "base")

    path = repo / "tests" / "staged.test.js"
    path.parent.mkdir(exist_ok=True)
    path.write_text('test.only("staged case", () => {});\n')
    _git(repo, "add", "--", "tests/staged.test.js")
    path.write_text('test("unstaged version", () => {});\n')
    fake_jev()

    status = cli.main(["check", "--staged", "--repo", str(repo), "--quiet"])

    assert status == 1
    assert "ONLY_ADDED" in capsys.readouterr().out


@pytest.mark.parametrize(("command", "reason_text"), [
    ("git add -A && git commit -m x", "git add"),
    ("git add -- file.js\ngit commit -m x", "git add"),
    ("git commit -am x", "-a"),
    ("git commit --all -m x", "-a"),
    ("git commit --only file.js", "outside the checked index"),
    ("git commit -- file.js", "outside the checked index"),
    ("git commit file.js", "outside the checked index"),
    ("git --git-dir=/repo-b/.git --work-tree=/repo-b commit -m x", "repository override"),
    ("git --git-dir /repo-b/.git --work-tree /repo-b commit -m x", "repository override"),
])
def test_codex_hook_blocks_commands_that_change_commit_content(command, reason_text, tmp_path):
    context = codex_hook.commit_context(command, str(tmp_path))

    assert context is not None
    assert context[0] == str(tmp_path.resolve())
    assert reason_text in context[1]


@pytest.mark.parametrize("command", [
    "git commit -m x",
    "git commit -qm change",
    "git commit -vm change",
    "git commit -m change # explain the commit",
    "git commit -m '#literal' # explain the commit",
    "git commit -m change#literal",
])
def test_codex_hook_allows_commit_from_existing_index_only(command, tmp_path):
    assert codex_hook.commit_context(command, str(tmp_path)) == (str(tmp_path.resolve()), None)


@pytest.mark.parametrize("command", [
    "git add -A && git commit -m x",
    "git commit -am x",
    "git --git-dir=/other/.git --work-tree=/other commit -m x",
])
def test_codex_hook_blocks_unsafe_commit_before_running_check(monkeypatch, tmp_path, capsys, command):
    event = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "cwd": str(tmp_path),
        "tool_input": {"command": command},
    }
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(event)))
    monkeypatch.setattr(cli, "check", lambda _args: pytest.fail("unsafe commit must be rejected before check"))

    assert cli.codex_precommit() == 2
    err = capsys.readouterr().err
    assert "commit blocked" in err
    assert "Stage changes in a separate Codex Bash call" in err


def test_codex_hook_checks_repository_root_when_commit_runs_from_subdirectory(monkeypatch, tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    nested = repo / "nested"
    nested.mkdir()
    event = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "cwd": str(nested),
        "tool_input": {"command": "git commit -m x"},
    }
    captured = []
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(event)))
    monkeypatch.setattr(cli, "check", lambda args: captured.append(args) or 0)

    assert cli.codex_precommit() == 0
    assert captured[0].repo == str(repo.resolve())


def test_codex_hook_checks_multiline_commit(monkeypatch, tmp_path):
    _git(tmp_path, "init", "-q", "-b", "main")
    event = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "cwd": str(tmp_path),
        "tool_input": {"command": "git status\ngit commit -m x"},
    }
    captured = []
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(event)))
    monkeypatch.setattr(cli, "check", lambda args: captured.append(args) or 1)

    assert cli.codex_precommit() == 2
    assert captured[0].repo == str(tmp_path.resolve())
