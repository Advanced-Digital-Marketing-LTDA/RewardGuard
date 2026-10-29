# Public-content API (Tasks 2 + 3)

Trusted-base configuration is the sole publication authority. Default `content.publications = []` makes arbitrary Markdown, internal documentation and JavaScript strings ineligible. Existing `include` / `source_include` only narrow declared sources. Required exclusions, unsafe paths and nonregular Git objects cannot be opted in.

```toml
[content]
packs = ["writing", "metadata", "links"]

[content.context]
B = [".rewardguard/product-facts.md"]
P = [".rewardguard/editorial-policy.md"]

[[content.publications]]
id = "articles"
sources = ["content/articles/**/*.md", "content/articles/**/*.mdx"]
type = "article"
route = "/articles/{stem}"
published = true
drafts = false
dependencies = ["footer"]
evidence = ["B", "P"]

[[content.publications]]
id = "footer"
sources = ["src/Footer.svelte"]
type = "component"
route = "/_shared/footer"

[[content.publications]]
id = "product-copy"
sources = ["content/products/*.json"]
type = "product"
route = "/products/{stem}"
fields = ["title", "description", "features.*.label"]
```

IDs are unique stable declaration identifiers; a declaration can map multiple source files. Types are `page`, `article`, `product`, `component`, `metadata`. Routes must be local paths, optionally with `{stem}` or `{path}` substitutions. Unknown dependencies, cycles, invalid fields/types/routes, duplicate IDs and unknown keys are configuration errors. Overlapping source mappings are excluded as ambiguous. `published=false` excludes a declaration; drafts require `drafts=true`. Evidence codes bind only the configured trusted-base paths for that declaration; no automatic documents, imports, sibling files, Git logs or repository inventories are collected.

`content_publications.manifest(repo, base, head, cfg, changed=None)` returns a JSON-compatible local manifest without clients, credentials, provider calls or executing branch code. Top-level fields: `schema_version`, `extractor_revision`, `base`, `head`, `artifacts`, `exclusions`, `deleted`, `cache`. `artifacts` lists all currently declared regular sources with `id`, `path`, `type`, `route`, `source_format`, `units`, `limitations`, `dependencies`, `resolved_dependencies`, `missing_dependencies`, `evidence`, source/semantic digests, `baseline_units`, `affected`, `semantic_changed`, `cache_only`, and `reasons`. A unit contains `identity`, `kind`, `text`, `context`, `field`, `line`, unit-relative `anchors`, `line_map`, and `changed`. `baseline_units` are comparison metadata. `exclusions` records path/reason. `deleted` records old id/path/route, never stale findings. Cache availability is `configured` or `disabled`; the manifest does not guess authenticated hits from file existence.

Source paths/commits/absolute lines never enter independent reader-unit model inputs. Explanation anchors are unit-relative exact extracted source snippets and are mapped to current source lines only in the final report. Whole-artifact/order, route/reference, editing-baseline and declared transitive dependency inputs enter only rules that consume them. Every rule has a semantic revision and explicit website disposition; `content_rules.inventory()` returns all 243 retained IDs, revisions, scopes and artifact types. Research/brief/SEO-research/ad/email/SMS/sponsorship/comms/sales/report/listing packs are outside this initial website scope. A rule requiring an adopted policy is locally not applicable without usable bound P. Other missing facts/render/measurement evidence remains not evaluated. C is contract-specific: only the two authored-text completeness rules (`CG_SECTION_PROMISE_MISMATCH`, `CG_SEARCH_ANSWER_COVERAGE`) can receive it from complete Markdown/HTML reader extraction plus complete declared dependencies. Selected JSON fields or HTML attributes never establish an entire record; model state explicitly treats unselected fields as unknown rather than absent.

`content_review.review(...)` returns `ContentResult`. `to_dict()` includes `status`, `coverage`, `provenance`, `omissions`, `errors`, `eligibility`, `result_cache_hits`, `grade_cache_hits`. Findings/notes remain separate attributes as before. Eligibility is deterministic, has no probability, and includes `cache_only` / `semantic_changed`. Coverage statuses are `evaluated`, `not_applicable`, `not_evaluated`, and `unchanged`. `unchanged` means no new reader content and no reusable completed authenticated result; it is not a required evidence gap or clean verdict. With only unchanged/unadopted work, overall status is `skipped`. Extraction gaps remain visible even alongside `reviewed` scopes. Later provider/explanation failure returns `status=error`, explicit `errors`, and all completed coverage/findings; CLI must propagate `errors` to its report (minimal compatibility propagation is included).

Authenticated final unit/rule records replay completed probabilities, coverage and relative findings. Restored coverage has `reused: true`; `result_cache_hits` counts completed unit/rule record hits independently of Jev request-cache hits. Completed Jev propositions are also checkpointed independently before explanation. If a later provider or Haiku step fails, cache-only replay can restore those authenticated grades/findings without a paid call. These partial records use `grade_cache_hits`, `reuse_stage=jev_grade_checkpoint`, and `result_complete=false`; unfinished required propositions remain `not_evaluated`, and unavailable explanations keep an explicit `explanation_status=not_evaluated`. A clean completed proposition never implies the remaining required fields passed. A move-only or implementation-only change uses cache-only lookup for unchanged reader semantics; a miss never triggers regrading. Complete clean records survive explanation-model changes. Warning/failure records invalidate changed explanation inputs; normal changed-content review then reuses the raw Jev request cache and regenerates only explanations. On cache-only untouched scopes, changed explanation inputs preserve the authenticated Jev probability/finding, omit stale details and report `explanation_status=not_evaluated` with an explicit reason, without a provider call. There is no automatic TTL; existing explicit cache-age configuration remains honored. This is interim signed local/Actions caching; durable/concurrent cross-run exactly-once guarantees remain deferred to REWARD-1.

Extraction is deliberately conservative: Markdown paragraphs/headings/simple frontmatter/links/alt; literal HTML paragraphs with inline markup/entities, reader attributes and JSON-LD; declared JSON string fields; static template markup from Svelte/Vue/Astro and one unambiguously bounded direct JSX return expression. The JSX boundary skips JavaScript strings/comments and stops at the matching root element; compound or multiple return expressions, regex ambiguity and interpolated JavaScript template literals fail closed. MDX ESM and expression regions are omitted whole, including multiline bodies, before reading subsequent unambiguous Markdown. When a safe closing boundary cannot be established, the remaining region is omitted with an explicit limitation. Code fences, dynamic expressions, unsupported frontmatter/escaped or ambiguously anchored repeated JSON/implementation formats remain explicit extraction limits; there is no whole-source fallback. Source observations never establish rendered output, live routes, measured behavior or external facts. Blob reads are bounded to 160000 bytes, and oversized whole semantic inputs are unverified rather than clipped into an invented complete artifact.
