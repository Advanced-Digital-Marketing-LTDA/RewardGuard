---
id: rewardguard-shared-ci
type: goal-and-requirements
status: active
title: RewardGuard Shared GitHub CI Workflow
tags: [ci, github-actions, content-review]
---

# RewardGuard Shared GitHub CI Workflow

A trusted shared CI review that protects code and tests, reviews only verified public content, and reuses completed work without hiding incomplete results.

## Overview

RewardGuard's shared GitHub workflow reviews code/test integrity and public website content as distinct scopes. It must preserve existing code/test protections while reviewing only eligible, changed public content. Stable local result reuse, bounded provider spending, isolated credentials, and truthful reporting are core behavior—not optional optimizations.

The current checkout contains a Python CLI and GitHub Action for code/test-integrity review, with content review in the normal `check` flow; [README.md](README.md) documents current usage. This spec defines the shared workflow's target contract, not implementation status: some requirements are present or partial, while others remain unverified or absent. Live-provider accuracy and external-consumer rollout require separate provider and release-run evidence.

## Problem Statement

The target must close three stated gaps in the existing shared-workflow approach: internal material must not enter public-content review, identical completed work must not repeatedly incur provider calls, and release rollout must be verified through the workflow's actual consumers. These changes must not weaken RewardGuard's code/test-integrity checks or turn missing evidence, unavailable credentials, cache failures, or provider errors into a pass.

## Target Users

- RewardGuard maintainers who own the review engine and shared workflow.
- Maintainers of repositories that consume the shared workflow.
- Contributors and reviewers who need clear, correctly scoped results for a pull request or push.

The roles are inferred from the supplied requirements; the primary operator and ownership boundaries are unconfirmed.

## Jobs to Be Done

- When a repository change is reviewed, maintainers need code/test checks and public-content checks to remain distinct so excluding internal content cannot disable code protections.
- When content or code is unchanged, maintainers need the workflow to reuse valid prior results so repeated events do not repeat paid provider work.
- When a check cannot run or evidence is incomplete, maintainers need an explicit incomplete/error result rather than a misleading clean pass.
- When a release is promoted, maintainers need evidence that callers used the tested immutable action revision and that rollback remains possible.

## Key User Story

When a pull request changes application code, public content, or both, I want RewardGuard to evaluate only the applicable changed work, reuse valid results for unchanged work, and publish evidence tied to the exact reviewed head, so I can trust the result without exposing internal material or paying for duplicate evaluations.

## Goals

- Preserve every existing code/test-integrity rule and test capability unless a deliberate removal is documented.
- Make public-content eligibility deterministic and local; internal or ambiguous material causes zero content-model calls.
- Reuse unchanged completed evaluations, warnings, failures, and explanations; invalidate only results whose actual inputs changed.
- Bound and isolate provider work so errors, budget exhaustion, unavailable credentials, or missing evidence never yield a false pass.
- Publish complete, head-specific results and measurements that distinguish local reuse from provider-side caching and actual usage.
- Roll out through immutable, tested releases and verified shared-workflow consumers, with an explicit rollback path.

## Non-Goals

- Treating prose, Markdown, or SEO mentions as evidence that a file is public website content.
- Sending internal documents as automatic content-review context or reviewing them as public artifacts.
- Allowing Haiku explanations to change Jev's verdict, or allowing missing evidence to become a fabricated defect or pass.
- Running proposed branch code in a job that holds provider credentials.
- Claiming source files prove rendered, accessible, deployed, or visually correct behavior without corresponding evidence.
- Enabling every rule in the existing catalog, or requiring unrelated SEO, conversion, accessibility, or publishing work for a small content change.

## Success Conditions

The implementation is complete only when measurable evidence shows all of the following:

1. Internal documents generate no content-review requests.
2. Unchanged completed work generates no new Jev or Haiku calls, including across identical or concurrent runs.
3. A change invalidates only the results that depend on that change; reusable findings and coverage remain intact and re-anchored.
4. Reports prove eligibility, evaluation/reuse/exclusion state, provider and cache activity, budgets, reviewed commits, and evidence limitations without exposing prompts, credentials, signing material, or sensitive content.
5. The shared workflow is validated before its maintained `v0` branch is promoted; both action references use the same tested immutable RewardGuard release SHA, and a real consumer run proves the deployed SHA and cache behavior.

