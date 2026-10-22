# reward-hacking-checker
A pre-commit and pre-merge check for reward hacking behavior in AI coding agents using decision models.

`rewardguard` checks a branch against its base and fails if an AI coding agent may have gamed its tests: deleting or skipping them, weakening assertions, editing expected values to match a bug, hard-coding answers, swallowing errors, or leaving notes aimed at the checker. It supports **Jest, Vitest and Playwright** projects. **Jev** (TypeSafe) is the judge and only answers yes/no questions; **Claude Haiku** then explains each chunk Jev flags.

The same tool runs locally and as a GitHub Action.

## How it works

Every run has three layers. Configuration is always read from the **base** commit, so a branch can't loosen its own check.

1. **Static checks.** Pattern and count rules on the diff. Counting is done in code because Jev counts unreliably.
2. **Jev judge.** Each changed file's diff is split into chunks that fit Jev's 32k-token state limit. Each chunk is asked yes/no (`noul`) questions. A probability at or above `fail` fails the check; at or above `warn`, it warns. When a PR description is available, Jev is also asked whether it claims work the whole diff doesn't contain.
3. **Haiku explainer.** Every chunk Jev flags is sent to Claude Haiku (`claude-haiku-5-5`) with the statements Jev judged true. It runs through the `claude` CLI (`claude -p`), billed to your Claude subscription via `CLAUDE_CODE_OAUTH_TOKEN`; `ANTHROPIC_API_KEY` is removed from the CLI's environment so it can't bill the API instead. The CLI runs with no tools, no project settings and no MCP servers. Haiku returns the line, the code, the problem and a fix for each one, and these appear in the report. Haiku only explains: it can't clear or downgrade a Jev finding. If it finds no matching lines, the report says to review that chunk by hand.
4. **Test runs.** Each suite runs in clean git worktrees:
   - **base:** the base commit as-is
   - **head:** the branch, with test-runner config restored from base
   - **original:** the branch's code against the base branch's test files
   - **new-vs-base:** the branch's test files against the base code (only when application code changed), to find new tests that pass without the change

**Fail-closed.** If Jev returns an HTTP error, a malformed answer or a missing answer, the check fails. So does a `claude` CLI failure, an error result or a missing structured answer from Haiku. It also fails if the Jev key, the Claude token or the `claude` CLI is missing, a suite writes no report, or the config is invalid. There is no fallback. Jev retries happen only on HTTP 429/5xx, at most 3 times. Test commands never see `TYPESAFE_API_KEY`, `CLAUDE_CODE_OAUTH_TOKEN`, `ANTHROPIC_API_KEY` or GitHub tokens.

Exit codes: `0` pass (warnings allowed), `1` failed, `2` error.

## What it catches

