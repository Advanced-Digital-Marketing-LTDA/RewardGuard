"""Runs each test suite three times in clean worktrees:

1. base   - the base commit as-is
2. head   - the branch, with test-runner config taken from base
3. original - the branch's code, run against the base branch's test files and config

Test commands never see the Jev key or GitHub tokens.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from . import gitops
from .config import Config, Suite
from .models import FAIL, WARN, Finding, RewardGuardError
from .static_checks import CHECKER, CONFIG, TEST, classify

SECRET_ENV = ("TYPESAFE_API_KEY", "GITHUB_TOKEN", "GH_TOKEN", "ACTIONS_RUNTIME_TOKEN",
              "ACTIONS_ID_TOKEN_REQUEST_TOKEN", "ACTIONS_ID_TOKEN_REQUEST_URL")


@dataclass
class Results:
    total: int = 0
    skipped: int = 0
    passed: set[str] = field(default_factory=set)
    failed: set[str] = field(default_factory=set)


def _clean_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if k not in SECRET_ENV}
    env["CI"] = env.get("CI", "true")
    return env


def _sh(cmd: str, cwd: Path, timeout: int, env: dict[str, str]) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, shell=True, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        raise RewardGuardError(f"'{cmd}' timed out after {timeout}s in {cwd.name}") from e


def _rel(path: str, root: Path) -> str:
    try:
        return str(Path(path).resolve().relative_to(root.resolve()))
    except ValueError:
        return path


def parse_report(data: dict, root: Path) -> Results:
    r = Results()
    if "testResults" in data:  # Jest / Vitest
        for suite in data["testResults"]:
            fname = _rel(suite.get("name", "?"), root)
            assertions = suite.get("assertionResults") or []
            if not assertions and suite.get("status") == "failed":
                r.failed.add(f"{fname}::<suite failed to run>")
            for a in assertions:
                tid = f"{fname}::{a.get('fullName') or a.get('title')}"
                st = a.get("status")
                r.total += 1
                if st == "passed":
                    r.passed.add(tid)
                elif st == "failed":
                    r.failed.add(tid)
                else:  # pending, skipped, todo, disabled
                    r.skipped += 1
        return r
    if "suites" in data and "stats" in data:  # Playwright
        def walk(suite, titles):
            t = titles + ([suite["title"]] if suite.get("title") else [])
            for spec in suite.get("specs", []):
                for test in spec.get("tests", []):
                    tid = f"{spec.get('file', '?')}::{' > '.join(t[1:] + [spec.get('title', '')])} [{test.get('projectName', '')}]"
                    st = test.get("status")
                    r.total += 1
                    if st == "expected":
                        r.passed.add(tid)
                    elif st in ("unexpected", "flaky"):
                        r.failed.add(tid)
                    else:
                        r.skipped += 1
            for child in suite.get("suites", []):
                walk(child, t)
        for s in data["suites"]:
            walk(s, [])
        for i, err in enumerate(data.get("errors", []) or []):
            r.failed.add(f"<global error {i}>: {str(err.get('message', ''))[:120]}")
        return r
    raise RewardGuardError("Test report is neither Jest/Vitest JSON nor Playwright JSON")


def run_suite(suite: Suite, cwd: Path, cfg: Config, label: str) -> Results:
    report = cwd.parent / f"report-{label}-{suite.name}.json"
    if report.exists():
        report.unlink()
    env = _clean_env()
    env["PLAYWRIGHT_JSON_OUTPUT_NAME"] = str(report)
    cmd = suite.command.replace("{report}", str(report))
    proc = _sh(cmd, cwd, cfg.test_timeout_seconds, env)
    if not report.exists():
        raise RewardGuardError(
            f"Suite '{suite.name}' ({label}) wrote no JSON report. Exit {proc.returncode}.\n"
            f"{(proc.stdout + proc.stderr)[-1500:]}"
        )
    try:
        data = json.loads(report.read_text())
    except json.JSONDecodeError as e:
        raise RewardGuardError(f"Suite '{suite.name}' ({label}) report is not valid JSON: {e}") from e
    return parse_report(data, cwd)


def _overlay_base_config(repo: str, base: str, head: str, head_dir: Path, cfg: Config) -> None:
    base_files = set(gitops.list_files(repo, base))
    for path in base_files:
        if classify(path, cfg) in (CONFIG, CHECKER):
            content = gitops.show_file(repo, base, path)
            dest = head_dir / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content or "")
    # remove config files the branch added
    for rel in gitops.list_files(repo, head):
        if rel not in base_files and classify(rel, cfg) == CONFIG:
            (head_dir / rel).unlink(missing_ok=True)
    # package.json: keep the branch's dependencies, restore base test scripts / jest / vitest blocks
    for path in base_files:
        if not path.endswith("package.json") or "node_modules" in path:
            continue
        dest = head_dir / path
        if not dest.exists():
            continue
        base_pkg = json.loads(gitops.show_file(repo, base, path) or "{}")
        head_pkg = json.loads(dest.read_text())
        scripts = head_pkg.setdefault("scripts", {})
        for k in list(scripts):
            if k not in base_pkg.get("scripts", {}) and _is_test_key(k):
                del scripts[k]
        for k, v in base_pkg.get("scripts", {}).items():
            if _is_test_key(k):
                scripts[k] = v
        for k in ("jest", "vitest"):
            if k in base_pkg:
                head_pkg[k] = base_pkg[k]
            else:
                head_pkg.pop(k, None)
        dest.write_text(json.dumps(head_pkg, indent=2) + "\n")


def _is_test_key(k: str) -> bool:
    return bool(re.search(r"test|e2e|spec|vitest|jest|playwright", k))


def _overlay_base_tests(repo: str, base: str, head: str, head_dir: Path, cfg: Config) -> None:
    base_files = set(gitops.list_files(repo, base))
    for rel in gitops.list_files(repo, head):
        if rel not in base_files and classify(rel, cfg) == TEST:
            (head_dir / rel).unlink(missing_ok=True)
    for path in base_files:
        if classify(path, cfg) == TEST:
            dest = head_dir / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(subprocess.run(["git", "-C", repo, "show", f"{base}:{path}"],
                                            capture_output=True, check=True).stdout)


def run(repo: str, base: str, head: str, cfg: Config, log=print) -> list[Finding]:
    tmp = Path(tempfile.mkdtemp(prefix="rewardguard-"))
    base_dir, head_dir = tmp / "base", tmp / "head"
    findings: list[Finding] = []

    def f(rule, default, msg, evidence=None):
        sev = cfg.severity(rule, default)
        if sev != "off":
            findings.append(Finding(rule, sev, msg, source="run", evidence=evidence))

    try:
        gitops.git(repo, "worktree", "add", "--detach", str(base_dir), base)
        gitops.git(repo, "worktree", "add", "--detach", str(head_dir), head)
        _overlay_base_config(repo, base, head, head_dir, cfg)
        if cfg.install:
            for d in (base_dir, head_dir):
                log(f"  install in {d.name}: {cfg.install}")
                proc = _sh(cfg.install, d, cfg.test_timeout_seconds, _clean_env())
                if proc.returncode != 0:
                    raise RewardGuardError(f"Install failed in {d.name}:\n{(proc.stdout + proc.stderr)[-1500:]}")

        base_res, head_res = {}, {}
        for s in cfg.suites:
            log(f"  suite '{s.name}': base")
            base_res[s.name] = run_suite(s, base_dir, cfg, "base")
            log(f"  suite '{s.name}': head")
            head_res[s.name] = run_suite(s, head_dir, cfg, "head")

        _overlay_base_tests(repo, base, head, head_dir, cfg)
        orig_res = {}
        for s in cfg.suites:
            log(f"  suite '{s.name}': branch code vs. original tests")
            orig_res[s.name] = run_suite(s, head_dir, cfg, "original")

        for s in cfg.suites:
            b, h, o = base_res[s.name], head_res[s.name], orig_res[s.name]
            n = s.name
            if h.total == 0:
                f("NO_TESTS_RAN", FAIL, f"[{n}] zero tests ran on the branch")
            if h.total < b.total:
                f("RUN_TEST_TOTAL_DROP", FAIL, f"[{n}] tests run dropped {b.total} -> {h.total}")
            if h.skipped > b.skipped:
                f("RUN_SKIPPED_INCREASE", FAIL, f"[{n}] skipped tests rose {b.skipped} -> {h.skipped}")
            new_fail = sorted(h.failed - b.failed)
            if new_fail:
                f("NEW_FAILURES", FAIL, f"[{n}] {len(new_fail)} test(s) fail on the branch but not on base",
                  "\n".join(new_fail[:20]))
            old_fail = sorted(h.failed & b.failed)
            if old_fail:
                f("PREEXISTING_FAILURES", WARN, f"[{n}] {len(old_fail)} test(s) already failing on base",
                  "\n".join(old_fail[:20]))
            broke = sorted(b.passed - o.passed)
            if broke:
                f("ORIGINAL_TESTS_FAIL", WARN,
                  f"[{n}] {len(broke)} base test(s) that passed now fail or don't run against the branch's code. "
                  "Either behavior changed on purpose (confirm the requirement) or the tests were edited to hide a bug.",
                  "\n".join(broke[:20]))
    finally:
        for d in (base_dir, head_dir):
            gitops.git(repo, "worktree", "remove", "--force", str(d), check=False)
        shutil.rmtree(tmp, ignore_errors=True)
    return findings
