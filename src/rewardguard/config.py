"""Configuration, read from the commit being checked (the PR head).

A branch can therefore change its own config, but it can't do so quietly: any change to
.rewardguard.toml or .github/ always fails CHECKER_CONFIG_CHANGED (the config can't lower or exclude
that rule), and judge.api_url may only change on the base branch, so a branch can't redirect the
Jev key to another server."""
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


DEFAULT_API_URL = "https://api.typesafe.ai/v1/systemone"
UNLOWERABLE_RULES = ("CHECKER_CONFIG_CHANGED",)


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
    api_url: str = DEFAULT_API_URL
    max_state_chars: int = 90_000  # ~22k tokens; Jev allows 32k for state + longest question
    context_lines: int = 20
    concurrency: int = 4
    timeout_seconds: int = 60
    explainer_model: str = "claude-haiku-5-5"
    explainer_effort: str = "low"
    explainer_timeout_seconds: int = 300
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
        if rule in UNLOWERABLE_RULES and sev != FAIL:
            raise RewardGuardError(f"{CONFIG_FILE}: rule {rule} always fails and can't be set to {sev}")

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
        api_url=str(judge.get("api_url", DEFAULT_API_URL)),
        max_state_chars=int(judge.get("max_state_chars", 90_000)),
        context_lines=int(judge.get("context_lines", 20)),
        concurrency=int(judge.get("concurrency", 4)),
        timeout_seconds=int(judge.get("timeout_seconds", 60)),
        explainer_model=str(explainer.get("model", "claude-haiku-5-5")),
        explainer_effort=str(explainer.get("effort", "low")),
        explainer_timeout_seconds=int(explainer.get("timeout_seconds", 300)),
        test_timeout_seconds=int(data.get("test_timeout_seconds", 1800)),
        rule_severity=dict(rules),
    )
    if not 0 < cfg.warn_threshold <= cfg.fail_threshold <= 1:
        raise RewardGuardError(f"{CONFIG_FILE}: need 0 < warn <= fail <= 1")
    if cfg.model == "jev-latest":
        raise RewardGuardError(f"{CONFIG_FILE}: pin a versioned Jev model, not jev-latest")
    if cfg.explainer_effort not in ("low", "medium", "high", "xhigh", "max"):
        raise RewardGuardError(f"{CONFIG_FILE}: explainer effort must be low, medium, high, xhigh or max")
    return cfg


def load_from_commit(repo: str, commit: str) -> Config:
    text = gitops.show_file(repo, commit, CONFIG_FILE)
    if text is None:
        raise RewardGuardError(f"{CONFIG_FILE} not found on commit {commit[:12]}.")
    return parse(text)


def load_for_check(repo: str, base: str, head: str) -> Config:
    """The head's config, refused if it moves judge.api_url away from the base's (or the default when
    the base has no config yet): the Jev key is sent there, so only the base branch may change it."""
    cfg = load_from_commit(repo, head)
    base_text = gitops.show_file(repo, base, CONFIG_FILE)
    allowed = parse(base_text).api_url if base_text is not None else DEFAULT_API_URL
    if cfg.api_url != allowed:
        raise RewardGuardError(
            f"{CONFIG_FILE}: judge.api_url can only change on the base branch "
            f"(base uses {allowed}, this branch sets {cfg.api_url})."
        )
    return cfg
