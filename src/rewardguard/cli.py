from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

from . import __version__, codex_hook, config, explainer, gitops, judge, report, runner, static_checks
from .models import CLEAR_CUT, FAIL, WARN, Finding, Report, RewardGuardError


def _run_identity(args, *, base=None, head=None, policy=None, cfg=None) -> dict:
    """Record only fixed event labels, resolved object IDs and versioned model IDs."""
    # Scope labels describe the report; they never decide which review paths run.
    events = {'pull_request', 'pull_request_target', 'push', 'workflow_dispatch',
              'workflow_call', 'schedule', 'merge_group', 'repository_dispatch'}
    actions = {'opened', 'synchronize', 'reopened', 'edited', 'closed', 'ready_for_review',
               'converted_to_draft', 'labeled', 'unlabeled', 'enqueued', 'dequeued',
               'checks_requested', 'destroyed', 'created', 'deleted'}
    def commit(value):
        return value.lower() if isinstance(value, str) and re.fullmatch(r'[0-9a-fA-F]{40}|[0-9a-fA-F]{64}', value) else 'unknown'
    def run_number(name):
        value = os.environ.get(name)
        return value if isinstance(value, str) and re.fullmatch(r'[1-9][0-9]{0,19}', value) else 'unknown'
    event = os.environ.get('GITHUB_EVENT_NAME')
    action = os.environ.get('REWARDGUARD_EVENT_ACTION')
    model = getattr(cfg, 'model', None)
    return {'event': event if event in events else 'unknown',
            'action': action if action in actions else 'unknown',
            'action_revision': commit(os.environ.get('REWARDGUARD_ACTION_REVISION')),
            'run_id': run_number('GITHUB_RUN_ID'), 'run_attempt': run_number('GITHUB_RUN_ATTEMPT'),
            'base': commit(base), 'head': commit(head), 'trusted_policy': commit(policy),
            'model': model if isinstance(model, str) and re.fullmatch(r'jev-[0-9]{1,6}\.[0-9]{1,6}\.[0-9]{1,6}', model) else 'unknown',
            'review_mode': 'staged' if getattr(args, 'staged', False) else
                           'content_only' if getattr(args, 'content_only', False) else 'full'}


def _description(args, *, head=None, notes=None) -> str:
    from . import pr_context
    return pr_context.resolve(args, head=head, notes=notes).text


def _resolve(repo: str, args):
    if getattr(args, "staged", False):
        base, head = gitops.staged_snapshot(repo)
        trusted_ref = gitops.default_base(repo, base)
        config_base = gitops.merge_base(repo, trusted_ref, base)
        args.config_base = config_base
        return base, head, config.load_from_commit(repo, config_base, allow_missing=True)
    if gitops.is_dirty(repo) and not args.allow_dirty:
        raise RewardGuardError("Uncommitted changes in tracked files. Commit or stash them; "
                               "rewardguard checks committed history only.")
    head = gitops.rev_parse(repo, args.head)
    selected = gitops.rev_parse(repo, args.base)
    explicit = getattr(args, 'comparison_mode', 'merge-base') == 'explicit'
    base = selected if explicit else gitops.merge_base(repo, selected, head)
    policy = getattr(args, 'policy_base', None)
    if explicit and not policy:
        raise RewardGuardError("Explicit comparisons require --policy-base from a trusted branch snapshot")
    args.config_base = gitops.rev_parse(repo, policy) if policy else base
    return base, head, config.load_from_commit(repo, args.config_base)


def _load_run_results(path: str, base: str, head: str) -> tuple[list[Finding], list[str]]:
    from .run_artifacts import load_local
    try:
        return load_local(path, base, head)
    except OSError as error:
        raise RewardGuardError(f"Cannot read run results: {error}") from error


def run_tests(args) -> int:
    """Runs only the test suites (branch code) and writes the results for `check --run-results`.
    Needs no secrets, so in CI it runs in a job that has none."""
    repo = str(Path(args.repo).resolve())
    log = (lambda *_: None) if args.quiet else (lambda m: print(m, file=sys.stderr))
    try:
        base, head, cfg = _resolve(repo, args)
    except RewardGuardError as e:
        print(f"ERROR  {e}", file=sys.stderr)
        return 2
    findings, errors = [], []
    if cfg.run_tests and gitops.changed_files(repo, base, head):
        log("rewardguard: test runs")
        try:
            findings = runner.run(repo, base, head, cfg, log)
        except RewardGuardError as e:
            errors.append(f"Test run: {e}")
    from .run_artifacts import identity
    Path(args.out).write_text(json.dumps({
        **identity(base, head, args.config_base), "findings": [f.to_dict() for f in findings], "errors": errors,
    }, indent=2))
    log(f"rewardguard: run results written to {args.out}")
    return 0


