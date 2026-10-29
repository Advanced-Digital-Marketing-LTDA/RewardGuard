"""Publish scoped content checks from a trusted RewardGuard JSON report (stdlib only)."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import html
import json
import math
import os
from pathlib import Path
import stat
import re
import sys
import urllib.error
import urllib.parse
import urllib.request


RULE_ID = re.compile(r"CG_[A-Z0-9_]{1,116}\Z")


def display_limit(value: str, limit: int) -> str:
    """Cap presentation bytes explicitly; grading always uses the original report."""
    encoded = value.encode("utf-8")
    if len(encoded) <= limit:
        return value
    marker = " … (display truncated; see JSON)"
    budget = max(0, limit - len(marker.encode("utf-8")))
    return encoded[:budget].decode("utf-8", errors="ignore").rstrip("\\") + marker


def safe(value: object, limit: int = 2000) -> str:
    """Render report data as inert Markdown text, marking any display truncation."""
    value = re.sub(r"[\x00-\x1f\x7f]", " ", str(value))
    value = html.escape(value, quote=False)
    return display_limit(re.sub(r"([\\`*_{}\[\]()#+.!|>~-])", r"\\\1", value), limit)


def source_records(value: object) -> list[dict]:
    """Keep report provenance readable without exposing its internal dictionary layout."""
    if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
        raise ValueError("source provenance must be an array of objects")
    return [row for row in value if row.get("role") != "boundary"]


def source_summary(value: object) -> str:
    if value is None:
        return "Source provenance not supplied"
    rows = source_records(value)
    paths = sorted({str(row.get("path", row.get("file", "unspecified"))) for row in rows})
    examples = ", ".join(safe(path, 250) for path in paths[:5])
    tail = f"; {len(paths) - 5} more paths" if len(paths) > 5 else ""
    return f"{len(rows)} evidence unit(s) from {len(paths)} source path(s)" + (f": {examples}{tail}" if paths else "")


def omission_groups(value: object) -> list[tuple[str, list[str], int]]:
    if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
        raise ValueError("collection omissions must be an array of objects")
    groups = defaultdict(list)
    for row in value:
        groups[str(row.get("reason", "Evidence unavailable"))].append(str(row.get("path", row.get("file", "unspecified"))))
    return [(reason, sorted(set(paths)), len(paths)) for reason, paths in sorted(groups.items())]


def omission_summary(value: object) -> str:
    if value is None:
        return "Collection omission metadata not supplied"
    groups = omission_groups(value)
    parts = [f"{safe(reason, 300)} ({count})" for reason, _, count in groups[:6]]
    if len(groups) > 6:
        parts.append(f"{len(groups) - 6} additional reason(s); see JSON")
    return "; ".join(parts) or "No collection omissions recorded"


def probability(value: object) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if not 0 <= value <= 1:
        return None
    return float(value) if math.isfinite(value) else None


def _scope(row: dict) -> str:
    return "; ".join(f"{label}: {source_summary(row[key]) if key == 'provenance' else safe(row[key])}" for key, label in
                     (("file", "file"), ("line", "line"), ("instance", "instance"), ("reason", "reason"),
                      ("requires", "requires"), ("available", "available"),
                      ("missing_sources", "missing sources"), ("provenance", "provenance"),
                      ("reused", "authenticated reuse"), ("explanation_status", "explanation status"),
                      ("result_complete", "result complete"), ("source_only", "source only"), ("applicability", "applicability"))
                     if row.get(key) is not None) or "Scope unspecified in report"


def build_checks(report: dict) -> list[dict]:
    content = report.get("content")
    if not isinstance(content, dict) or not content:
        raise ValueError("content must be a nonempty object")
    status = content.get("status")
    if not isinstance(status, str) or status not in {"reviewed", "skipped", "not_evaluated", "error"}:
        raise ValueError("unknown content status")
    coverage = content.get("coverage")
    findings = report.get("findings")
    notes = report.get("notes")
    if not isinstance(coverage, list) or not all(isinstance(r, dict) for r in coverage):
        raise ValueError("coverage must be an array of objects")
    if not isinstance(findings, list) or not all(isinstance(r, dict) for r in findings):
        raise ValueError("findings must be an array of objects")
    if not isinstance(notes, list) or not all(isinstance(note, str) for note in notes):
        raise ValueError("notes must be an array of strings")
    for field in ("provenance", "omissions"):
        if field in content and (not isinstance(content[field], list) or
                                 not all(isinstance(row, dict) for row in content[field])):
            raise ValueError(f"{field} must be an array of objects")
    for row in coverage:
        row_status = row.get("status")
        if not isinstance(row_status, str) or row_status not in {"eligible", "skipped", "evaluated", "not_evaluated", "not_applicable", "unchanged"}:
            raise ValueError("unknown content coverage status")
        rule = row.get("rule")
        if rule is not None and (not isinstance(rule, str) or not RULE_ID.fullmatch(rule)):
            raise ValueError("invalid content rule ID")
        if row_status in {"evaluated", "not_applicable"} and rule is None:
            raise ValueError("rule coverage requires a content rule ID")
        if (rule is not None or row.get("stage") == "classification") and (
                not isinstance(row.get("file"), str) or not row["file"].strip()):
            raise ValueError("content rule and classification scopes require an artifact path")
        if row.get("stage") == "classification":
            if row_status not in {"eligible", "skipped"} or probability(row.get("probability")) is None:
                raise ValueError("classification requires a valid probability and classification status")
        elif row_status in {"eligible", "skipped"}:
            raise ValueError("classification status requires the classification stage")
        if row_status == "evaluated" and probability(row.get("probability")) is None:
            raise ValueError("evaluated coverage requires a valid probability")
        if "applicability" in row and probability(row["applicability"]) is None:
            raise ValueError("rule applicability requires a valid probability")
    for finding in findings:
        if finding.get("source") == "content":
            rule = finding.get("rule")
            if not isinstance(rule, str) or not RULE_ID.fullmatch(rule) or probability(finding.get("probability")) is None:
                raise ValueError("content findings require a content rule ID and valid probability")
            if not isinstance(finding.get("file"), str) or not finding["file"].strip():
                raise ValueError("content findings require an artifact path")
    if status == "reviewed" and not any(row["status"] == "evaluated" for row in coverage):
        raise ValueError("reviewed content must contain an evaluated rule scope")
    counts = Counter(row["status"] for row in coverage)
    classifiers = [row for row in coverage if row.get("stage") == "classification"]
    summary = (f"Content status: {safe(status)}. Classification: {len(classifiers)} chunk(s), "
               f"{sum(r.get('status') == 'eligible' for r in classifiers)} eligible, "
               f"{sum(r.get('status') == 'skipped' for r in classifiers)} skipped.\n\n"
               + "Coverage: " + (", ".join(f"{safe(k)}: {v}" for k, v in sorted(counts.items())) or "no coverage recorded")
               + ".\n\nClassification at p >= 0.60 enters review; it is not a defect score. "
               "Skipped and missing evidence scopes are unverified, never a clean content verdict.")
    declarations = content.get('eligibility')
    if isinstance(declarations, list):
        summary = (f"Content status: {safe(status)}. Trusted publication eligibility: {len(declarations)} artifact(s).\n\n"
                   "Eligibility is deterministic and has no model probability. "
                   "Defects warn at 0.60 <= p < 0.80 and fail at p >= 0.80.\n\n"
                   + "Coverage: " + (", ".join(f"{safe(k)}: {v}" for k, v in sorted(counts.items())) or "no coverage recorded")
                   + ". Skipped and missing evidence scopes remain unverified.")
    for row in classifiers[:20]:
        summary += f"\n- {_scope(row)}; classification p={safe(row['probability'])}; {safe(row['status'])}"
    if len(classifiers) > 20:
        summary += f"\n- {len(classifiers) - 20} additional classification scopes; see JSON."
    general_gaps = [r for r in coverage if not r.get("rule") and r.get("status") == "not_evaluated"]
    for row in general_gaps[:10]:
        summary += f"\n- Unverified: {_scope(row)}"
    if len(general_gaps) > 10:
        summary += f"\n- {len(general_gaps) - 10} additional unverified scopes; see JSON."
    summary += f"\n\nSources: {source_summary(content.get('provenance', []))}"
    if content.get("omissions"):
        summary += f"\n\nCollection limits: {omission_summary(content['omissions'])}. Missing automatic discovery probes do not require repository setup."
    for key in ("missing_sources", "reason"):
        if key in content:
            summary += f"\n\n{safe(key)}: {safe(content[key])}"
    content_notes = [note for note in notes if "content" in note.lower()]
    for note in content_notes[:10]:
        summary += f"\n\n{safe(note)}"
    if len(content_notes) > 10:
        summary += f"\n\n{len(content_notes) - 10} additional content notes; see JSON."
    checks = [{"name": "contentguard / eligibility", "conclusion": "neutral",
               "output": {"title": "Content eligibility and coverage", "summary": display_limit(summary, 60000)}}]
    groups = defaultdict(list)
    for row in coverage:
        if row.get("rule") and row.get("status") in ("evaluated", "not_evaluated"):
            rule = row["rule"]
            if not isinstance(rule, str) or not RULE_ID.fullmatch(rule):
                raise ValueError("invalid content rule ID")
            groups[rule].append(row)
    content_findings = defaultdict(list)
    for row in findings:
        if row.get("source") != "content":
            continue
        rule = row.get("rule")
        if not isinstance(rule, str) or not RULE_ID.fullmatch(rule):
            raise ValueError("invalid content finding rule ID")
        content_findings[rule].append(row)
        groups.setdefault(rule, [])
    for rule, rows in sorted(groups.items()):
        evaluated = [r for r in rows if r.get("status") == "evaluated"]
        gaps = [r for r in rows if r.get("status") == "not_evaluated"]
        # Every evaluated/finding score was validated before any presentation limits.
        scores = [float(row["probability"]) for row in evaluated + content_findings[rule]]
        peak = max(scores) if scores else None
        uncertain = bool(gaps)
        conclusion = "neutral"
        if peak is not None and peak >= .8:
            conclusion = "failure"
        elif peak is not None and peak < .6 and evaluated and not uncertain:
            conclusion = "success"
        title = f"{rule}: " + (f"highest p={peak!r}" if peak is not None else "unverified")
        summary = (f"{len(evaluated)} evaluated proposition(s); {len(gaps)} missing evidence scope(s). "
                   f"Highest defect probability: {peak!r}.\n\n"
                   "p < 0.60 ignored; 0.60 <= p < 0.80 warning (neutral); p >= 0.80 failure. "
                   "A success covers only the evaluated scopes listed here. Missing evidence is unverified.")
        for key in ("pack", "title", "skill"):
            values = sorted({str(row[key]) for row in rows if row.get(key) is not None})
            if values:
                summary += f"\n\n{safe(key)}: {safe(', '.join(values))}"
        for row in rows[:30]:
            summary += f"\n- {safe(row.get('status'))}: {_scope(row)}"
            if row.get("probability") is not None:
                summary += f"; p={safe(row['probability'])}"
        if len(rows) > 30:
            summary += f"\n- {len(rows) - 30} additional scopes; consult JSON report."
        for finding in content_findings[rule][:10]:
            summary += f"\n\nFinding: {_scope(finding)}; p={safe(finding.get('probability'))}: {safe(finding.get('message', ''))}"
            for detail in (finding.get("details") or [])[:5]:
                if isinstance(detail, dict):
                    summary += f"\n- Grounded line {safe(detail.get('line'))}: {safe(detail.get('problem', ''))}; fix: {safe(detail.get('fix', ''))}"
            if len(finding.get("details") or []) > 5:
                summary += f"\n- {len(finding['details']) - 5} additional grounded details; see JSON."
        if len(content_findings[rule]) > 10:
            summary += f"\n\n{len(content_findings[rule]) - 10} additional findings; see JSON."
        checks.append({"name": f"contentguard / {rule}", "conclusion": conclusion,
                       "output": {"title": title, "summary": display_limit(summary, 60000)}})
    if status == "error":
        checks.append(error_check("Content evaluation failed; reviewed scopes are incomplete. See the RewardGuard error report."))
    return checks


def error_check(message: str) -> dict:
    return {"name": "contentguard / evaluation", "conclusion": "failure",
            "output": {"title": "Content reporting or evaluation error", "summary": safe(message)}}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("GitHub API redirects are not permitted")



def load_report(report_argument: str) -> dict:
    """Read one bounded report inside the runner report directory or local CWD."""
    runner_directory = os.environ.get("RUNNER_TEMP")
    if runner_directory is not None and not runner_directory.strip():
        raise ValueError("RUNNER_TEMP must identify the runner report directory")
    try:
        allowed_directory = (Path(runner_directory) if runner_directory is not None else Path.cwd()).resolve(strict=True)
        report_path = Path(report_argument).resolve(strict=True)
    except RuntimeError as exc:
        raise ValueError("report path cannot be resolved safely") from exc
    if not allowed_directory.is_dir():
        raise ValueError("report root must be a directory")
    if not report_path.is_relative_to(allowed_directory) or report_path.suffix != ".json":
        raise ValueError("report must be a JSON file inside the report directory")
    # Resolve before containment checking, and reject a changed final-component symlink on open.
    descriptor = os.open(report_path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
    with os.fdopen(descriptor, "rb") as stream:
        metadata = os.fstat(stream.fileno())
        maximum_bytes = 16 * 1024 * 1024
        if not stat.S_ISREG(metadata.st_mode):
            raise ValueError("report must be a regular file")
        if metadata.st_size > maximum_bytes:
            raise ValueError("report exceeds the 16 MiB size limit")
        payload = stream.read(maximum_bytes + 1)
        if len(payload) > maximum_bytes:
            raise ValueError("report exceeds the 16 MiB size limit")
    try:
        report = json.loads(payload)
    except RecursionError as exc:
        raise ValueError("report JSON nesting is unsupported") from exc
    if not isinstance(report, dict):
        raise ValueError("report must be an object")
    return report


def main(argv: list[str] | None = None) -> int:
    # Backward-compatible command name, one shared publication boundary.
    from .publisher import main as publish_main
    return publish_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
