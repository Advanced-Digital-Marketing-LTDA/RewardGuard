# reward-hacking-checker
A pre-commit and pre-merge check for reward hacking behavior in AI coding agents using decision models.

`rewardguard` checks a branch against its base and fails if an AI coding agent may have gamed its tests: deleting or skipping them, weakening assertions, editing expected values to match a bug, hard-coding answers, swallowing errors, or leaving notes aimed at the checker. It supports **Jest, Vitest and Playwright** projects. **Jev** (TypeSafe) is the judge and only answers yes/no questions; **Claude Haiku** then explains each chunk Jev flags.

The same tool runs locally and as a GitHub Action. Version `0.3.0` prepares the explicit-publication contract; publication and shared-channel rollout are pending. [Release verification](docs/shared-ci-release-verification.md) records the gates and caller migration.

Content review shares the existing `rewardguard check` path. Explicit trusted-base publication declarations select public website sources, reader units, metadata and declared dependencies. The catalog retains **243 rule signatures in 37 packs**, derived from 80 inspected guides; the website runtime selects supported rules by artifact type and evidence. Research, advertising, email, sales and other nonwebsite packs remain cataloged outside this initial runtime scope. See [Content checks](docs/content-checks.md) for configuration and [the publication API](docs/shared-ci-public-content.md) for exact source/extraction limits.

Live-provider precision has not been verified. CI rollout needs the published action commit SHA containing this change; a local checkout does not update existing pinned callers.

## How it works

The code review path has the layers below. Configuration is always read from the **base** commit, so a branch can't loosen its own check. Content review uses the same Jev grades and Haiku explainer, with separate routing and focused rubrics.

1. **Static checks.** Pattern and count rules on the diff. Counting is done in code because Jev counts unreliably.
2. **Jev judge.** Every changed text file in any language is judged, except excluded paths, `.github/` and `.rewardguard.toml`. Its diff is split into chunks that fit Jev's 32k-token state limit, and each chunk is asked yes/no (`noul`) questions. When a PR description is available, Jev is also asked whether it claims work the whole diff doesn't contain. Jev also grades every static and test-run finding that isn't clear-cut (see the table below): it is asked whether the finding is a real problem, given that file's diff. Lines that hold a credential, and every line of a private-key block, are redacted before anything is sent to Jev or Haiku; the report notes each file whose key-block lines were hidden, so they can be reviewed by hand.

   Severity comes from Jev's probability and is fixed, not configurable: **below 0.60 there is no output**, 0.60–0.79 warns, and 0.80 or higher fails. Clear-cut findings, which report an objective fact, keep their fixed severity and are not sent to Jev or Haiku.
