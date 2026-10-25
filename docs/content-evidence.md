# Repository evidence for content review

`rewardguard.content_evidence.collect(repo, trusted_base, head, path, cfg,
max_chars=18000)` collects evidence for one affected **file**. It returns an
`EvidenceBundle` containing `text`, `available`, `provenance`, `omissions`, and
`source_observations`. Evidence-code availability describes the supplied material;
the review engine must still decide whether its scope satisfies a particular rule.

The collector reads committed Git objects from the trusted policy revision and
proposed revision. It does not read working-tree files, execute project code, install
packages, run a browser, resolve remote imports, or fetch referenced URLs. Revisions
are resolved to commit IDs before reading objects. Symlinks and submodules are not
followed. Repository text, import paths, links, and commit messages remain quoted
data. Only applicable policy from the trusted base governs a review.

## Sources and their scope

Configured `[content.context]` paths are attempted first, using the trusted base and
their explicitly declared evidence codes. These files are included as complete artifacts within the budget where possible.
Oversized configured B/P/S Markdown may supply whole relevant sections with exact
line ranges, declared codes, and incomplete-artifact provenance. Matching uses the
affected path tokens and appropriate business/editorial headings; a scoped unit
does not establish completeness of its parent ledger or document. Unadmitted
configured files remain eligible for automatic discovery. Other oversized
configured formats are explicitly omitted. A supplied context file is a repository assertion; the
collector does not independently authenticate its business claims or measurements.

Internal-document filtering applies before all evidence discovery and reads, including
explicit `[content.context]` paths. `content.evidence_exclude` defaults cover agent
instructions and installed skills, documentation and planning trees, tests/fixtures,
tooling, CI, infrastructure, backend-only paths and conventional project documents.
A configured reference to an excluded file records an omission; its contents never
become B/P/S/R/M evidence or reach Haiku. The same boundary applies to Markdown
references, static imports, related-source candidates and inventory entries.
Case differences such as `Docs/` and `Agents.md` do not bypass exclusions.

Use the dedicated `.rewardguard/content-*.md` or JSON files for intentional review
evidence. These remain eligible as trusted context but are excluded as grading
targets. The old implicit `.agents/product-marketing.md` default is removed.
Do not copy a whole development manual into a content policy; supply only the
adopted public-content facts and requirements relevant to the reviewed artifact.

Eligible root business/editorial documents can still provide scoped automatic B/P
evidence. Whole sections, per-file budgets, relevance checks, provenance and source
conflicts are preserved. Missing or filtered policy is a coverage gap, not proof of
a defect. Configured R/M records still require target/revision/freshness checks.

`content.exclude` controls grading targets; `content.evidence_exclude` controls
evidence paths independently. Both are trusted-base, case-insensitive path-list
overrides. A project that actually publishes from an otherwise internal-looking
directory must deliberately retain the other internal exclusions while opting the
published subtree into both lists. Adding a path to `include` or `context` alone
does not bypass either exclusion list. Credential/private-export safety checks
cannot be overridden by these lists.

The proposed-tree inventory supplies I with scope `eligible_text_files`. It lists
up to 40 eligible file paths, prioritizing the affected file, explicit local-link
file matches, and route/content directories before hidden tooling paths. It records
truncation and expressly says URL/render
coverage is unknown. It does not establish sitemap completeness, public routes,
canonical URLs, crawl state, deployment state, or rendered navigation.

The affected file's base and proposed source are included when available. Each
counterpart has a source budget of up to 6,500 characters, also constrained by the
remaining total budget. Whole files are preferred. Git diff line ranges select
whole Markdown sections or complete literal semantic source containers containing
the change when a whole file does not fit. If no whole changed unit fits, the
collector records an omission. The primary diff is supplied independently by the
review engine. Scoped sections retain their exact line ranges and incomplete
artifact provenance; they do not grant complete-artifact evidence.

Relative static imports, conventional `$lib/` to `src/lib/` and `@/` to `src/`
aliases with existing safe Git targets, and ancestor layout, metadata, content,
product, and pricing definitions provide related source, up to six files. Related
files are supplied whole when they fit the per-file and total budgets. Otherwise,
only whole fitting Markdown or semantic source sections defining symbols actually
referenced in the affected artifact are admitted. Other related material is
omitted. Leading snippets and partial line windows are never supplied as
replacement evidence.
Other import aliases, dynamic imports, transitive dependencies, route execution,
framework rendering, and runtime behavior are not resolved.

Actual `git log` metadata for up to five trusted-base commits affecting the file
can supply scoped H evidence. This supplies commit identity, date, and subject;
it does not supply earlier artifact contents, historical claim accuracy, rename
history, or a complete editorial audit trail. No historical evidence is invented
from the current file. Newly added files can have no history.

Only explicitly configured context provides R, M, or S. Raw templates do not
establish rendered state, measurements, or independently verified sources. For a
complete admitted `.html` or `.htm` file, `source_observations` records selected
literal HTML opening tags and attributes with source line numbers. Observations
are marked `source_only`; they cannot establish element visibility, accessible
names, link reachability, computed layout, or runtime form behavior.

## Bounds and privacy

All included text passes through the judge's credential and private-key block
redaction, plus URL-userinfo redaction, before excerpting. Paths containing private,
credential, environment, export, log, dependency, or generated-output indicators
are excluded even if explicitly configured. Binary and undecodable blobs are
omitted; individual blobs over 160,000 bytes are never read. These exclusions and
redaction are defensive heuristics, not a guarantee that arbitrary prose contains
no sensitive information.

Each text evidence unit includes path, commit, role, code, scope, line range, and
completeness provenance. The total text respects `max_chars`; automatic document
content has a separate bounded allowance. Documentation scans, related files,
file inventory, and static HTML observations have explicit caps. Oversized or
skipped units produce omission records. `complete` applies to the stated unit or
scope, so consumers must not interpret a matched section as a complete artifact.
Guidance relevance uses the complete blob already admitted by the read-size guard.
Policy-reference discovery, changed-line anchor collection, section selection, and
history limits each report omissions when they exclude candidates. The primary
diff remains independent of these context-selection limits. If an affected artifact
is unavailable, the collector records that fact and skips dependent skill-relevance,
link-prioritization, import, or related-section analysis rather than treating the
artifact as empty. An absent base counterpart for a newly added file is explicitly
recorded as unavailable.

Missing external facts and omitted evidence remain gaps, rather than proof that
the changed content is defective.