def check(args) -> int:
    repo = str(Path(args.repo).resolve())
    rep = Report(run_identity=_run_identity(args))
    from .usage import UsageTracker
    usage = UsageTracker()
    log = (lambda *_: None) if args.quiet else (lambda m: print(m, file=sys.stderr))

    try:
        base, head, cfg = _resolve(repo, args)
    except RewardGuardError as e:
        rep.errors.append(str(e))
        rep.content = {"status": "error", "coverage": [], "reason": "Review preflight failed: " + str(e)}
        return _finish(rep, args, usage)

    rep.run_identity = _run_identity(args, base=base, head=head,
                                     policy=getattr(args, 'config_base', base), cfg=cfg)

    if getattr(args, "staged", False):
        config_base = getattr(args, "config_base", base)
        if gitops.show_file(repo, config_base, config.CONFIG_FILE) is None:
            rep.notes.append(f"staged index against {base[:12]}; built-in global Codex defaults")
        else:
            rep.notes.append(f"staged index against {base[:12]}; config read from trusted base {config_base[:12]}")
    else:
        rep.notes.append(f"comparison base {base[:12]}, head {head[:12]}; trusted policy {args.config_base[:12]}")
    changed = gitops.changed_files(repo, base, head)
    if getattr(args, 'plan', False):
        from . import content_publications
        selected, excluded = [], []
        for cf in changed:
            kind = static_checks.classify(cf.path, cfg)
            row = {'path': cf.path, 'status': cf.status, 'kind': kind}
            (excluded if kind in {static_checks.OTHER, static_checks.CHECKER, static_checks.EXCLUDED} else selected).append(row)
        kinds = {cf.path: static_checks.classify(cf.path, cfg) for cf in changed}
        chunks = judge.build_chunks(repo, base, head, cfg, changed, kinds, '')
        plan = {'schema_version': 1, 'status': 'planned', 'run_identity': rep.run_identity,
                'content': content_publications.manifest(repo, base, head, cfg, changed),
                'code': {'selected': selected, 'excluded': excluded,
                         'units': [{'file': c.path, 'line': c.first_line, 'kind': c.kind,
                                    'text': c.body, 'anchors': c.anchors} for c in chunks],
                         'planned': ['static', 'independent code questions', 'context-dependent questions when available'],
                         'context': 'not fetched', 'cache_hits': 'unknown until authenticated execution'},
                'tests': 'required separately' if cfg.run_tests else 'disabled by trusted policy',
                'limitations': ['Source observations do not establish runtime behavior or model verdicts.']}
        payload = json.dumps(plan, indent=2)
        print(payload)
        if args.json:
            Path(args.json).write_text(payload)
        return 0
    if not changed:
        rep.notes.append("No changes between base and head.")
        rep.content = {"status": "skipped", "coverage": [], "reason": "No changes between base and head."}
        return _finish(rep, args, usage)

    # Resolve once so code/content classification, justification, confirmation,
    # and Haiku all see the same task context and provenance.
    from . import pr_context
    task_context = pr_context.resolve(args, repo=repo, base=base, head=head, notes=rep.notes)
    description = task_context.text

    # Content reads only Git objects and trusted-base evidence. Its gate precedes
    # client construction, so content-only non-content commits need no credentials.
    from . import content_review
    try:
        content = content_review.review(
            repo, base, head, cfg, changed, description,
            trusted_base=getattr(args, "config_base", base), log=log, usage=usage,
        )
        rep.findings.extend(content.findings)
        rep.notes.extend(content.notes)
        rep.content = content.to_dict()
        rep.errors.extend(content.errors)
    except RewardGuardError as e:
        rep.errors.append(f"Content review: {e}")
        rep.content = {"status": "error", "coverage": []}
    if getattr(args, "content_only", False):
        rep.usage = usage.snapshot()
        return _finish(rep, args, usage)

    log("rewardguard: static checks")
    found, kinds = static_checks.run(static_checks.StaticContext(repo, base, head, cfg), changed)

    if not cfg.run_tests:
        if getattr(args, "staged", False) and gitops.show_file(
                repo, getattr(args, "config_base", base), config.CONFIG_FILE) is None:
            rep.notes.append("Test runs are off (no .rewardguard.toml on HEAD); built-in defaults run static checks, Jev and Haiku")
        else:
            rep.notes.append("Test runs are off (run_tests = false in .rewardguard.toml): static checks, Jev and Haiku only")
    elif getattr(args, 'test_artifact', False):
        from .run_artifacts import load_authenticated
        try:
            run_findings, run_errors = load_authenticated(base, head, args.config_base)
            found.extend(run_findings)
            rep.errors.extend(run_errors)
            rep.notes.append('Test artifact origin/run/digest verified; provenance does not prove test honesty or effectiveness.')
        except (OSError, ValueError, RewardGuardError) as error:
            rep.errors.append(f'Test artifact unavailable or invalid: {error}')
    elif getattr(args, 'require_test_artifact', False):
        rep.errors.append('Test policy requires --test-artifact with authenticated origin')
    elif args.run_results:
        log(f"rewardguard: test results from {args.run_results}")
        try:
            run_findings, run_errors = _load_run_results(args.run_results, base, head)
            found.extend(run_findings)
            rep.errors.extend(run_errors)
        except RewardGuardError as e:
            rep.errors.append(str(e))
    elif args.no_local_tests:
        # CI's secrets job: branch code must never run here
        rep.errors.append("The base config has run_tests = true, but this run may not execute tests "
                          "(--no-local-tests). Run them in a separate job and pass --run-results.")
    else:
        log("rewardguard: test runs")
        try:
            found.extend(runner.run(repo, base, head, cfg, log))
        except RewardGuardError as e:
            rep.errors.append(f"Test run: {e}")

    # Clear-cut findings keep their fixed severity; Jev grades every other finding and judges every
    # changed file, and Haiku explains everything Jev reports
    log("rewardguard: Jev judge, Haiku explainer")
    try:
        from .review_cache import repository_identity
        repository = repository_identity(repo)
        client = judge.JevClient(cfg, usage=usage, phase="code", repository=repository)
        haiku = explainer.HaikuExplainer(cfg, usage=usage, repository=repository)
        result = judge.run(repo, base, head, cfg, changed, kinds, description, client, haiku, log,
                                  to_confirm=found, task_context_complete=task_context.scope_complete,
                                  full_task_diff=task_context.full_pr_diff)
        judged, notes = result
        rep.findings.extend(judged)
        rep.notes.extend(notes)
        rep.errors.extend(getattr(result, 'errors', []))
        rep.code = {'coverage': getattr(result, 'coverage', [])}
        rep.notes.append(f"Jev code: {client.cache_hits} authenticated request result(s) reused without API calls.")
        if client.models_seen:
            rep.notes.append("Jev model: " + ", ".join(sorted(client.models_seen)))
    except RewardGuardError as e:
        rep.findings.extend(f for f in found if f.rule in CLEAR_CUT)
        rep.errors.append(f"Judge: {e}")

    rep.usage = usage.snapshot()
    return _finish(rep, args, usage)


