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
their explicitly declared evidence codes. These files are included only as complete
units within the budget. A supplied context file is a repository assertion; the
collector does not independently authenticate its business claims or measurements.

Automatic discovery then looks for ancestor `AGENTS.md`, `CLAUDE.md`, and README
files, root product/style/content documents, plus documentation under `docs/`, `doc/`, and `.agents/` whose paths concern
writing, content, product, style, SEO, CRO, or landing pages. Applicable agent files
can reference local skill documents through Markdown links. Only safe local paths
with relevant names are followed; remote links and unrelated skills are excluded.
Markdown sections must contain a relevant topic and business or policy language.
Whole matching sections supply scoped B or P evidence. A section that does not fit
is omitted with its line range; a clipped sentence never becomes a complete policy.
Business facts are repository-authored claims, not independently verified truth.
All sources retain separate provenance, including conflicting facts; no newest-file
overwrite or claim reconciliation is performed. Configured R/M evidence also
requires consumer checks for the target file, measured revision, and freshness.
The trusted revision of a context file does not prove it measured the proposed
revision. Heuristics cannot establish that every discovered guideline applies to every rule.

The proposed-tree inventory supplies I with scope `eligible_text_files`. It lists
up to 40 eligible file paths, prioritizing the affected file, explicit local-link
file matches, and route/content directories before hidden tooling paths. It records
truncation and expressly says URL/render
coverage is unknown. It does not establish sitemap completeness, public routes,
canonical URLs, crawl state, deployment state, or rendered navigation.

The affected file's base and proposed source are included when available. Each
counterpart has a 3,000-character source budget. Git diff line ranges select whole
Markdown sections or complete literal semantic source containers containing the
change when they fit. Otherwise an explicitly partial line window surrounds the
first changed line; a leading excerpt is used only when no changed line is known.
Every excerpt retains its line range and incomplete-artifact provenance.
Relative static imports, conventional `$lib/` to `src/lib/` and `@/` to `src/`
aliases with existing safe Git targets, and ancestor layout, metadata, content, product,
and pricing definitions provide related source, up to six files and 1,800
characters per counterpart. These sources establish source-level facts only.
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
Missing external facts and omitted evidence remain gaps, rather than proof that
the changed content is defective.
