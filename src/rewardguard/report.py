from __future__ import annotations

import json
from collections import Counter, defaultdict

from .content_checks import safe, source_records, source_summary, omission_groups

from .models import FAIL, Report

MARKER = "<!-- rewardguard-report -->"

# Exact internal reason strings map to fixed labels. Unknown text is never
# copied into diagnostics, even if a caller supplies a branch-authored reason.
_OMISSION_REASONS = {
    'Unsafe or excluded repository path': 'excluded_path',
    'Repository evidence excluded by path safety or content.evidence_exclude': 'excluded_path',
    'File not available at revision': 'unavailable_at_revision',
    'Blob exceeds 160000 byte read limit': 'blob_read_limit',
    'Binary or undecodable blob': 'binary_or_undecodable',
    'Whole evidence unit exceeds per-file or remaining total budget': 'unit_budget',
    'Whole relevant configured section exceeds per-file allowance': 'configured_section_budget',
    'No whole relevant configured Markdown unit admitted': 'configured_unit_unavailable',
    'Artifact-dependent installed-skill relevance analysis unavailable: proposed source not available': 'artifact_unavailable',
    'Local policy-reference discovery capped at 30 candidate documents': 'policy_discovery_limit',
    'Business-context allowance exhausted; writing-policy space reserved': 'business_context_budget',
    'Relevant whole section exceeds per-document budget': 'document_budget',
    'Automatic documentation scan capped at 16 documents': 'document_scan_limit',
    'Automatic documentation candidate limit; some candidate documents unscanned': 'document_candidate_limit',
    'Local-link inventory prioritization unavailable: proposed source not available': 'artifact_unavailable',
    'File inventory capped at 40 paths': 'inventory_limit',
    'Changed-line anchor collection capped at 200 lines in this hunk; primary diff remains independent': 'changed_anchor_limit',
    'Whole-section selection capped at 200 changed-line anchors; primary diff remains independent': 'section_anchor_limit',
    'No whole changed source section fits the evidence budget; primary diff is supplied independently': 'source_section_unavailable',
    'Full artifact exceeds source budget; only admitted whole sections are supplied': 'artifact_budget',
    'Static HTML observations capped at 80': 'html_observation_limit',
    'Static import discovery unavailable: affected source not available': 'artifact_unavailable',
    'Related-section relevance analysis unavailable: affected source not available': 'artifact_unavailable',
    'Full related source exceeds per-file budget; only whole sections defining referenced symbols may be supplied': 'related_source_budget',
    'Related-source collection capped at 6 files': 'related_source_limit',
    'Git history metadata capped at five commits; additional older history exists': 'history_limit',
}
_GAP_REASONS = {
    'Relevant check lacks specific supporting evidence after repository discovery': 'missing_evidence_after_discovery',
    'Supplied sources do not establish this specific target/claim or required condition': 'insufficient_target_evidence',
    'No textual source; binary/visual evidence is unavailable': 'binary_or_no_text',
}


def evidence_diagnostics(content: dict) -> dict:
    """Summarize coverage and omitted units without retaining source text or paths."""
    counts = dict.fromkeys(('eligible', 'evaluated', 'skipped', 'not_applicable', 'not_evaluated', 'unchanged', 'unknown'), 0)
    gaps = Counter()
    for row in content.get('coverage', []):
        status = row.get('status') if isinstance(row, dict) else None
        counts[status if isinstance(status, str) and status in counts else 'unknown'] += 1
        if status == 'not_evaluated':
            reason = row.get('reason')
            gaps[_GAP_REASONS.get(reason, 'unknown') if isinstance(reason, str) else 'unknown'] += 1
    reasons = Counter()
    for row in content.get('omissions', []):
        reason = row.get('reason') if isinstance(row, dict) else None
        label = _OMISSION_REASONS.get(reason, 'other_or_unknown') if isinstance(reason, str) else 'other_or_unknown'
        reasons[label] += 1
    status = content.get('status')
    return {'status': status if status in ('reviewed', 'skipped', 'not_evaluated', 'error') else 'unknown',
            'coverage': counts, 'omission_count': sum(reasons.values()),
            'omission_reasons': dict(sorted(reasons.items())), 'not_evaluated_reasons': dict(gaps)}


def _diagnostics(report: Report) -> dict:
    return {**report.diagnostics, 'provider_cache_accounting': 'only when explicitly returned per response; otherwise unavailable',
            'evidence': evidence_diagnostics(report.content)}


def _loc(f) -> str:
    if not f.file:
        return ""
    return f"{f.file}:{f.line}" if f.line else f.file


