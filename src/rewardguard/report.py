from __future__ import annotations

import json

from .models import FAIL, Report

MARKER = "<!-- rewardguard-report -->"


def _loc(f) -> str:
    if not f.file:
        return ""
    return f"{f.file}:{f.line}" if f.line else f.file


def terminal(report: Report) -> str:
    out = []
    for e in report.errors:
        out.append(f"ERROR  {e}")
    for f in sorted(report.findings, key=lambda x: (x.severity != FAIL, x.file or "", x.line or 0)):
        p = f" (p={f.probability:.2f})" if f.probability is not None else ""
        out.append(f"{f.severity.upper():5}  {f.rule}{p}  {_loc(f)}\n       {f.message}")
        if f.evidence:
            out.extend("       > " + l for l in f.evidence.splitlines()[:10])
        for d in f.details or []:
            out.append(f"       line {d['line']}: {d['problem']}")
            out.append(f"         fix: {d['fix']}")
        if f.details == []:
            out.append("       Haiku found no specific lines; review this chunk by hand")
    for n in report.notes:
        out.append(f"note   {n}")
    fails = sum(f.severity == FAIL for f in report.findings)
    warns = len(report.findings) - fails
    verdict = "FAILED" if report.failed else "PASSED"
    out.append(f"\nrewardguard {verdict}: {fails} fail, {warns} warn, {len(report.errors)} error")
    return "\n".join(out)


def markdown(report: Report) -> str:
    fails = sum(f.severity == FAIL for f in report.findings)
    warns = len(report.findings) - fails
    head = "❌ **Failed**" if report.failed else "✅ **Passed**"
    lines = [MARKER, f"## rewardguard: {head}", "",
             f"{fails} fail · {warns} warn · {len(report.errors)} error", ""]
    if report.errors:
        lines += ["### Errors", ""] + [f"- `{e.splitlines()[0][:300]}`" for e in report.errors] + [""]
    if report.findings:
        lines += ["| Severity | Rule | Where | Detail |", "|---|---|---|---|"]
        for f in sorted(report.findings, key=lambda x: (x.severity != FAIL, x.file or "", x.line or 0)):
            p = f" (p={f.probability:.2f})" if f.probability is not None else ""
            detail = f.message.replace("|", "\\|").replace("\n", " ")
            if f.evidence:
                ev = f.evidence.splitlines()[0][:120].replace("|", "\\|").replace("`", "'")
                detail += f"<br>`{ev}`"
            for d in f.details or []:
                problem = f"line {d['line']}: {d['problem']} Fix: {d['fix']}".replace("|", "\\|").replace("\n", " ")
                detail += f"<br>{problem}"
            if f.details == []:
                detail += "<br>Haiku found no specific lines; review this chunk by hand"
            where = f"`{_loc(f)}`" if f.file else "—"
            lines.append(f"| {f.severity} | `{f.rule}`{p} | {where} | {detail} |")
        lines.append("")
    if report.notes:
        lines += [f"<sub>{n}</sub>  " for n in report.notes]
    if report.content:
        coverage = report.content.get("coverage", [])
        gaps = [row for row in coverage if row.get("status") == "not_evaluated"]
        evaluated = sum(row.get("status") == "evaluated" for row in coverage)
        lines += ["", "### Content coverage", "",
                  f"Status: **{report.content.get('status', 'unknown')}** · "
                  f"{evaluated} proposition(s) evaluated · {len(gaps)} evidence gap(s).",
                  "Evidence gaps are unverified checks, not violations or a claimed pass."]
        if gaps:
            lines += ["", "<details><summary>Content evidence gaps</summary>", ""]
            for row in gaps[:50]:
                rule = row.get("rule", row.get("context", row.get("file", "content")))
                lines.append(f"- `{rule}`: {row.get('reason', 'Required evidence unavailable')}")
            if len(gaps) > 50:
                lines.append(f"- {len(gaps) - 50} more gaps; see the JSON report for complete coverage.")
            lines += ["", "</details>"]
    return "\n".join(lines) + "\n"


def as_json(report: Report) -> str:
    return json.dumps({
        "failed": report.failed,
        "errors": report.errors,
        "findings": [f.to_dict() for f in report.findings],
        "notes": report.notes,
        "content": report.content,
    }, indent=2)
