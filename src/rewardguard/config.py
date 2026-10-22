"""Configuration, always read from the base commit so a branch cannot loosen its own check."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field

from . import gitops
from .models import FAIL, WARN, RewardGuardError

CONFIG_FILE = ".rewardguard.toml"

DEFAULT_TEST_GLOBS = [
    "**/*.{test,spec}.{js,jsx,ts,tsx,mjs,cjs,mts,cts}",
    "**/__tests__/**",
    "**/{test,tests,e2e}/**",
]
DEFAULT_CONFIG_GLOBS = [
    "**/{jest,vitest,vite,playwright}.config.*",
    "**/vitest.workspace.*",
    "**/{jest,vitest}.setup.*",
    "**/setupTests.*",
    "**/.{c8rc,nycrc}{,.*}",
    ".github/**",
    CONFIG_FILE,
]
DEFAULT_SNAPSHOT_GLOBS = ["**/__snapshots__/**", "**/*-snapshots/**", "**/*.snap"]
DEFAULT_JUDGE_INCLUDE = ["**/*.{js,jsx,ts,tsx,mjs,cjs,mts,cts,vue,svelte}"]
DEFAULT_EXCLUDE = [
    "**/node_modules/**",
    "**/dist/**",
    "**/build/**",
    "**/coverage/**",
    "**/*.min.js",
    "**/{package-lock.json,yarn.lock,pnpm-lock.yaml}",
]


@dataclass
class Suite:
    name: str
    command: str


@dataclass
class Config:
    install: str | None
    suites: list[Suite]
    run_tests: bool = True  # false: skip the test-run layer (static checks, Jev and Haiku only)
    test_globs: list[str] = field(default_factory=lambda: list(DEFAULT_TEST_GLOBS))
    config_globs: list[str] = field(default_factory=lambda: list(DEFAULT_CONFIG_GLOBS))
    snapshot_globs: list[str] = field(default_factory=lambda: list(DEFAULT_SNAPSHOT_GLOBS))
    judge_include: list[str] = field(default_factory=lambda: list(DEFAULT_JUDGE_INCLUDE))
    exclude: list[str] = field(default_factory=lambda: list(DEFAULT_EXCLUDE))
    fail_threshold: float = 0.8
    warn_threshold: float = 0.5
    model: str = "jev-1.13.0"
    api_url: str = "https://api.typesafe.ai/v1/systemone"
    max_state_chars: int = 90_000  # ~22k tokens; Jev allows 32k for state + longest question
    context_lines: int = 20
    concurrency: int = 4
    timeout_seconds: int = 60
    explainer_model: str = "claude-haiku-5-5"
    explainer_effort: str = "low"
    explainer_timeout_seconds: int = 300
    explainer_min_probability: float = 0.6  # Haiku explains only Jev findings at or above this
    test_timeout_seconds: int = 1800
    rule_severity: dict[str, str] = field(default_factory=dict)

    def severity(self, rule: str, default: str) -> str:
        return self.rule_severity.get(rule, default)


def _list(section: dict, key: str, default: list[str]) -> list[str]:
    v = section.get(key, default)
    if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
        raise RewardGuardError(f"{CONFIG_FILE}: '{key}' must be a list of strings")
    return v


def parse(text: str) -> Config:
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as e:
        raise RewardGuardError(f"{CONFIG_FILE} is not valid TOML: {e}") from e

    run_tests = data.get("run_tests", True)
    if not isinstance(run_tests, bool):
        raise RewardGuardError(f"{CONFIG_FILE}: run_tests must be true or false")
    suites_raw = data.get("suites", [])
    if not isinstance(suites_raw, list) or (run_tests and not suites_raw):
        raise RewardGuardError(f"{CONFIG_FILE} must define at least one [[suites]] entry, or set run_tests = false")
    suites = []
    for s in suites_raw:
        if not isinstance(s, dict) or not s.get("name") or not s.get("command"):
            raise RewardGuardError(f"{CONFIG_FILE}: every [[suites]] needs 'name' and 'command'")
        suites.append(Suite(name=str(s["name"]), command=str(s["command"])))

    paths = data.get("paths", {})
    th = data.get("thresholds", {})
    judge = data.get("judge", {})
    explainer = data.get("explainer", {})
    rules = data.get("rules", {})
    for rule, sev in rules.items():
        if sev not in (FAIL, WARN, "off"):
            raise RewardGuardError(f"{CONFIG_FILE}: rule {rule} severity must be fail, warn or off")

    cfg = Config(
        install=data.get("install"),
        suites=suites,
        run_tests=run_tests,
        test_globs=_list(paths, "test_globs", DEFAULT_TEST_GLOBS),
        config_globs=_list(paths, "config_globs", DEFAULT_CONFIG_GLOBS),
        snapshot_globs=_list(paths, "snapshot_globs", DEFAULT_SNAPSHOT_GLOBS),
        judge_include=_list(paths, "judge_include", DEFAULT_JUDGE_INCLUDE),
        exclude=_list(paths, "exclude", DEFAULT_EXCLUDE),
        fail_threshold=float(th.get("fail", 0.8)),
        warn_threshold=float(th.get("warn", 0.5)),
        model=str(judge.get("model", "jev-1.13.0")),
        api_url=str(judge.get("api_url", "https://api.typesafe.ai/v1/systemone")),
        max_state_chars=int(judge.get("max_state_chars", 90_000)),
        context_lines=int(judge.get("context_lines", 20)),
        concurrency=int(judge.get("concurrency", 4)),
        timeout_seconds=int(judge.get("timeout_seconds", 60)),
        explainer_model=str(explainer.get("model", "claude-haiku-5-5")),
        explainer_effort=str(explainer.get("effort", "low")),
        explainer_timeout_seconds=int(explainer.get("timeout_seconds", 300)),
        explainer_min_probability=float(explainer.get("min_probability", 0.6)),
        test_timeout_seconds=int(data.get("test_timeout_seconds", 1800)),
        rule_severity=dict(rules),
    )
    if not 0 < cfg.warn_threshold <= cfg.fail_threshold <= 1:
        raise RewardGuardError(f"{CONFIG_FILE}: need 0 < warn <= fail <= 1")
    if cfg.model == "jev-latest":
        raise RewardGuardError(f"{CONFIG_FILE}: pin a versioned Jev model, not jev-latest")
    if cfg.explainer_effort not in ("low", "medium", "high", "xhigh", "max"):
        raise RewardGuardError(f"{CONFIG_FILE}: explainer effort must be low, medium, high, xhigh or max")
    if not 0 < cfg.explainer_min_probability <= 1:
        raise RewardGuardError(f"{CONFIG_FILE}: explainer min_probability must be above 0 and at most 1")
    return cfg


def load_from_commit(repo: str, commit: str) -> Config:
    text = gitops.show_file(repo, commit, CONFIG_FILE)
    if text is None:
        raise RewardGuardError(
            f"{CONFIG_FILE} not found on the base commit {commit[:12]}. "
            "Commit it to the base branch first; it is never read from the branch being checked."
        )
    return parse(text)