def status(report: Report) -> str:
    if report.errors:
        return 'error'
    rows = [*report.content.get('coverage', []), *report.code.get('coverage', [])]
    if any(r.get('status') in {'not_evaluated', 'error'} or r.get('result_complete') is False
           for r in rows):
        return 'incomplete'
    if report.failed:
        return 'failed'
    if not report.findings and not any(r.get('status') == 'evaluated' for r in rows):
        return 'skipped'
    return 'passed'


def scope_counts(report: Report) -> dict:
    rows = [*report.content.get('coverage', []), *report.code.get('coverage', [])]
    known = {'evaluated', 'eligible', 'skipped', 'excluded', 'not_applicable', 'not_evaluated', 'unchanged', 'error'}
    counts = Counter(r.get('status') if r.get('status') in known else 'unknown' for r in rows)
    counts['reused'] = sum(r.get('reused') is True for r in rows)
    counts['explanation_not_evaluated'] = sum(r.get('explanation_status') == 'not_evaluated' for r in rows)
    return dict(counts)


def terminal(report: Report) -> str:
    out = []
    if report.run_identity:
        out.append('run    ' + ' '.join(f'{key}={value}' for key, value in report.run_identity.items()))
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
        if u.get('explanations'):
            out.append('usage  ' + phase + ' explanations: ' + json.dumps(u['explanations'], sort_keys=True))
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
    diagnostic = _diagnostics(report)
    evidence = diagnostic['evidence']
    out.append('scope  content=' + evidence['status'] + ' ' +
               ' '.join(f'{key}={count}' for key, count in evidence['coverage'].items()))
    if evidence['omission_count']:
        out.append('scope  omitted evidence units=' + str(evidence['omission_count']) + ': ' +
                   ', '.join(f'{key}={count}' for key, count in evidence['omission_reasons'].items()))
    if evidence['not_evaluated_reasons']:
        out.append('scope  not evaluated reasons: ' +
                   ', '.join(f'{key}={count}' for key, count in sorted(evidence['not_evaluated_reasons'].items())))
    for event in diagnostic.get('events', []):
        out.append('diag   ' + json.dumps(event, sort_keys=True, separators=(',', ':')))
    out.append(f"diag   {len(diagnostic.get('events', []))} request/cache events, "
               f"{diagnostic.get('events_dropped', 0)} events dropped; provider cache accounting "
               'only when explicitly returned per response; otherwise unavailable')
    fails = sum(f.severity == FAIL for f in report.findings)
    warns = len(report.findings) - fails
    out.append('scope  ' + json.dumps(scope_counts(report), sort_keys=True))
    out.append('cache  completed content results=' + str(report.content.get('result_cache_hits', 0)) +
               '; partial Jev checkpoints=' + str(report.content.get('grade_cache_hits', 0)))
    verdict = status(report).upper()
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
    if isinstance(content.get('eligibility'), list):
        lines[3] = (f"Trusted publication eligibility: {len(content['eligibility'])} artifact(s); "
                    "determined locally without a probability. "
                    "Defects warn at **0.60 ≤ p < 0.80** and fail at **p ≥ 0.80**.")
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
    head = "**" + status(report).capitalize() + "**"
    lines = [MARKER, f"## rewardguard: {head}", "",
             f"{fails} fail · {warns} warn · {len(report.errors)} error", ""]
    lines += ['**Reviewed snapshot:** ' + safe(json.dumps(report.run_identity, sort_keys=True)), '',
              '**Scope:** ' + safe(json.dumps(scope_counts(report), sort_keys=True)), '',
              'Authenticated content results reused: ' + str(report.content.get('result_cache_hits', 0)) +
              '; partial Jev grade checkpoints: ' + str(report.content.get('grade_cache_hits', 0)) + '.', '',
              'Unchanged scopes have no new work; missing explanations preserve the original grade. '
              'Source observations do not prove runtime behavior.', '']
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
    for phase, usage in sorted(report.usage.items()):
        if usage.get('explanations'):
            lines += ['**' + safe(phase) + ' explanations:** ' + safe(json.dumps(usage['explanations'], sort_keys=True)), '']
    limitations = [r for r in [*report.content.get('coverage', []), *report.code.get('coverage', [])]
                   if r.get('explanation_status') == 'not_evaluated' or r.get('result_complete') is False]
    if limitations:
        lines += ['**Preserved grades with unfinished work:**', '']
        lines += ['- ' + safe(json.dumps({k: r[k] for k in ('file', 'rule', 'reason', 'explanation_status', 'result_complete', 'probability') if k in r}, sort_keys=True))
                  for r in limitations[:30]]
        lines += ['']
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
        "status": status(report),
        "scope": scope_counts(report),
        "failed": report.failed,
        "errors": report.errors,
        "findings": [f.to_dict() for f in report.findings],
        "notes": report.notes,
        "content": report.content,
        "code": report.code,
        "usage": report.usage,
        "run_identity": report.run_identity,
        "diagnostics": _diagnostics(report),
    }, indent=2)
