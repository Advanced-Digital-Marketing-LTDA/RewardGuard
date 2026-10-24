"""Publish scoped content checks from a trusted RewardGuard JSON report (stdlib only)."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import html
import json
import math
import os
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
                      ("source_only", "source only"), ("applicability", "applicability"))
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
        if not isinstance(row_status, str) or row_status not in {"eligible", "skipped", "evaluated", "not_evaluated", "not_applicable"}:
            raise ValueError("unknown content coverage status")
        rule = row.get("rule")
        if rule is not None and (not isinstance(rule, str) or not RULE_ID.fullmatch(rule)):
            raise ValueError("invalid content rule ID")
        if row_status in {"evaluated", "not_applicable"} and rule is None:
            raise ValueError("rule coverage requires a content rule ID")
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
    for key in ("eligibility", "missing_sources", "reason"):
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--repo", required=True)
    args = parser.parse_args(argv)
    try:
        if not re.fullmatch(r"[0-9a-fA-F]{40}", args.head):
            raise ValueError("head must be a resolved 40-character commit SHA")
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repo) or any(x in (".", "..") for x in args.repo.split("/")):
            raise ValueError("repo must be owner/name")
        base = os.environ.get("GITHUB_API_URL", "https://api.github.com").rstrip("/")
        parsed = urllib.parse.urlsplit(base)
        if (parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password
                or parsed.query or parsed.fragment or parsed.port not in (None, 443)
                or parsed.path not in ("", "/api/v3")):
            raise ValueError("GitHub API URL must be an absolute HTTPS API host (optionally /api/v3)")
        token = os.environ.get("GH_TOKEN", "")
        if not token or any(ord(c) < 33 or ord(c) > 126 for c in token):
            print("::error::GH_TOKEN is missing or invalid; content checks require a token with checks:write.", file=sys.stderr)
            return 2
        invalid = False
        try:
            with open(args.report, encoding="utf-8") as stream:
                report = json.load(stream)
            if not isinstance(report, dict):
                raise ValueError("report must be an object")
            checks = build_checks(report)
        except (OSError, ValueError, TypeError):
            print("::error::RewardGuard JSON report is absent or malformed; content coverage is unavailable. Inspect the original judge error.", file=sys.stderr)
            invalid = True
            checks = [error_check("RewardGuard JSON report is absent or malformed. Content coverage is unavailable; inspect the original judge step error."),
                      {"name": "contentguard / eligibility", "conclusion": "neutral", "output": {"title": "Content eligibility unavailable", "summary": "No valid report; no content scope can be claimed reviewed."}}]
        opener = urllib.request.build_opener(NoRedirect)
        for check in checks:
            # GitHub caps text by bytes; bound every output even with multi-byte report text.
            check["output"]["summary"] = display_limit(check["output"]["summary"], 60000)
            check["output"]["title"] = display_limit(check["output"]["title"], 250)
            payload = dict(check, head_sha=args.head, status="completed")
            request = urllib.request.Request(f"{base}/repos/{args.repo}/check-runs", method="POST",
                                             data=json.dumps(payload, allow_nan=False).encode(),
                                             headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                                                      "Content-Type": "application/json", "X-GitHub-Api-Version": "2022-11-28"})
            with opener.open(request, timeout=20) as response:
                if response.status != 201:
                    raise ValueError("GitHub check creation did not return HTTP 201")
                response_body = response.read(1_048_577)
                if len(response_body) > 1_048_576:
                    raise ValueError("GitHub check response exceeds the 1 MiB limit")
                result = json.loads(response_body)
                if not isinstance(result, dict) or type(result.get("id")) is not int or result["id"] <= 0:
                    raise ValueError("GitHub returned an invalid check ID")
        print(f"Published {len(checks)} scoped content checks.")
        return 2 if invalid else 0
    except urllib.error.HTTPError as exc:
        print(f"::error::Content check publication failed (HTTP {exc.code}); verify checks:write permission.", file=sys.stderr)
    except (OSError, ValueError, TypeError, urllib.error.URLError):
        print("::error::Content check publication failed: invalid inputs, API response, or unavailable API. No complete publication can be claimed.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