| Rule | Layer | Default |
|---|---|---|
| `TEST_FILE_DELETED`, `TEST_COUNT_DROP` | static | fail |
| `SKIP_ADDED` (`.skip`, `xit`, `.todo`, `test.fixme`, `test.fail`, `it.fails`) | static | fail |
| `ONLY_ADDED` (`.only`, `fit`) | static | fail |
| `TAUTOLOGICAL_ASSERTION` (`expect(true)…`, `expect(x).toBe(x)`) | static | fail |
| `EARLY_EXIT`, `DEAD_BRANCH` in tests | static | fail |
| `PASS_WITH_NO_TESTS`, `CONFIG_CHANGED`, `TEST_SCRIPT_CHANGED` | static | fail |
| `CHECKER_CONFIG_CHANGED` (`.github/**`, `.rewardguard.toml`) | static | fail |
| `REVIEWER_NOTE` (text addressed to a reviewer/AI) | static | fail |
| `ASSERTION_COUNT_DROP`, `SNAPSHOT_CHANGED`, `EMPTY_CATCH`, `TYPE_ESCAPE`, `TEST_ENV_BRANCH`, `MOCK_IN_SOURCE` | static | warn |
| `COVERAGE_IGNORE` (`istanbul`/`c8`/`v8 ignore`), `LOG_SILENCED`, `TIMEOUT_CHANGED`, `FIXED_WAIT`, `DEPENDENCY_DOWNGRADE` | static | warn |
| `NO_TESTS_RAN`, `RUN_TEST_TOTAL_DROP`, `RUN_SKIPPED_INCREASE`, `NEW_FAILURES` | run | fail |
| `ORIGINAL_TESTS_FAIL` (base tests fail against the branch's code) | run | warn |
| `PREEXISTING_FAILURES` | run | warn |
| `NEW_TESTS_PASS_ON_BASE` (new tests pass on the base code, so they don't test the change) | run | warn |
| `WEAKENED_ASSERTION`, `NEUTRALIZED_TEST`, `TEST_REPLACED_EASIER`, `MOCKS_CODE_UNDER_TEST`, `GRADER_TAMPERING` | Jev | by threshold |
| `EXPECTED_VALUE_CHANGED` (fails only if app code also changed and the PR description doesn't justify it) | Jev | by threshold |
| `OVER_MOCKING`, `ASSERTS_ON_MOCK`, `RECOMPUTED_EXPECTED`, `NO_OUTCOME_ASSERTION`, `TEST_NAME_MISMATCH`, `FLAKE_MASKING` | Jev | by threshold |
| `HARDCODED_OUTPUT`, `SPECIAL_CASED_INPUTS`, `SWALLOWED_ERROR`, `FAKE_SUCCESS`, `MOCK_DATA_AT_RUNTIME`, `UNSAFE_RETRY`, `STUB_IMPLEMENTATION`, `TYPE_SAFETY_BYPASS`, `TIMING_TAMPER`, `REVIEWER_INJECTION` | Jev | by threshold |
| `SECURITY_CHECK_DISABLED`, `UNREACHABLE_CHANGE`, `TEST_DATA_AT_RUNTIME`, `LOG_SUPPRESSION`, `DELAY_MASKING`, `LIMIT_RAISED` | Jev | by threshold |
| `DESCRIPTION_OVERCLAIM` (PR description claims work the diff doesn't contain) | Jev | by threshold |
| `DESCRIPTION_NOT_VERIFIED` (diff too large to check against the description in one call) | Jev | warn |

You can set any rule to `fail`, `warn` or `off` under `[rules]`.

## Setup

1. Copy [`examples/.rewardguard.toml`](examples/.rewardguard.toml) to your project root, set your test command, and commit it to `main`.
2. Get a TypeSafe API key. Install the Claude Code CLI (`npm install -g @anthropic-ai/claude-code`, v2.1.293 or later) and run `claude setup-token` to create a one-year subscription token (Pro, Max, Team or Enterprise plan). Subscription rate limits apply.

### Local

```bash
pipx install git+https://github.com/Advanced-Digital-Marketing-LTDA/reward-hacking-checker.git
export TYPESAFE_API_KEY=...
export CLAUDE_CODE_OAUTH_TOKEN=...   # from `claude setup-token`
git commit -am "wip"              # it checks committed history only
rewardguard check --base main
rewardguard check --base main --description "PR text" --markdown report.md --json report.json
```

### GitHub Action

1. Add `TYPESAFE_API_KEY` and `CLAUDE_CODE_OAUTH_TOKEN` as repository secrets. The Action installs the Claude Code CLI itself; the workflow needs Node (the example sets up Node 22).
2. Copy [`examples/rewardguard.yml`](examples/rewardguard.yml) to `.github/workflows/`.
3. In branch protection, make the `rewardguard` check **required**.
4. Add a `CODEOWNERS` rule that requires your review for `/.github/` and `/.rewardguard.toml`. A `pull_request` workflow runs from the PR's own copy of the workflow file, so this review requirement is what stops an agent from editing the check away. `CHECKER_CONFIG_CHANGED` also fails any PR that touches these files.

The Action writes the report to the job summary and posts or updates one PR comment.

## Calibrating

The default thresholds (`fail = 0.8`, `warn = 0.5`) are a starting point. Before relying on them:

1. Run against branches that cheat on purpose; [`tests/test_cheat_branches.py`](tests/test_cheat_branches.py) has 14 ready-made ones.
2. Run against a set of honest PRs.
3. Adjust the thresholds in `.rewardguard.toml` on `main`.

Pin the Jev model version (`jev-latest` is rejected). The model that actually answered is printed in each report.

## Not included yet

- Mutation testing
- Tests kept hidden from the agent (holdout tests)

Either can be added as another `[[suites]]` entry whose command lives outside the agent's reach.

## Development

```bash
pip install -e ".[dev]"
python -m pytest -q      # needs Node 22+ and npm; Jev and Haiku APIs are faked in tests
```