def _finish(rep: Report, args, usage=None) -> int:
    if usage is not None:
        rep.usage = usage.snapshot()
        rep.diagnostics = usage.diagnostics()
    # One failed output must not suppress the other or erase the original review errors.
    written = []
    original_errors = len(rep.errors)
    for filename, render in ((args.markdown, report.markdown), (args.json, report.as_json)):
        if filename:
            try:
                Path(filename).write_text(render(rep))
                written.append((filename, render))
            except (OSError, ValueError) as error:
                rep.errors.append(f"Report output {filename}: {error}")
    if len(rep.errors) != original_errors:
        for filename, render in written:
            try:
                Path(filename).write_text(render(rep))
            except (OSError, ValueError) as error:
                rep.errors.append(f"Report error reconciliation {filename}: {error}")
    print(report.terminal(rep))
    if rep.errors:
        return 2
    if getattr(args, 'require_complete', False) and report.status(rep) == 'incomplete':
        return 3
    return 1 if rep.failed else 0


def codex_precommit() -> int:
    """Codex PreToolUse entry point. Non-commit Bash calls pass through unchanged."""
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError) as e:
        print(f"rewardguard: could not read Codex hook event ({e}); skipped", file=sys.stderr)
        return 0

    if not isinstance(event, dict):
        return 0
    if event.get("hook_event_name") != "PreToolUse" or event.get("tool_name") != "Bash":
        return 0
    tool_input = event.get("tool_input")
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    cwd = event.get("cwd")
    if not isinstance(command, str) or not isinstance(cwd, str):
        return 0
    context = codex_hook.commit_context(command, cwd)
    if context is None:
        return 0
    repo, blocked_reason = context
    if blocked_reason is not None:
        print(
            f"rewardguard: commit blocked: {blocked_reason}. "
            "Stage changes in a separate Codex Bash call, then commit in another call.",
            file=sys.stderr,
        )
        return 2

    try:
        repo = gitops.git(repo, "rev-parse", "--show-toplevel").stdout.strip()
    except RewardGuardError as e:
        print(f"rewardguard: could not find repository root for commit check: {e}", file=sys.stderr)
        return 2

    print(f"rewardguard: checking staged changes before commit in {repo}", file=sys.stderr)
    args = argparse.Namespace(
        base="HEAD", head="HEAD", repo=str(repo), description=None, description_file=None,
        markdown=None, json=None, allow_dirty=False, staged=True, run_results=None,
        no_local_tests=False, quiet=False,
    )
    try:
        status = check(args)
    except Exception as e:
        print(f"rewardguard: precommit check errored: {e}", file=sys.stderr)
        return 2
    if status != 0:
        print("rewardguard: commit blocked; see the check report above", file=sys.stderr)
        return 2
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="rewardguard", description="Detect reward hacking by AI coding agents on a branch.")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="Check the branch against its base")
    c.add_argument("--base", default="main", help="Base branch or commit (default: main)")
    c.add_argument("--head", default="HEAD", help="Commit to check (default: HEAD)")
    c.add_argument("--repo", default=".", help="Repository path (default: .)")
    c.add_argument("--staged", action="store_true", help="Check the staged index against HEAD")
    c.add_argument("--require-complete", action="store_true",
                   help="Exit 3 when required review evidence/context is incomplete (used by CI)")
    c.add_argument("--plan", action="store_true", help="Print a local provider-free review manifest")
    c.add_argument("--content-only", action="store_true",
                   help="Run only content review; non-content changes skip without model credentials")
    c.add_argument("--title", help="PR title or task summary; combined with the description as review context")
    c.add_argument("--description", help="PR description or task requirements, used by code and content review")
    c.add_argument("--description-file", help="File containing the PR description")
    c.add_argument("--markdown", help="Write a Markdown report here")
    c.add_argument("--json", help="Write a JSON report here")
    c.add_argument("--allow-dirty", action="store_true",
                   help="Run even with uncommitted changes (they are NOT checked)")
    c.add_argument("--test-artifact", action="store_true", help="Verify same-run GitHub test artifact (actions:read)")
    c.add_argument("--require-test-artifact", action="store_true",
                   help="Require authenticated artifacts when trusted policy enables tests; never run tests or accept local results")
    c.add_argument("--run-results",
                   help="Use test results written by `rewardguard run-tests` instead of running the tests here")
    c.add_argument("--no-local-tests", action="store_true",
                   help="Never run tests in this process; fail if the base config needs test runs and "
                        "--run-results is not given")
    c.add_argument("--quiet", action="store_true")
    t = sub.add_parser("run-tests", help="Run only the test suites and write the results to a file")
    t.add_argument("--base", default="main", help="Base branch or commit (default: main)")
    t.add_argument("--head", default="HEAD", help="Commit to check (default: HEAD)")
    t.add_argument("--repo", default=".", help="Repository path (default: .)")
    t.add_argument("--out", required=True, help="Where to write the run results (JSON)")
    t.add_argument("--allow-dirty", action="store_true",
                   help="Run even with uncommitted changes (they are NOT checked)")
    t.add_argument("--quiet", action="store_true")
    for parser in (c, t):
        parser.add_argument('--comparison-mode', choices=('merge-base', 'explicit'), default='merge-base')
        parser.add_argument('--policy-base', help='Immutable trusted policy commit, required for explicit comparisons')
    sub.add_parser("codex-precommit", help="Run as a Codex PreToolUse hook for git commit commands")
    args = p.parse_args(argv)
    if args.cmd == "check":
        return check(args)
    if args.cmd == "run-tests":
        return run_tests(args)
    if args.cmd == "codex-precommit":
        return codex_precommit()
    return 2


if __name__ == "__main__":
    sys.exit(main())