The scenario table below is the acceptance contract. Every scenario must produce the stated result before completion is claimed.

| Scenario | Required result |
| --- | --- |
| Only README, internal docs, plans, or agent instructions change | Zero content-model calls |
| An internal document outside a conventional `docs/` directory changes | Still excluded |
| A public article authored in Markdown changes | Included through explicit publication mapping |
| No eligible public content changes | Explicit no-content result; zero content calls |
| First review of new public content | Evaluated once and persisted |
| Identical rerun | Zero Jev/Haiku calls for already completed identical work |
| An unchanged warning or failure is reused | Same finding reproduced from cache |
| One paragraph changes | Only affected units and dependent checks are reevaluated |
| An unrelated commit occurs | Existing content results remain reusable |
| A cosmetic PR-description edit occurs | Independent content results remain reusable |
| A shared public component changes | Only affected dependent artifacts/checks are invalidated |
| A rule or policy changes | Only relevant dependent results are invalidated |
| A file moves without content changes | Content results are reused where valid; route checks are reconsidered |
| Content is deleted | Stale findings are removed; affected references are reconsidered |
| Two runs request identical work | One paid evaluation; the other reuses it |
| A cache entry is tampered with | Rejected; no false pass |
| Cache storage is unavailable | Explicit bounded behavior; no uncontrolled spending |
| A provider returns invalid or incomplete output | Incomplete/error result, never clean |
| Required evidence is missing | `not_evaluated` with a reason |
| A budget is exhausted | Further paid calls stop; review remains incomplete |
| A PR advances during a run | Results remain tied to the reviewed head |
| A test artifact has mismatched commits | Rejected |
| An untrusted branch attempts execution beside secrets | Execution is prevented |
| A new release is deployed | A real run confirms the intended SHA and cache behavior |

## Capabilities

### 1. Separate review scopes

- Preserve two separately identifiable scopes: code/test integrity and public website content. Eligibility, findings, usage, and caching remain distinguishable for each.
- Retain the existing code/test checks even when internal files are excluded from content review.
- Never infer public-content eligibility from prose, a Markdown extension, or an SEO reference.

### 2. Establish a trusted public-content boundary

- Use a trusted, repository-specific allowlist for actual public-content directories, route files, CMS collections, and public-copy sources. Determine eligibility locally before any content-model call.
- Exclude by default when publication status is unknown. Report ambiguous files as excluded/unverified with a reason; never spend model tokens asking whether internal material is public.
- Review only eligible content affected by the reviewed change. An empty eligible set produces an explicit no-content result and zero content-model calls.
- Permit Markdown/MDX only when its source is explicitly mapped as public. File extensions never override the publication boundary.
- Exclude README and contribution files, changelogs, licenses, internal docs/notes/plans/specs/ADRs/RFCs/tickets/runbooks, agent instructions/skills/prompts/workflow and tool documentation, research/briefs/audits/reports/internal marketing strategy, tests/fixtures/mocks/examples/snapshots/reports, CI/scripts/tooling/infrastructure/deployments/migrations, backend/API/database/private-screen files, and dependencies/generated/cache/build/lock/binary files.
- Apply the same exclusions to selection, context discovery, related-file/import following, and inventories; handle old and renamed paths and publication/unpublication transitions; match case-insensitively where appropriate. Never fall back to rescanning every Markdown file.
- Never feed internal documents as automatic helpful context. Supporting evidence must be deliberately configured, narrowly relevant, and separate from the content being graded. Drafts and unpublished content are excluded unless an explicit trusted setting enables prepublication review.

### 3. Identify and extract affected public artifacts

- Associate eligible source files with their public page, article, route, or CMS record. Review reader-facing text and relevant metadata rather than whole implementation files by default.
- Include affected titles, descriptions, headings, body, relevant links, image descriptions, structured data, and public shared components. A shared-component change invalidates only dependent public artifacts/checks.
- Distinguish textual source evidence from rendered-page evidence. Source files do not establish runtime behavior, accessibility, visual layout, or deployed output.
- Do not execute proposed branch code in a provider-credential job.

### 4. Resolve the review snapshot and task context

