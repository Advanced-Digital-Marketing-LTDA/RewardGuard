# ContentGuard skill audit

Snapshot: 2026-10-23. The available cloud catalog contained **124 skills** over seven pages. The executor catalog contained **0 skills**. This audit read all **80 main guides** relevant to writing, SEO, landing pages, conversion, channel content, and adjacent content/research artifacts. The other 44 catalog entries are development workflows, infrastructure/account tools, non-content data operations, or unrelated specialties.

## Sources and coverage

| Audit | Main guides | Scope |
|---|---:|---|
| [Writing](writing.md) | 10 | Copywriting/editing, humanizing, voice, content strategy, briefs, product context, customer research, sales writing |
| [SEO](seo.md) | 10 | Search/AI visibility, ecommerce, one-page sites, technical SEO, schema, pSEO, architecture, comparisons |
| [OpenSEO](openseo.md) | 10 | Keyword research/clustering, competitors, local search, links, project context, audits/reports |
| [Conversion](conversion.md) | 15 | Landing pages, offers, pricing, forms, signup, activation, paywalls, popups, tools, experiments, site guidance |
| [Channels](channels.md) | 12 | Ads, email, outbound, SMS/WhatsApp, social, video/images, press, ASO, sponsorships, directories |
| [Adjacent content](adjacent.md) | 19 | Launches, partnerships, community/events, referrals/cancellation, reports, measurement, writing providers |
| [Supplementary evidence](supplementary.md) | 4 | Analytical/visual truthfulness, updates, feedback anchoring |
| **Total** | **80** | **Every relevant main guide in the available catalog** |

[Machine-readable skill inventory](skill-inventory.json) records every catalog entry, its exact source URI, audit family, and inclusion/exclusion status.

## How to interpret the audit

The family reports retain detailed candidate defects and per-skill provenance. Candidate counts are not the final execution count: overlapping guidance is consolidated into the canonical catalog in the revised content review specification. A skill can contribute several checks; several skills can support one check. Pure provider/operation guidance is recorded without fabricating a content requirement.

The selected [243-signature catalog](../content-checks.md) spans 37 focused packs; its [authoritative JSON](../content-checks.json) maps all 80 inspected main guides and records artifact variants, specialist overrides, cross-pack routes, aliases, and inline rubric exclusions. Named fields and requirements receive separate propositions. Family candidates remain research and do not add enabled checks beyond that selected catalog.

Only applicable checks run. Factual contradictions require supporting evidence; absent live/crawl/analytics/visual data is an explicit coverage gap rather than a finding or a claimed pass. Preferred layouts, word counts, vocabulary lists, and channel tactics become enforceable only when an approved project brief or policy makes them requirements.

Missing evidence is recorded as `not_evaluated`. A contract-required missing provenance field is reviewed from its adopted contract and complete relevant record; it does not require the missing source itself. Dates are required only when material to the claim. Each explanation receives its matching bounded rubric with exclusions inline, rather than instructions to consult an unloaded audit.

## Source limitations

Every relevant main SKILL.md was read completely, including pagination where present. Numerous linked user-package reference resources returned `failed to read skill resource` through the provided skill reader. Accessible references were read and are listed by each audit; unavailable references are recorded separately and their unseen detailed rules were not used. This is comprehensive coverage of the available main guides, not a claim to have inspected inaccessible reference files or undiscovered private repositories.

No publishing, sending, SEO account mutation, analytics query, or other skill workflow was executed as part of reading these sources.

This audit does not establish live Jev/Haiku precision. Runtime verification and release rollout are separate; CI consumers need the published action commit SHA containing the feature.

