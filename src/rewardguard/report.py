from __future__ import annotations

import json
from collections import Counter, defaultdict

from .content_checks import safe, source_records, source_summary, omission_groups

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
    for phase, u in sorted(report.usage.items()):
        out.append(f"usage  Jev {phase}: {u['requests']} responses, {u['input_tokens']} reported input tokens, "
                   f"{u['usage_missing']} without usage; {u['state_characters']} state characters, "
                   f"{u['question_characters']} question characters")
        out.append(f"usage  Jev {phase}: {u.get('attempts', 0)} HTTP attempts, "
                   f"{u.get('request_bytes', 0)} serialized request bytes, "
                   f"{u.get('cache_hits', 0)} cache hits, {u.get('budget_denials', 0)} budget denials")
        for stage, s in sorted(u.get('stages', {}).items()):
            out.append(f"usage  Jev {phase}/{stage}: {s['attempts']} HTTP attempts, {s['request_bytes']} request bytes, "
                       f"{s['requests']} responses, {s['input_tokens']} reported input tokens, "
                       f"{s['usage_missing']} missing usage, {s['cache_hits']} cache hits, {s['budget_denials']} budget denials")
    fails = sum(f.severity == FAIL for f in report.findings)
    warns = len(report.findings) - fails
    verdict = "FAILED" if report.failed else "PASSED"
    out.append(f"\nrewardguard {verdict}: {fails} fail, {warns} warn, {len(report.errors)} error")
    return "\n".join(out)


def _content_markdown(content: dict) -> list[str]:
    if not content:
        return []
    coverage = content.get("coverage", [])
    gaps = [r for r in coverage if r.get("status") == "not_evaluated"]
    evaluated = sum(r.get("status") == "evaluated" for r in coverage)
    omitted = sum(r.get("status") == "not_applicable" for r in coverage)
    classified = [r for r in coverage if r.get("stage") == "classification"]
    lines = ["### Content review and coverage", "",
             f"Status: **{safe(content.get('status', 'unknown'))}** · {evaluated} proposition(s) evaluated · "
             f"{len(gaps)} evidence gap(s) · {omitted} not applicable.",
             f"Classification: {len(classified)} chunk(s), "
             f"{sum(r.get('status') == 'eligible' for r in classified)} eligible, "
             f"{sum(r.get('status') == 'skipped' for r in classified)} skipped. "
             "Exactly **0.60** enters review. Defects warn at **0.60 ≤ p < 0.80** and fail at **p ≥ 0.80**.",
             "Skipped scopes and missing evidence are unverified; they do not claim a clean content review.", ""]
    packs = defaultdict(Counter)
    for row in coverage:
        if row.get("rule") and row.get("status") in ("evaluated", "not_evaluated"):
            packs[row.get("pack") or "unspecified"][row["status"]] += 1
    if packs:
        lines += ["| Content pack | Evaluated propositions | Evidence gaps |", "|---|---:|---:|"]
        for pack, counts in sorted(packs.items()):
            lines.append(f"| {safe(pack)} | {counts['evaluated']} | {counts['not_evaluated']} |")
        lines.append("")
    provenance = source_records(content.get("provenance", []))
    lines += ["**Repository sources:** " + source_summary(content.get("provenance", [])) + ".", ""]
    if provenance:
        lines += ["<details><summary>Scoped repository evidence</summary>", "",
                  "Repository assertions and source observations are not independent verification. Full provenance is retained in JSON.", "",
                  "| Path | Revision | Scope | Evidence codes |", "|---|---|---|---|"]
        for source in provenance[:12]:
            revision = str(source.get("commit", source.get("revision", "unspecified")))[:12]
            scope = str(source.get("scope", "file"))
            if source.get("start_line") is not None:
                scope += f"; lines {source['start_line']}–{source.get('end_line', source['start_line'])}"
            codes = source.get("codes", [])
            code_text = ", ".join(map(str, codes)) if isinstance(codes, list) else str(codes)
            lines.append(f"| {safe(source.get('path', source.get('file', 'unspecified')), 250)} | {safe(revision)} | {safe(scope, 250)} | {safe(code_text, 100) or '—'} |")
        if len(provenance) > 12:
            lines += ["", f"{len(provenance) - 12} additional evidence unit(s); see JSON for full scope and provenance."]
        lines += ["", "</details>", ""]
    omission_rows = omission_groups(content.get("omissions", []))
    if omission_rows:
        lines += ["<details><summary>Evidence collection limits and unavailable sources</summary>", "",
                  "Missing automatically probed conventional files do not require repository setup. Applicable rules still need their stated evidence.", "",
                  "| Reason | Occurrences | Example paths |", "|---|---:|---|"]
        for reason, paths, count in omission_rows[:8]:
            examples = ", ".join(safe(path, 250) for path in paths[:3])
            if len(paths) > 3:
                examples += f"; {len(paths) - 3} more paths"
            lines.append(f"| {safe(reason, 300)} | {count} | {examples} |")
        if len(omission_rows) > 8:
            lines += ["", f"{len(omission_rows) - 8} additional reason(s); see JSON."]
        lines += ["", "</details>", ""]
    for key in ("sources", "missing_sources", "eligibility", "reason"):
        if content.get(key) is not None:
            lines += [f"**{safe(key)}:** {safe(content[key])}", ""]
    if gaps:
        lines += ["<details><summary>Content evidence gaps (scoped, unverified)</summary>", ""]
        for row in gaps[:15]:
            scope = "; ".join(f"{key}: {source_summary(row[key]) if key == 'provenance' else safe(row[key])}" for key in
                              ("file", "rule", "instance", "context", "reason", "requires", "missing_sources", "provenance")
                              if row.get(key) is not None)
            lines.append(f"- {scope or 'Required evidence unavailable'}")
        if len(gaps) > 15:
            lines.append(f"- {len(gaps) - 15} additional scoped gaps; see the JSON report and individual content checks.")
        lines += ["", "</details>", ""]
    return lines