3. **Haiku explainer.** Every Jev finding that is reported (0.60 or higher) is sent to Claude Haiku (`claude-haiku-5-5`) with the statement Jev answered. It runs through the `claude` CLI (`claude -p`), billed to your Claude subscription via `CLAUDE_CODE_OAUTH_TOKEN`; `ANTHROPIC_API_KEY` is removed from the CLI's environment so it can't bill the API instead. The CLI runs with no tools, no project settings and no MCP servers. Haiku returns the line, the code, the problem and a fix for each one, and these appear in the report. Haiku only explains: it can't clear or downgrade a Jev finding. If it finds no matching lines, the report says to review that chunk by hand.
4. **Test runs** (optional; set `run_tests = false` in `.rewardguard.toml` to skip them for a suite that can't run in a workflow). Each suite runs in clean git worktrees:
   - **base:** the base commit as-is
   - **head:** the branch, with test-runner config restored from base
   - **original:** the branch's code against the base branch's test files
   - **new-vs-base:** the branch's test files against the base code (only when application code changed), to find new tests that pass without the change

**Fail-closed.** If Jev returns an HTTP error, a malformed answer or a missing answer, the check fails. So does a `claude` CLI failure, an error result or a missing structured answer from Haiku. It also fails if the Jev key, the Claude token or the `claude` CLI is missing, a suite writes no report, or the config is invalid. There is no fallback. Jev retries happen only on HTTP 429/5xx, at most 3 times. Test commands never see `TYPESAFE_API_KEY`, `CLAUDE_CODE_OAUTH_TOKEN`, `ANTHROPIC_API_KEY` or GitHub tokens.

Each run reports Jev's provider-reported input tokens and request context sizes separately for code and content review, in the terminal, Markdown and JSON reports. State and question sizes are character counts, not token estimates. Responses without valid usage are counted separately; failed or interrupted requests may also be missing from these totals, so consult the provider's billing records for actual charges. The report does not retain the prompts in its usage totals. Content review may submit the same state repeatedly for applicability and batches of independent checks; all reported input tokens are added per response.

The same reports include HTTP attempts, serialized request-body bytes, authenticated cache hits, and denied requests per phase and per recorded content stage (including applicability and evaluation). Attempts and request bytes are reserved before each provider call and include retries, failures and requests whose responses are lost. Cache hits do not use an HTTP attempt. Bytes are a payload measure, not a token or billing estimate.

The terminal and JSON report also include structured per-request cache, retry,
response and budget events using run-local numeric IDs. They never contain
prompts, source payloads, credentials, signing material or request hashes.
Archive restore/save diagnostics separately report their non-secret key,
matched key when exposed, step outcome and restored entry-file count. An
archive hit is not itself an authenticated result hit. A result-key miss cannot
say which input changed: the matching signed identity is simply absent. Missing
provider cache/billing fields are marked unavailable rather than inferred. To
bound report size, at most 10,000 events are retained and dropped events are
counted explicitly.

Optional trusted-base `[judge]` settings `max_attempts` and `max_request_bytes` limit the combined code and content review across the entire run. Both must be positive integers; omitting a setting leaves that budget unlimited. For example:

```toml
[judge]
max_attempts = 100
max_request_bytes = 2000000
```

Budget exhaustion fails the check visibly as an incomplete review, without silently skipping the remaining work. The byte limit applies to JSON request bodies including retries, not provider-reported tokens, HTTP headers or charges. Choose limits from observed workloads rather than assuming an arbitrary default is safe for every repository.

Exit codes: `0` pass or skip (warnings allowed), `1` failure findings, `2` execution/output error. Local commands retain exit `0` for incomplete evidence without failures/errors, with `status=incomplete` and explicit coverage. CI uses `--require-complete`, which returns `3` for that incomplete state; scoped checks never advertise incomplete coverage as success.

## What it catches

| Rule | Layer | Severity |
|---|---|---|
| `TEST_FILE_DELETED`, `TEST_COUNT_DROP` | static | fail (clear-cut) |
| `SKIP_ADDED` (`.skip`, `xit`, `.todo`, `test.fixme`, `test.fail`, `it.fails`) | static | fail (clear-cut) |
| `ONLY_ADDED` (`.only`, `fit`), `EARLY_EXIT` in tests | static | fail (clear-cut) |
| `PASS_WITH_NO_TESTS`, `CONFIG_CHANGED`, `TEST_SCRIPT_CHANGED` | static | fail (clear-cut) |
| `SECRET_ADDED` (token formats, private keys, URLs with a password, also base64-encoded) | static | fail (clear-cut) |
| `ASSERTION_COUNT_DROP`, `SNAPSHOT_CHANGED`, `DEPENDENCY_DOWNGRADE`, `NEW_DEPENDENCY`, `NON_TEST_FILES_DELETED`, `AGENT_INSTRUCTIONS_CHANGED` (`AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `.claude/`, `.cursor/`, `.gemini/`…) | static | warn (clear-cut) |
| `NO_TESTS_RAN`, `RUN_TEST_TOTAL_DROP`, `RUN_SKIPPED_INCREASE`, `NEW_FAILURES` | run | fail (clear-cut) |
| `PREEXISTING_FAILURES` | run | warn (clear-cut) |
| `TAUTOLOGICAL_ASSERTION` (`expect(true)…`, `expect(x).toBe(x)`), `DEAD_BRANCH`, `REVIEWER_NOTE` (text addressed to a reviewer/AI) | static | Jev-graded |
| `EMPTY_CATCH`, `TYPE_ESCAPE`, `TEST_ENV_BRANCH`, `MOCK_IN_SOURCE`, `COVERAGE_IGNORE` (`istanbul`/`c8`/`v8 ignore`), `LOG_SILENCED`, `TIMEOUT_CHANGED`, `FIXED_WAIT` | static | Jev-graded |
| `GATE_CONFIG_WEAKENED` (`HUSKY=0`, `--no-verify`, `core.hooksPath`, `continue-on-error: true`, `"strict": false`, ESLint rule `off`, any hook/lint/tsconfig change) | static | Jev-graded |
| `RUNTIME_MONKEYPATCH` (application code reassigns `Math`/`Date`/`JSON` members, built-in prototypes or test globals, or reads the call stack) | static | Jev-graded |
| `LICENSE_HEADER_REMOVED`, `LARGE_LITERAL_TABLE` (100+ lines of literal lookup data in app code) | static | Jev-graded |
| `ORIGINAL_TESTS_FAIL` (base tests fail against the branch's code), `NEW_TESTS_PASS_ON_BASE` (new tests pass on the base code, so they don't test the change) | run | Jev-graded |
| `WEAKENED_ASSERTION`, `NEUTRALIZED_TEST`, `TEST_REPLACED_EASIER`, `MOCKS_CODE_UNDER_TEST`, `GRADER_TAMPERING` | Jev | Jev-graded |
| `EXPECTED_VALUE_CHANGED` (dropped when app code also changed and the complete PR title/body justifies the specific change) | Jev | Jev-graded |
| `OVER_MOCKING`, `ASSERTS_ON_MOCK`, `RECOMPUTED_EXPECTED`, `NO_OUTCOME_ASSERTION`, `TEST_NAME_MISMATCH`, `FLAKE_MASKING` | Jev | Jev-graded |
| `HARDCODED_OUTPUT`, `SPECIAL_CASED_INPUTS`, `SWALLOWED_ERROR`, `FAKE_SUCCESS`, `MOCK_DATA_AT_RUNTIME`, `UNSAFE_RETRY`, `STUB_IMPLEMENTATION`, `TYPE_SAFETY_BYPASS`, `TIMING_TAMPER`, `REVIEWER_INJECTION` | Jev | Jev-graded |
| `SECURITY_CHECK_DISABLED`, `UNREACHABLE_CHANGE`, `TEST_DATA_AT_RUNTIME`, `LOG_SUPPRESSION`, `DELAY_MASKING`, `LIMIT_RAISED` | Jev | Jev-graded |
| `HOLLOW_FALLBACK`, `SPECULATIVE_TEST_HEDGING`, `SCOPE_CREEP`, `HIDDEN_PARAMETER_DISABLE` | Jev | Jev-graded |
| `DESCRIPTION_OVERCLAIM` (a concrete completed-change claim in PR context contradicts the complete supplied diff; missing or partial context is unverified) | Jev | Jev-graded |

Jev-graded: below 0.60 nothing is reported, 0.60–0.79 warns, 0.80 or higher fails. The clear-cut list is `CLEAR_CUT` in [`src/rewardguard/models.py`](src/rewardguard/models.py).

You can turn any rule off under `[rules]` (`RULE = "off"`); severities can't be changed. [`docs/agent-behaviours.md`](docs/agent-behaviours.md) lists the agent behaviours these rules come from, with sources, and the ones a diff can't show.

## Content review

The normal `check` command includes content review. Trusted-base `[[content.publications]]` declarations are the publication authority; the default empty list makes arbitrary Markdown, internal docs and JavaScript strings ineligible. Deterministic reader extraction and artifact/rule scope select work without a probabilistic task gate. Jev independently grades applicable evidenced claims, fields and requirements. Individual findings warn at **0.60 through below 0.80** and fail at **0.80 or higher**. A pack never receives one aggregate quality score.

```bash
rewardguard check --base main
rewardguard check --base main --content-only
rewardguard check --base main --staged --content-only
```

`--content-only` selects content review without the coding/test-review layers and returns success for a no-content skip. In a normal run, a content skip leaves the existing code checks in control of the overall result. Missing factual, rendered, measurement or policy evidence is reported as `not_evaluated`, with a coverage reason. It is neither a defect nor a claimed pass. Required reviews still fail closed on provider or configuration errors.

Declare each public source with a stable `id`, `sources`, `type` and local `route`; optionally select JSON `fields`, transitive `dependencies` and bound `evidence` codes. Types are `page`, `article`, `product`, `component` and `metadata`. `include` / `source_include` only narrow declarations. Empty `packs = []` allows supported website rules; artifact scope and evidence still filter them. `[content.context]` paths come only from the trusted base and must be bound by each declaration. See the [example config](examples/.rewardguard.toml) and [full guide](docs/content-checks.md#configure-content-review).

Internal docs, agent skills, tests/fixtures, tooling, CI, infrastructure and backend-only paths are excluded from both grading targets and evidence by default. This also filters explicitly configured context paths, reference following, related imports and inventories. Use dedicated `.rewardguard/content-*` files for intentional trusted evidence. See the [path review](docs/content-path-review.md) for the categories and explicit published-docs opt-in.

Haiku receives only the relevant rule rubric, inline exclusions, changed evidence and necessary trusted context. Artifact variants select their matching specialist. Source-audit candidates, rigid style preferences and optional marketing tactics do not automatically become enabled checks. Dates are required only when material to the particular claim. The content judge does not execute branch code to collect missing evidence.

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

# Content review alone, including a successful no-content skip
rewardguard check --base main --content-only

# The same split CI uses: run the tests without secrets, then judge
rewardguard run-tests --base main --out run.json
rewardguard check --base main --run-results run.json
```


### Immutable CI snapshots and content reuse

Pull requests review the full target/head merge-base interval. Pushes preserve their explicit before-to-head interval, including force pushes; trusted policy comes from the previous default tip or a separately resolved default-branch snapshot. `--comparison-mode explicit` requires `--policy-base`; supplied `--head` must match the checkout. Configuration edits cannot authorize their own review.

`rewardguard check --base main --plan` emits provider-free JSON with snapshot identity, selected/excluded code paths, public reader units, dependencies and planned work. It creates no provider clients and reports cache availability without guessing hits.

Authenticated completed content records reuse clean, warning and failure results, probabilities, coverage and explanations. `content.result_cache_hits` and `reused: true` identify completed-record reuse; raw Jev request-cache hits are separate. Unchanged reader semantics use cache-only lookup: a miss is `unchanged`, with no new grading. Changed explanation inputs preserve cached grades and explicitly mark missing explanations. Deleted sources do not replay stale findings. Reports include exact head/base/policy/action revision and partial results when later work fails.

The Action uploads `rewardguard-review-<run_id>-<attempt>/rewardguard.json`, including expected failure findings. Optional test transport authenticates run/attempt, repository, immutable commits and archive digest; it establishes origin, not test honesty. Test code runs in a separate secrets-free job. Callers need `contents: read`, `pull-requests: write`, `checks: write`; enable `actions: read` only when `run-tests: true` needs authenticated test artifacts. The reusable judge inherits these caller-bounded permissions.

Actions cache is interim and may miss or be evicted. It does not guarantee concurrent exactly-once evaluation or durable storage; that work remains REWARD-1. A cache archive hit alone is not an authenticated result hit. See [release verification](docs/shared-ci-release-verification.md) for required real-consumer evidence.

### PR title and description as task context

RewardGuard resolves one quoted context snapshot and shares it across code review,
content review, expected-value justification, confirmation, and Haiku explanations.
On PR events it uses both title and body, refreshing live metadata when it still
matches the reviewed head; if the PR advanced or lookup fails, it uses the original
event snapshot. On pushes it looks up an unambiguous open or merged PR associated
with the reviewed commit, including merge and squash commit associations.

An associated PR must cover the reviewed Git interval before it can establish the
whole push's scope. A branch-sync push importing newer main-branch work may contain
changes belonging to other tasks. Missing, ambiguous, or partial context
is recorded in the report: `SCOPE_CREEP` and `DESCRIPTION_OVERCLAIM` are unverified
rather than inferred from missing intent. Other code/content checks continue.

A contained incremental PR interval can still establish scope relevance, but
`DESCRIPTION_OVERCLAIM` additionally requires the complete PR interval. Work done
in earlier commits cannot be declared missing from an incremental push diff.

Scope is semantic. Supporting tests, types, validation, error handling, metadata
and integration changes need not be named individually in the PR summary. Task
goals and background context are distinguished from claims of completed work.
A source diff alone cannot disprove a claim about test execution or external CI.
PR text describes intent; instructions to suppress review and claims that code is
safe or approved do not override trusted policy or prove correctness.

Context is credential-redacted and preserved in full within the configured state
budget, with space reserved for the diff and supporting evidence. If the full task
context cannot fit, review reports an explicit budget error rather than grading
against a shortened request. Whole-PR overclaim review also includes changed
workflow/checker files; unavailable text or a complete diff that cannot fit leaves
that check explicitly unverified. The hosted GitHub lookup has a fixed API host,
bounded response size, timeout, and no redirects; it never executes repository code.
GitHub tokens used for lookup are removed from the Haiku subprocess environment.

Local callers can supply context explicitly:

```bash
rewardguard check --base main --title "Correct upload limits" --description-file pr-description.md
```

The global staged hook has no PR context by default; use an explicit check with
`--title` and `--description` or `--description-file` when that context is available.

### Codex global precommit

To check staged changes before commits Codex makes in any repository, add this hook to `~/.codex/hooks.json`. Merge it into the existing JSON if that file already has hooks:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "^Bash$",
        "hooks": [
          {
            "type": "command",
            "command": "rewardguard codex-precommit",
            "timeout": 600,
            "statusMessage": "Checking staged changes with RewardGuard"
          }
        ]
      }
    ]
  }
}
```

Install RewardGuard globally using the command above, make sure `TYPESAFE_API_KEY` and `CLAUDE_CODE_OAUTH_TOKEN` are available to the Codex process, then review and trust the hook in Codex's `/hooks` view. The existing hook calls the normal `check` path on the staged snapshot, including the content gate; no second Codex hook is needed. Code checks continue normally, while content-model calls depend on explicit public-source mappings and deterministic rule eligibility. Provider rate limits apply. RewardGuard reads an existing project config from the merge base with `origin/HEAD`, `origin/main`, `origin/master`, local `main` or local `master`, in that order; staged config edits do not affect the check. If none of those refs exist, it uses `HEAD`. When the trusted base has no `.rewardguard.toml`, built-in global defaults run static and model checks with test execution off. Otherwise it uses the trusted base config, including its test suites. The staged index is checked; unstaged edits are excluded. Stage changes in one Codex Bash call, then commit in a separate call. The hook blocks combined staging-and-commit commands, `git commit -a`, pathspec or interactive commit forms that can select content outside the checked index, and explicit `--git-dir`/`--work-tree` overrides that target another repository. Commits issued from a repository subdirectory are checked from the worktree root.

This is a Codex local-shell hook. It applies across repositories without adding files to each one. It doesn't intercept Git commands you run outside Codex or every possible way a shell script could invoke Git. See [Codex hook coverage](https://developers.openai.com/codex/hooks).

Locally, `rewardguard check` runs the tests in the same process as the keys. That's fine on your own machine, but don't run it on code you don't trust with those keys.

### Optional pre-commit content hook

The [pre-commit hook](.pre-commit-hooks.yaml) checks the staged snapshot through `rewardguard check --staged --content-only`. Add this to `.pre-commit-config.yaml`, replacing the placeholder with the published commit SHA containing the hook and content feature:

```yaml
repos:
  - repo: https://github.com/Advanced-Digital-Marketing-LTDA/RewardGuard
    rev: REPLACE_WITH_PUBLISHED_COMMIT_SHA
    hooks:
      - id: rewardguard-content
