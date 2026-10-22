from __future__ import annotations

from dataclasses import dataclass, field

FAIL = "fail"
WARN = "warn"


class RewardGuardError(Exception):
    """A condition that stops the check. Always results in a failing exit code."""


@dataclass
class Finding:
    rule: str
    severity: str  # FAIL or WARN
    message: str
    file: str | None = None
    line: int | None = None
    source: str = "static"  # static | run | judge
    probability: float | None = None
    evidence: str | None = None

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def failed(self) -> bool:
        return bool(self.errors) or any(f.severity == FAIL for f in self.findings)

    def add(self, finding: Finding) -> None:
        self.findings.append(finding)
