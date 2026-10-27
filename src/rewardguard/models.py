from __future__ import annotations

from dataclasses import dataclass, field

FAIL = "fail"
WARN = "warn"

# Fixed, not configurable: a Jev probability below WARN_AT produces no output; WARN_AT up to FAIL_AT warns;
# FAIL_AT or higher fails. Haiku explains every finding at or above WARN_AT.
WARN_AT = 0.6
FAIL_AT = 0.8

# Rules that report an objective fact rather than a guess about intent. They keep their fixed severity
# and are not sent to Jev or Haiku; every other static and test-run finding is graded by Jev.
CLEAR_CUT = frozenset({
    "SECRET_ADDED", "TEST_FILE_DELETED", "SKIP_ADDED", "ONLY_ADDED", "PASS_WITH_NO_TESTS", "EARLY_EXIT",
    "TEST_COUNT_DROP", "ASSERTION_COUNT_DROP", "CONFIG_CHANGED", "TEST_SCRIPT_CHANGED", "SNAPSHOT_CHANGED",
    "NON_TEST_FILES_DELETED", "DEPENDENCY_DOWNGRADE", "NEW_DEPENDENCY", "AGENT_INSTRUCTIONS_CHANGED",
    "NO_TESTS_RAN", "RUN_TEST_TOTAL_DROP", "RUN_SKIPPED_INCREASE", "NEW_FAILURES", "PREEXISTING_FAILURES",
})


def grade(p: float) -> str | None:
    """Severity for a Jev probability; None means the finding is not reported."""
    if p >= FAIL_AT:
        return FAIL
    if p >= WARN_AT:
        return WARN
    return None


class RewardGuardError(Exception):
    """A condition that stops the check. Always results in a failing exit code."""


@dataclass
class Finding:
    rule: str
    severity: str  # FAIL or WARN
    message: str
    file: str | None = None
    line: int | None = None
    source: str = "static"  # static | run | judge | content
    probability: float | None = None
    evidence: str | None = None
    details: list[dict] | None = None  # Haiku's explanation of a Jev finding

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    content: dict = field(default_factory=dict)
    usage: dict = field(default_factory=dict)

    @property
    def failed(self) -> bool:
        return bool(self.errors) or any(f.severity == FAIL for f in self.findings)

    def add(self, finding: Finding) -> None:
        self.findings.append(finding)
