# Whole-repository scan

`scripts/rewardguard_scan.py` reviews a Git checkout in context-sized groups and writes source-backed findings to CSV. It uses Python's standard library and supports source, test, configuration, and documentation files across common languages.

## Run

Preview the scan boundary without calling a judge:

```sh
python3 scripts/rewardguard_scan.py --repo-root . --output rewardguard-findings.csv --plan
```

Run the review with the configured Codex CLI:

```sh
python3 scripts/rewardguard_scan.py --repo-root . --output rewardguard-findings.csv
```

The default judge is `codex exec`, using the user's Codex configuration in a read-only sandbox from an empty temporary working directory. The judge receives only the bounded JSON request and is told not to inspect the filesystem. A complete run reviews every included unit, performs a synthesis pass over repository summaries and findings, validates every reported path, line range, and evidence excerpt, then atomically replaces the output CSV. A complete scan with no findings creates a header-only CSV. Failures leave an existing CSV untouched.

`--output` must be a `.csv` file inside the repository or the current directory; any other path is refused before anything is read.

Use `--max-context-bytes` to change the per-call payload limit and `--max-file-bytes` to change the maximum accepted size for one file. If a file or synthesis group cannot fit, the scan fails with a clear error rather than silently dropping content. `--timeout` sets the per-call judge timeout.

## Judge adapter

Set `REWARDGUARD_JUDGE_COMMAND` or pass `--judge-command` to use another judge. The command is split into arguments without a shell, runs with the repository as its working directory, receives one JSON request on stdin, and must write one JSON response to stdout. It must handle two request modes:

- `review`: `units` contains source text with exact line bounds; `repo_map` contains metadata; `expected_unit_ids` lists the units that must be covered.
- `synthesis`: `summaries`, `repo_map`, and validated `candidate_findings` are supplied for cross-component review.

Both responses must have exactly this shape:

```json
{
  "reviewed_unit_ids": ["each expected unit ID exactly once"],
  "summary": "A concise summary for the next synthesis pass",
  "findings": []
}
```

Each finding must contain `severity` (`critical`, `high`, `medium`, `low`, or `info`), `category`, numeric `confidence` from 0 to 1, `title`, `description`, `file`, 1-based inclusive `line_start` and `line_end`, exact `evidence`, `recommendation`, and `related_files`. Extra, missing, ungrounded, or out-of-scope fields fail the scan. A custom adapter is trusted code and runs with the invoking user's permissions.

## Scan boundary

The scanner uses `git ls-files` to include tracked files and nonignored untracked files. A fail-closed allowlist admits recognized source, test, config, and documentation types. It always excludes CSV, database and model artifacts, secrets and private keys, lockfiles, symlinks (including files under a symlinked directory), unknown types, generated-file markers, minified bundles, and common dependency, build, cache, and output directories. The requested output path is excluded even if it has a normally reviewable extension. Unreadable allowlisted files or files larger than the configured limit fail the scan; binary or non-UTF-8 files are excluded and listed in `--plan` output.

Review units split at complete line boundaries, and component findings must stay within the lines actually sent to the judge. Python imports and top-level declarations are summarized with the standard-library AST; other languages use path, role, and extension metadata. The synthesis pass uses summaries rather than resending the full repository source.