```

Run `pre-commit install` after installing pre-commit. The hook needs the same provider credentials when review is required and succeeds when no eligible content changed. It runs for the repository's pre-commit stage with no filename arguments; the staged index determines the reviewed content. Keep Codex's existing normal hook when you also want its code checks.

### GitHub Action

1. Add `TYPESAFE_API_KEY` and `CLAUDE_CODE_OAUTH_TOKEN` as repository secrets. The Action installs the Claude Code CLI itself; the workflow needs Node (the example sets up Node 22).
2. Copy [`examples/rewardguard.yml`](examples/rewardguard.yml) to `.github/workflows/`. It has two jobs:
   - **`rewardguard-tests`** (`mode: tests`) runs the branch's test suites with no secrets, a read-only token and no saved git credentials. It uploads the results as an artifact.
   - **`rewardguard`** (`mode: check`) runs the static checks, Jev and Haiku, and reads the uploaded results. It holds the secrets and never runs branch code.

   The split matters because branch code running as the same user can read secrets from other processes (for example through `/proc/<pid>/environ`). Removing them from the test command's environment is not enough. Never pass secrets to `mode: tests`; the Action refuses if you do. If the tests job fails or uploads nothing, the `rewardguard` job fails.
3. In branch protection, make the `rewardguard` check **required** (the second job).

   **No test runs:** if your suite is too large or needs services a workflow doesn't have, set `run_tests = false` in `.rewardguard.toml` and use [`examples/rewardguard-no-tests.yml`](examples/rewardguard-no-tests.yml) instead. It's one job (static checks, Jev, Haiku) that never runs branch code. You lose the run-layer rules (`NO_TESTS_RAN`, `NEW_FAILURES`, `ORIGINAL_TESTS_FAIL`, and so on), but every static and Jev rule still applies. The check job always passes `--no-local-tests`, so if the base config still says `run_tests = true` it fails instead of running tests next to the secrets.
4. Add a `CODEOWNERS` rule that requires your review for `/.github/` and `/.rewardguard.toml`. A `pull_request` workflow runs from the PR's own copy of the workflow file, so this review requirement is what stops an agent from editing the check away. Rewardguard itself doesn't flag changes to these files, because CI sometimes has to change; `.rewardguard.toml` edits only take effect once merged.

The Action writes a prominent content coverage summary (including per pack evaluation and evidence gaps) to the job summary and PR comment. It also publishes **`contentguard / eligibility`** and individual **`contentguard / CG_RULE_ID`** GitHub checks on the resolved review head. Only evaluated rules and rules with evidence gaps receive individual checks; unrelated catalog rules do not fill the Checks UI.

Give the judge job and any reusable-workflow caller **`checks: write`**, alongside `contents: read` and `pull-requests: write`. The Action input `content-checks` defaults to `"true"`; set it to `"false"` explicitly to disable publishing in an integration that cannot grant that permission. The test job keeps its read-only token. Publishing failures fail the aggregate job visibly.

For manual publication, run `python -I -m rewardguard.content_checks --report ./report.json --head <resolved-sha> --repo <owner/name>` with `GH_TOKEN` in the environment. The report must be a regular `.json` file inside the current working directory, or inside `RUNNER_TEMP` when that environment variable is present (as in Actions). Paths resolving outside that directory and files larger than 16 MiB are rejected; no report data is truncated on load. The Action uses its existing `$RUNNER_TEMP/rewardguard.json` path.

Each rule check shows its highest exact probability and the files/instances reviewed. A warning (**0.60 ≤ p < 0.80**) is neutral; **p ≥ 0.80** fails. A below-threshold result is successful only for evaluated scopes with no evidence gaps. Missing evidence stays neutral with explicit scope; skipped or unverified content never claims a clean review. Content evaluation errors fail a dedicated content check; unrelated coding errors retain their own aggregate result. Keep the aggregate job as the required branch-protection check; individual content checks vary with applicability.

Content review uses the same Action check mode. Publish this change and pin the Action or reusable-workflow consumer to the resulting published action SHA before rollout. Preserve the separate test and judge jobs: the secret-bearing content judge never executes proposed branch code. Live-provider precision remains unverified; registry coverage and mocked checks do not establish real model accuracy.

## Calibrating

The thresholds are fixed (no output below 0.60, warn at 0.60, fail at 0.80); a `.rewardguard.toml` that sets `[thresholds]` or `[explainer] min_probability` is rejected. Before relying on the check:

1. Run against branches that cheat on purpose; [`tests/test_cheat_branches.py`](tests/test_cheat_branches.py) has ready-made ones.
2. Run against a set of honest PRs.
3. Turn off a rule that misfires on your code under `[rules]` in `.rewardguard.toml` on `main`.

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

## Whole-repository scan

Run a standalone, source-backed review across all eligible code, configuration, and documentation files, then export validated findings to CSV:

```bash
python3 scripts/rewardguard_scan.py --repo-root /path/to/target-repo --output rewardguard-findings.csv --plan
python3 scripts/rewardguard_scan.py --repo-root /path/to/target-repo --output rewardguard-findings.csv
```

This complements `rewardguard check`, which reviews branch changes for reward-hacking behavior. See the [whole-repository scan guide](docs/repository-scan.md) for its file boundary, context grouping, judge adapter, and output guarantees.

## License

Rewardguard is source-available under the [PolyForm Shield License 1.0.0](LICENSE).
Commercial use is permitted when it complies with that license. For uses not
permitted by PolyForm Shield, see [commercial licensing](COMMERCIAL.md).

## Avoiding repeated model input

The GitHub Action now restores and saves authenticated Jev results across runs.
Identical clean defect requests (all probabilities below 0.60) and content routing
requests reuse their previous answers without another provider call. Findings,
errors and incomplete responses are not cached as clean results. Static checks,
test-result validation and content coverage still execute; reuse never turns a
skipped or missing-evidence scope into a verified pass.

The cache identity includes the complete request, endpoint, model and installed
RewardGuard version. Changed task descriptions, source/evidence or questions
therefore trigger fresh requests. Entries are authenticated with the existing
Jev API key; edited or unsigned entries are ignored, and key rotation invalidates
old entries. Cache files contain probabilities and model identifiers, not source
text or credentials. Only the secret-bearing review job uses this cache.

Each entry has a signed creation time. Older entries without one are ignored.
A missing or invalid clock, or an entry dated in the future, forces a fresh
review. There is no automatic age limit by default: exact request, endpoint,
model, epoch, version and key changes invalidate the corresponding entries.
For a mutable model alias, trusted-base `[judge] cache_max_age_seconds` may set
a positive maximum age, for example `86400` for 24 hours. Expiry bounds how long
an undisclosed model change can be reused but can increase provider calls; a
persistently wrong but otherwise valid clock cannot establish real age. For model
changes that keep the same provider model identifier, increment the trusted-base
`[judge] cache_epoch` value (default `"v1"`), for example `cache_epoch = "v2"`.
It accepts 1–64 ASCII letters, digits, dots, underscores or hyphens; changing it
invalidates all previous entries. Neither expiry nor the epoch automatically
detects an undisclosed model change; without expiry, it requires an epoch update.

For local checks, set `REWARDGUARD_CACHE_DIR` to a persistent directory to enable
reuse. Leave it unset locally to always call the provider. Delete that directory
(or the GitHub Actions cache) to force a fresh review.

Content routing and applicability now combine independent questions into fewer
requests, bounded by a conservative UTF-8 byte allowance. This reduces repeated
state even on the first review. Final defect/evidence grading retains its
existing focused batches. Terminal/Markdown notes identify reused requests;
reported input-token totals count actual provider responses only.