def markdown(report: Report) -> str:
    fails = sum(f.severity == FAIL for f in report.findings)
    warns = len(report.findings) - fails
    head = "❌ **Failed**" if report.failed else "✅ **Passed**"
    lines = [MARKER, f"## rewardguard: {head}", "",
             f"{fails} fail · {warns} warn · {len(report.errors)} error", ""]
    lines += _content_markdown(report.content)
    if report.usage:
        lines += ["### Jev input usage", "", "| Phase | Responses | Reported input tokens | Missing usage | State characters | Question characters |",
                  "|---|---:|---:|---:|---:|---:|"]
        for phase, u in sorted(report.usage.items()):
            lines.append(f"| {safe(phase)} | {u['requests']} | {u['input_tokens']} | {u['usage_missing']} | {u['state_characters']} | {u['question_characters']} |")
        lines += ["", "| Phase | HTTP attempts | Serialized request bytes | Cache hits | Budget denials |",
                  "|---|---:|---:|---:|---:|"]
        for phase, u in sorted(report.usage.items()):
            lines.append(f"| {safe(phase)} | {u.get('attempts', 0)} | {u.get('request_bytes', 0)} | {u.get('cache_hits', 0)} | {u.get('budget_denials', 0)} |")
        stage_rows = [(phase, stage, s) for phase, u in sorted(report.usage.items())
                      for stage, s in sorted(u.get('stages', {}).items())]
        if stage_rows:
            lines += ["", "| Phase / stage | Attempts | Request bytes | Responses | Reported input tokens | Missing usage | Cache hits | Budget denials |",
                      "|---|---:|---:|---:|---:|---:|---:|---:|"]
            for phase, stage, s in stage_rows:
                lines.append(f"| {safe(phase)} / {safe(stage)} | {s['attempts']} | {s['request_bytes']} | {s['requests']} | {s['input_tokens']} | {s['usage_missing']} | {s['cache_hits']} | {s['budget_denials']} |")
        lines += ["", "Attempts and request bytes include retries and failed calls; cache hits send no request. "
                  "Bytes are not tokens or billing. Reported tokens may be incomplete if responses lack usage or requests fail.", ""]
    if report.errors:
        lines += ["### Errors", ""] + [f"- {safe(e, 300)}" for e in report.errors] + [""]
    if report.findings:
        lines += ["| Severity | Rule | Where | Detail |", "|---|---|---|---|"]
        for f in sorted(report.findings, key=lambda x: (x.source != "content", x.severity != FAIL, x.file or "", x.line or 0)):
            p = f" (p={f.probability!r})" if f.probability is not None else ""
            detail = safe(f.message)
            if f.evidence:
                detail += "<br>" + safe(f.evidence, 160)
            for d in f.details or []:
                detail += f"<br>line {safe(d['line'])}: {safe(d['problem'])} Fix: {safe(d['fix'])}"
            if f.details == []:
                detail += "<br>Haiku found no specific lines; review this chunk by hand"
            where = safe(_loc(f)) if f.file else "—"
            lines.append(f"| {safe(f.severity)} | {safe(f.rule)}{p} | {where} | {detail} |")
        lines.append("")
    if report.notes:
        lines += [safe(n) + "  " for n in report.notes]
    return "\n".join(lines) + "\n"


def as_json(report: Report) -> str:
    return json.dumps({
        "failed": report.failed,
        "errors": report.errors,
        "findings": [f.to_dict() for f in report.findings],
        "notes": report.notes,
        "content": report.content,
        "usage": report.usage,
    }, indent=2)