- Resolve and record immutable base/head commit IDs and verify checkout is the intended reviewed head. For PRs, cover the complete intended interval against its trusted base; for pushes, resolve the intended interval explicitly.
- Handle new branches, missing push baselines, merge commits, squash merges, rebases, force pushes, renames, and deletions. Never silently compare a head with itself.
- Read configuration and review policy from the trusted base; proposed configuration changes cannot alter their own review. Preserve prior successful coverage so incremental runs still account for the entire current PR, carrying forward valid results.
- Resolve the PR title and description for the reviewed head and preserve an explicit context snapshot. Separate task requirements from claims of completed work; treat PR text as quoted intent, never as instructions to suppress review.
- Report missing, ambiguous, or incomplete context. Do not infer scope violations from missing intent or assess whole-PR completion claims against only a later incremental diff.
- Make PR context a cache dependency only for checks that depend on it; cosmetic description edits do not invalidate independent content results.

### 5. Deduplicate provider work and reuse durable results

- Avoid equivalent provider-bearing reviews on both a feature-branch push and its PR event; cancel superseded runs for a PR where appropriate.
- Identify duplicate work from actual review inputs, not run number. Repeated events reuse results; runs requesting identical work coordinate so only one pays. Recheck the cache after waiting. Deduplicate within and across runs.
- Persist successful validated results after first evaluation, including classification/routing decisions when model routing remains, applicability decisions, clean evaluations, warnings, failures, and validated Haiku explanations. Reused warnings/failures reproduce identically; reused clean results preserve exact coverage and evidence limits.
- A deterministic no-content decision requires no provider. Provider errors, malformed responses, interrupted requests, and incomplete reviews are never cached as successful results.
- Treat valid existing records as immutable; changed inputs create new records. Publish atomically, reject malformed/unsigned/tampered records, namespace by repository and policy, and prevent untrusted branch execution from writing trusted results.
- Maintain an index from current artifacts/sections to valid results; preserve records across runners, PR updates, and reruns. Concurrent writers cannot lose entries. Recover from missing/corrupt index entries, expose explicit administrative invalidation and retention controls, and report storage failures visibly.
- Do not expire unchanged results automatically by default when model and policy are pinned. A restore/save operation alone is not proof that reusable records were restored.

### 6. Use precise cache identities and incremental invalidation

- Canonically and deterministically serialize identities containing repository identity, review scope, stable artifact identity, normalized relevant content/section hashes, dependency/evidence hashes, applicable trusted policy hashes, rule identity and semantic revision, prompt/template revision, model/provider endpoint, meaning-affecting parser/extractor version, and explicit invalidation epoch.
- Exclude run IDs/attempts, timestamps, temporary paths, unrelated commit hashes/files/inventories, unrelated PR-description edits, and unrelated rules/package changes. Do not invalidate all results on a RewardGuard package-version change. Separate credential rotation from content identity where feasible and document intentional invalidation caused by rotation.
- Normalize without erasing substantive meaning. Extract/hash trusted context separately, keep its ordering/serialization stable, and do not embed changing commit IDs in otherwise unchanged model state.
- Compare current content with previously reviewed hashes. Unchanged artifacts require zero new evaluation calls. Split content into stable logical units (headings/sections, paragraphs, metadata fields, structured-data objects, relevant shared components); reevaluate changed units with only necessary surrounding context and reuse unchanged units.
- Reuse a move/rename when content is unchanged and route-dependent checks remain valid. Deletions invalidate dependent checks/references without regrading deleted prose. Handle ordering, moved paragraphs, link destinations, metadata, and shared dependencies; re-anchor findings to current locations and remove stale findings when content is deleted or a valid evaluation resolves them.
- Rerun whole-page or cross-page checks only when their actual inputs/relationships change. Preserve valid findings elsewhere on a page or PR. Any context expansion has an explicit dependency and reason; diff-only is not a universal rule.
- Avoid duplicate evidence and sending source files plus the same content again in diffs/evidence. Send rule-specific rubrics and necessary evidence, not the full catalog or every skill. Combine compatible independent questions when this reduces repeated state. Use provider-side context caching only when supported and verified; report it separately and never call it zero-cost without billing evidence.
- Avoid classification/routing/applicability model calls when deterministic logic can decide the same thing.

### 7. Apply scoped rules and preserve evidence/grading contracts

