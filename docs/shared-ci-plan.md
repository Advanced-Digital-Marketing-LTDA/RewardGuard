# RewardGuard shared CI implementation plan

Baseline: `958ef58b886910c5370536c63252a0a81f30fe8d`, 2026-10-28.
Requirements: [goal-and-requirements.md](../goal-and-requirements.md).

## Agreed scope and constraints

- Preserve existing code/test rules, fixed thresholds (`0.60` warning, `0.80` failure), optional test execution, fail-closed provider validation, and separate content/code coverage.
- Establish publication locally from trusted-base mappings. Unknown/internal content receives no content-model calls. No proposed code executes beside provider credentials.
- Use signed GitHub Actions-cache records for interim reuse. Durable storage and cross-run coordination belong to **REWARD-1**, task 1307 in the new RewardGuard project (REWARD, project 17, team Moderaty) in It's a Plan. The task is unassigned in Backlog, without start/due dates.
- Budget work is excluded by the user's later instruction. Preserve existing optional limits; add no mandatory spending policy.
- This intermediate release cannot claim the original durability, concurrent exactly-once, or finite production spending guarantees. Keep their acceptance rows visibly deferred/excluded.
- Preserve unrelated working changes. Local hooks are separate installations. Publication, shared-channel promotion, and production acceptance require separate evidence.

## Current baseline

The content gate uses broad file patterns and Jev classification. The cache stores routing and clean Jev responses, but not warning/failure evaluations or Haiku explanations, and includes the package version in its identity. The shared workflow separates branch tests and the judge and pins both action uses to one release SHA. Its existing promotion evidence calls `@v0`, so candidate workflow validation must be added before promotion.

Focused baseline cache, budget, configuration, and diagnostics tests passed (180 tests). Full implementation verification must use the declared development dependencies and retain provider-free fixtures.

## Task 1: Authenticated results and explanations

Extend the existing HMAC/atomic-file cache with repository/scope identity, deterministic serialization, explicit format/revision/epoch, validation, immutable valid records, recoverable local metadata, and within-run per-identity coordination. Do not include package version or incidental run identifiers. Cache all validated Jev probabilities including warnings/failures, and validated Haiku explanations separately. Keep completed evaluation work when explanations fail. Never persist prompts or credentials. Reject invalid records; preserve visible outage diagnostics. Record signing-key rotation invalidation. Keep the signing key out of the Haiku subprocess and use an allowlisted runtime/authentication environment. Report requests, attempts where observable, local reuse, and unavailable provider billing fields separately. No cross-run exactly-once claim.

## Task 2: Trusted publication boundary and public units

Extend trusted-base configuration with explicit source/public-artifact mappings, stable IDs/routes, publication status, shared dependencies, and narrowly configured evidence. Include patterns only narrow a mapping; they never establish publication. Apply exclusions and safe-path handling to old/new paths, imports, context and inventory, including case variants, drafts and symlinks. Remove automatic internal-document discovery. Content exclusion never changes code-review selection.

Extract reader-facing fields from mapped Markdown/MDX, HTML, JSON copy records and supported static template literals without executing code. Preserve source anchors and evidence limits; unsupported dynamic portions remain not_evaluated. Split into stable headings, paragraphs, metadata, links, descriptions, structured data and shared units. Separate semantic content identity from source location. Changes schedule dependent units/checks; moves re-anchor unchanged content and reconsider routes; deletions remove stale findings and reconsider references.

## Task 3: Scoped applicability and incremental evaluation

Retain catalog IDs and inventory every code/test rule. Add semantic revisions and explicit public-artifact applicability; classify existing catalog rules as public-enabled, adopted-policy-only, or outside website scope. Use deterministic routing where possible. Model applicability can operate only after publication eligibility, with reusable results. Independent unit/rule identities contain actual content, evidence, selected policy, prompt/extractor revisions, model/endpoint and epoch. Exclude unrelated commits/files, package updates, and PR descriptions for context-independent checks. Required missing evidence is not_evaluated, not an invented defect or pass. Preserve grounded explanations and thresholds.

## Task 4: Snapshots, dry run, artifacts and reporting

Resolve immutable comparison base, policy base and head once, distinguishing PR merge-base coverage from explicit push intervals. Preserve full-current-PR coverage through record reuse. Handle new branches, force pushes/rebases, merges, renames and deletions without silently comparing a head with itself. Add provider-free `check --plan` output for selected/excluded files, units, dependencies, cache availability and planned work. Preserve source-vs-runtime limits.

Keep tests separate, pin trusted tools, use isolated Python and no persisted checkout credentials. Validate test artifact origin/run association/digest/commits before use and state that provenance does not prove effectiveness. Avoid feature-push plus PR duplicate events, serialize PR review and preflight stale heads. Publish exact-head evaluated/reused/excluded/skipped/not_evaluated/incomplete/error states in terminal, Markdown, JSON, summaries and one stable PR comment. Reconcile stale checks and preserve original errors when reporting/cache operations also fail.

## Task 5: Compatibility, candidate validation and rollout

Update action/config examples, caller guidance, content guides and README together. Preserve every README code/test rule and capability unless an explicit removal is documented. Exercise candidate shared-workflow content at its immutable revision before channel promotion; both RewardGuard action uses must match one tested published release SHA. Inventory caller permissions, pins, mappings and run-tests agreement. A real mapped-content consumer must show first evaluation, restored-record reuse including findings, exact workflow/action SHAs and rollback evidence. Roll back through a forward reviewed commit restoring known-good pins. Never claim merging RewardGuard alone completes rollout.

## Validation and acceptance

Use focused failing regressions before behavior changes, then full Python and workflow tests. Test publication safety, no-content zero calls, explicit Markdown publication, malformed config, symlinks, evidence filtering and unchanged integrity coverage. Verify clean/warning/failure/explanation reruns, independent invalidation, paragraph moves/renames/deletions, duplicate requests, tampering, missing/corrupt indexes and outages. Test invalid/incomplete provider output, evidence gaps, missing credentials, snapshot mismatch, artifact provenance, no branch execution beside secrets, stale checks/comments, and exact-head publication errors. Provider fixtures are not live accuracy evidence.

| Original acceptance scenarios | Intermediate disposition |
| --- | --- |
| Internal/unknown material; public Markdown; no-content | Required |
| First review, identical rerun, reused findings | Required when authenticated records are restored |
| Paragraph, unrelated commit, PR text, dependency/policy, move/deletion | Required for declared supported extraction and dependency scope |
| Two concurrent runs pay once; guaranteed durable persistence/index merging | Deferred to REWARD-1; within-run deduplication still required |
| Tampering, cache outage, malformed providers, missing evidence | Required; outage may cause a visible fresh review |
| Mandatory finite spending / budget exhaustion acceptance | Excluded from new work; existing optional controls retained |
| Head advance, artifact mismatch, secret isolation | Required |
| New release and real consumer SHA/cache proof | Release gate; cannot be certified by local tests |

## Implementation evidence

Implementation progress and test commands are recorded during execution. No live provider run, release publication, consumer deployment, or channel promotion has been claimed.
