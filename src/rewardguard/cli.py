from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from . import __version__, config, gitops, judge, report, runner, static_checks
from .models import Report, RewardGuardError


def _description(args) -> str:
    if args.description:
        return args.description
    if args.description_file:
        return Path(args.description_file).read_text()
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if event_path and Path(event_path).exists():
        event = json.loads(Path(event_path).read_text())
        pr = event.get("pull_request") or {}
        return f"{pr.get('title', '')}\n\n{pr.get('body') or ''}".strip()
    return ""


def check(args) -> int:
    repo = str(Path(args.repo).resolve())
    rep = Report()
    log = (lambda *_: None) if args.quiet else (lambda m: print(m, file=sys.stderr))

    try:
        if gitops.is_dirty(repo) and not args.allow_dirty:
            raise RewardGuardError("Uncommitted changes in tracked files. Commit or stash them; "
                                   "rewardguard checks committed history only.")
        head = gitops.rev_parse(repo, args.head)
        base = gitops.merge_base(repo, gitops.rev_parse(repo, args.base), head)
        cfg = config.load_from_commit(repo, base)
    except RewardGuardError as e:
        rep.errors.append(str(e))
        return _finish(rep, args)

    rep.notes.append(f"base {base[:12]} (merge-base with {args.base}), head {head[:12]}; config read from base")
    changed = gitops.changed_files(repo, base, head)
    if not changed:
        rep.notes.append("No changes between base and head.")
        return _finish(rep, args)

    log("rewardguard: static checks")
    findings, kinds = static_checks.run(static_checks.StaticContext(repo, base, head, cfg), changed)
    rep.findings.extend(findings)

    log("rewardguard: Jev judge")
    try:
        client = judge.JevClient(cfg)
        rep.findings.extend(judge.run(repo, base, head, cfg, changed, kinds, _description(args), client, log))
        if client.models_seen:
            rep.notes.append("Jev model: " + ", ".join(sorted(client.models_seen)))
    except RewardGuardError as e:
        rep.errors.append(f"Judge: {e}")

    log("rewardguard: test runs")
    try:
        rep.findings.extend(runner.run(repo, base, head, cfg, log))
    except RewardGuardError as e:
        rep.errors.append(f"Test run: {e}")

    return _finish(rep, args)


def _finish(rep: Report, args) -> int:
    print(report.terminal(rep))
    if args.markdown:
        Path(args.markdown).write_text(report.markdown(rep))
    if args.json:
        Path(args.json).write_text(report.as_json(rep))
    if rep.errors:
        return 2
    return 1 if rep.failed else 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="rewardguard", description="Detect reward hacking by AI coding agents on a branch.")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="Check the branch against its base")
    c.add_argument("--base", default="main", help="Base branch or commit (default: main)")
    c.add_argument("--head", default="HEAD", help="Commit to check (default: HEAD)")
    c.add_argument("--repo", default=".", help="Repository path (default: .)")
    c.add_argument("--description", help="PR description text, used to judge changed expected values")
    c.add_argument("--description-file", help="File containing the PR description")
    c.add_argument("--markdown", help="Write a Markdown report here")
    c.add_argument("--json", help="Write a JSON report here")
    c.add_argument("--allow-dirty", action="store_true",
                   help="Run even with uncommitted changes (they are NOT checked)")
    c.add_argument("--quiet", action="store_true")
    args = p.parse_args(argv)
    if args.cmd == "check":
        return check(args)
    return 2


if __name__ == "__main__":
    sys.exit(main())