- Maintain a versioned rule registry with stable IDs, predicates, applicability, exclusions, evidence requirements, and focused explanation rubrics. Use the existing catalog as a migration inventory, but filter it to public website scope before enabling rules. Do not enable research, internal-report, email, advertising, or other channel rules merely because they exist.
- Map every enabled rule to applicable public artifact types. Evaluate distinct claims, fields, and requirements independently; do not replace judgments with a broad page-quality score. Optional marketing tactics and style preferences remain optional unless adopted in trusted policy; unrelated SEO/conversion/accessibility/publication features are not prerequisites for small edits.
- Preserve the fixed thresholds: `p < 0.60` means no defect, `0.60 ≤ p < 0.80` warning, and `p ≥ 0.80` failure. Keep task-eligibility probability separate from defect probability. Validate required model answers and probability ranges; missing or malformed required answers fail visibly.
- Haiku explains findings but cannot clear or downgrade Jev's verdict. Explanations identify file/location, supporting excerpt, problem, and actionable correction; reject invented locations/quotations and use focused rule context. Cache explanations against their actual finding/context inputs. Insufficient grounding requires manual review, not invented precision.
- Distinguish supplied facts, adopted policy, inventories, primary sources, rendered observations, measurements, and historical evidence. Record provenance and scope; admit only evidence relevant to the artifact/revision. Keep evidence hashes separate from incidental reporting labels.
- A file inventory is not a public URL inventory; source HTML is not a verified browser render; repository claims do not establish factual truth. Missing required evidence yields `not_evaluated` with the specific missing requirement, not an invented defect or pass. A contract's required-field omission is still evaluable when the adopted contract and complete relevant record establish it.

### 8. Preserve code/test-integrity review

Retain existing capabilities, including deterministic checks for deleted/skipped/focused tests, early exits, reduced test/assertion counts, changed snapshots, altered test configuration/scripts, secrets, dependency changes, deleted files, and changed agent instructions; and Jev review for suspicious assertions, mocks, hardcoded outputs, special cases, fake success, swallowed errors, unsafe retries, stubs, disabled security checks, type escapes, unreachable changes, suppressed logs, timing manipulation, and checker manipulation.

Also preserve PR-context scope-creep and completed-work-overclaim checks when complete context exists; specific expected-value-change justification when code and requirements support it; and optional execution of base tests, head tests, original tests on head code, and new tests on base code. Detect no tests, decreased totals, increased skips, new/existing failures, failing original tests, and ineffective new tests. Objective clear-cut checks retain their severities without unnecessary model calls. Unsupported languages or unavailable test execution have explicit coverage limitations.

The migration accounts for every existing rule ID and behavior in the current README; any deliberate removal is documented.

### 9. Bound spending and isolate credentials/execution

- Require explicit finite production budgets. Bound provider attempts, retries, total request bytes, concurrency, runtime, and individual request size. Add token/cost limits only where usage is honestly measurable or bounded.
- Reserve budget before requests; charge retries and failed attempts to attempt/byte budgets. Cache hits consume no provider attempt. On exhaustion stop paid work and report incomplete review—never skip silently and return clean.
- Provide dry-run output for eligible files, cache availability, planned work, and exclusion reasons, with no provider calls. Cache outage must not trigger an unlimited full review.
- Resolve commits in a job that executes no proposed code. Run optional branch tests separately without provider secrets. The judge never executes repository install hooks, tests, generators, or application code.
- Install RewardGuard from a trusted pinned action source; pass only explicitly named secrets; keep checkout credentials out of untrusted execution. Redact credentials and private-key blocks before model submission/logging.
- Keep GitHub/provider credentials out of Haiku's subprocess environment except its intended authentication; disable Haiku tools, project configuration, and MCP execution.
- Define behavior for fork and Dependabot PRs without credentials; unavailable credentials never mean pass. Authenticate test artifacts and validate expected base/head/run association before use.

### 10. Publish complete reports and observable usage

- Produce terminal, Markdown, and machine-readable JSON reports, plus a job summary for PR and push runs. Update one stable PR comment rather than posting duplicates.
- Publish checks on the exact reviewed head. Keep `rewardguard / rewardguard` as the stable aggregate required check; publish content eligibility and only applicable content-rule checks.
- Distinguish evaluated, reused, excluded, skipped, `not_evaluated`, incomplete, and error states. Warnings stay neutral; failures fail. Remove or correct stale checks from earlier runs when findings resolve or rules become inapplicable. Required publication failure is visible, and the original review error is preserved even if reporting/cache saving also fails.
- Report separately for code, content, and explanations: provider requests and HTTP attempts; local result-cache hits; restore/save outcomes; changed/reused artifacts/sections; provider-reported input/output and cached-input tokens where available; missing usage data; request bytes and context/question sizes; retries and budget denials; content-stage breakdown; evidence-backed cache-miss reasons; model/rule/prompt/policy revisions and reviewed commits.
- State explicitly that archive restoration does not prove result reuse. Do not log prompts, credentials, signing material, or sensitive content. Do not invent monetary savings or token estimates as measured billing.

### 11. Release and maintain the shared workflow

- Update implementation, configuration schema, examples, and documentation together. Publish an immutable RewardGuard release and pin both shared-workflow action references to the same tested release SHA.
- Validate the shared workflow before promoting its maintained `v0` branch. Verify callers consume the intended shared workflow; inventory repositories on older immutable pins; confirm caller permissions include required read/check/comment permissions and test-execution settings agree with trusted configuration.
- Verify the deployed action SHA in a real run and provide a rollback path. Preserve compatible caches across unrelated releases; make required cache migrations explicit.
- Update local hooks separately when they use independently installed RewardGuard versions. Merging into RewardGuard's default branch alone is not rollout completion.

## Non-Functional Requirements

- **Security and trust:** trusted-base configuration, repository/policy cache isolation, authenticated records/artifacts, minimal secret exposure, and no untrusted code execution beside provider credentials.
- **Reliability:** atomic durable records, concurrent-run coordination, recoverable indexes, bounded failure behavior, and truthful incomplete/error states.
- **Determinism:** stable eligibility, canonical cache identities, explicit Git intervals, and exact reviewed-head association.
- **Cost control:** finite budgets and zero provider attempts for valid cache hits or deterministic no-content outcomes.
- **Auditability:** reports preserve provenance, coverage, usage, cache outcomes, limitations, revisions, and commits without sensitive payloads.

## Technology

| Aspect | Choice | Rationale |
| --- | --- | --- |
| CI integration | GitHub Actions shared workflow | Explicitly required by the project scope. |
| Review engine | RewardGuard | Existing implementation and rule inventory are the migration baseline supplied by the user. |
| Content-model stages | Jev evaluation and Haiku explanation | Required by the supplied behavior; Haiku cannot alter Jev's verdict. |
| Review events/results | GitHub PR and push events, checks, job summaries, and one stable PR comment | Required publication and review-snapshot behavior. |
| Durable cache/storage/signing implementation | Unselected | The requirements define integrity and durability behavior but do not choose a storage or signing mechanism. |
| Implementation language/runtime and exact provider endpoints | Unconfirmed | Not specified by the supplied target scope; settle during architecture/design. |

## Source Baseline

The user supplied these source references as the migration baseline and reported that they were inspected on October 28, 2026. They are references for implementation and rule inventory, not evidence that the target requirements already pass:

- Shared workflow at [`workflows/.github/workflows/rewardguard.yml`](https://github.com/Advanced-Digital-Marketing-LTDA/workflows/blob/f655460184fdef407af2d8441915834d0d24b77b/.github/workflows/rewardguard.yml), commit `f655460184fdef407af2d8441915834d0d24b77b`.
- RewardGuard implementation at [Advanced-Digital-Marketing-LTDA/RewardGuard](https://github.com/Advanced-Digital-Marketing-LTDA/RewardGuard/tree/958ef58b886910c5370536c63252a0a81f30fe8d), commit `958ef58b886910c5370536c63252a0a81f30fe8d`.
- Existing content rule catalog at [`src/rewardguard/content_data/catalog.json`](https://github.com/Advanced-Digital-Marketing-LTDA/RewardGuard/blob/958ef58b886910c5370536c63252a0a81f30fe8d/src/rewardguard/content_data/catalog.json).
- Existing code/test rule IDs and behaviors are to be inventoried from the [current README](https://github.com/Advanced-Digital-Marketing-LTDA/RewardGuard/blob/958ef58b886910c5370536c63252a0a81f30fe8d/README.md).
