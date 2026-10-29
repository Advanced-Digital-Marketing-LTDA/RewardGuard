# OpenSEO skill audit for RewardGuard ContentGuard

> Historical source-audit record (2026-10-23). The candidate contracts and routing/evidence proposals below document the broader catalog design, not the current website runtime. In particular, the old Jev task-classifier and automatic evidence-discovery proposals are not active. Current behavior requires explicit trusted-base publications and bound evidence, deterministic supported artifact/rule selection, and mandatory exclusions. See [current review flow](../content-checks.md#review-flow) and [the publication API](../shared-ci-public-content.md).

Research date: 2026-10-23. Scope: all ten `openseo:*` skills. This is a research catalog, not an SEO audit, implementation, or live research run. No SEO APIs, credit-spending operations, remote writes, or tests were used.

## Reading record and source boundaries

The exact packages were discovered through the paginated cloud skill catalog (`skills.list`, pages starting at offsets 0 and 20). Each main resource was read completely with `skills.read`; all ten returned `next_cursor: null`. The long `seo-report` response was inspected in complete, non-overlapping portions after a combined display truncated. Total main-skill text: 95,191 characters. The relevant cross-reference is the sibling `seo-report` skill, whose full writing rules, starter HTML/CSS, primitives, and guardrails were read. These skills contain no separately linked rubric/checklist resource files. Public documentation links in their output instructions identify workflow provenance; they were not treated as unseen additional guidance.

| Skill | Full main-resource URI | Characters read |
| --- | --- | ---: |
| competitive-landscape | `skill://plugin_asdk_app_6abddd2c7e4c819191f1398c4bd8e9b3/competitive-landscape/SKILL.md` | 6,235 |
| competitor-analysis | `skill://plugin_asdk_app_6abddd2c7e4c819191f1398c4bd8e9b3/competitor-analysis/SKILL.md` | 6,245 |
| keyword-clustering | `skill://plugin_asdk_app_6abddd2c7e4c819191f1398c4bd8e9b3/keyword-clustering/SKILL.md` | 5,710 |
| keyword-research | `skill://plugin_asdk_app_6abddd2c7e4c819191f1398c4bd8e9b3/keyword-research/SKILL.md` | 6,983 |
| link-prospecting | `skill://plugin_asdk_app_6abddd2c7e4c819191f1398c4bd8e9b3/link-prospecting/SKILL.md` | 6,814 |
| local-seo | `skill://plugin_asdk_app_6abddd2c7e4c819191f1398c4bd8e9b3/local-seo/SKILL.md` | 7,532 |
| seo-audit | `skill://plugin_asdk_app_6abddd2c7e4c819191f1398c4bd8e9b3/seo-audit/SKILL.md` | 15,144 |
| seo-coach | `skill://plugin_asdk_app_6abddd2c7e4c819191f1398c4bd8e9b3/seo-coach/SKILL.md` | 9,711 |
| seo-project-setup | `skill://plugin_asdk_app_6abddd2c7e4c819191f1398c4bd8e9b3/seo-project-setup/SKILL.md` | 9,227 |
| seo-report | `skill://plugin_asdk_app_6abddd2c7e4c819191f1398c4bd8e9b3/seo-report/SKILL.md` | 21,590 |

## Fit with the approved architecture

Keep the deterministic content-presence gate, then Jev's content-task classification at `p >= 0.60`, then independent applicable defect checks. Each candidate below is a separate hypothesis about a defect: `< 0.60` ignore; `0.60–0.79` warn; `>= 0.80` fail. These are probabilities that a defect exists, not editorial quality scores, SEO metric targets, or ranking guarantees.

The catalog deliberately exceeds the five generic checks. It separates content usefulness, research validity, report provenance, local interpretation, outreach accuracy, and viewer compatibility. Candidate IDs are proposed stable names, not claims that these checks already exist. Cross-skill overlaps should normalize to one canonical check with multiple sources rather than duplicate Jev calls or findings.

Applicability must be narrower than “this file contains SEO words.” Recognize page copy, keyword map/brief, outreach draft, market/competitor research report, local audit, coaching response, setup record, and OpenSEO HTML report separately. Most of these skills describe research orchestration and reports; they do not impose universal website or landing-page requirements. A normal landing page does not need a research log, a Maps grid, a shortlist, an evidence appendix, or an OpenSEO byline.

Every check must identify newly changed content and a concrete consequence. Missing external evidence means a factual conclusion is **not evaluable**, unless the defect being checked is an explicitly required provenance disclosure in the report itself. “No source supplied” does not establish “the number is false,” “the page does not rank,” or “the business is invisible.” A claimed completed save, upload, connection, or publication can be checked only against supplied tool records.

Evidence labels in the tables:

- **D**: changed artifact plus enough surrounding content to interpret the change.
- **T**: trusted base-revision project scope, business facts, goals, voice preferences, existing URL inventory, or approved brief/template.
- **E**: supplied evidence capture: SERP rows, GSC exports, crawl/page snapshots, keyword metrics, profile/grid/review data, or contact source pages, with relevant dates and scope.
- **W**: supplied workflow/tool metadata, such as a successful save, confirmed integration, prior report identity, or user-authorized public sharing.

For Haiku, extract only the source paragraph(s) for the triggered rule, the changed passage, and the required T/E/W inputs. For example, the missing-grid-rank check needs the local skill's rank-interpretation guardrail and the point's `resultsCount`; it does not need keyword research, the entire report CSS, or all ten skills. HTML constraints can have exact local evidence, but they remain scoped to the OpenSEO report viewer.

## 1. competitive-landscape

Source: full URI in the reading record, especially Workflow 1–9, Output format, and Guardrails. Actual guidance: define a representative query set and location; distinguish direct product competitors, publishers, marketplaces, communities, and documentation; compare recurring winners; synthesize themes, SERP formats, authority, and gaps. “Distinguish SEO competitors from business competitors,” label estimates, call a small-query-set read directional, and separate organic from Maps winners. The default report includes market read, winner table, patterns, gaps, next workflow, and query-set methodology. Default operating quantities (such as 5–10 queries or 3–5 domains) are research budgeting guidance, not website content thresholds.

| Proposed rule ID | Defect statement | Apply only to | Evidence required |
| --- | --- | --- | --- |
| OSEO_LANDSCAPE_DOMAIN_TYPE_MISSING | A winner is presented without distinguishing its business/content type where that distinction changes the strategy. | Market landscape reports | D; E winning-domain roster |
| OSEO_LANDSCAPE_BUSINESS_SEARCH_CONFUSED | Shared SERP visibility is asserted to prove direct product competition. | Landscape competitor classification | D; T positioning; E domains and queries |
| OSEO_LANDSCAPE_LEADER_QUERY_SUPPORT | A claimed market leader is not supported by the report's query-set visibility evidence. | Leader claims | D; E recurring-domain/query results |
| OSEO_LANDSCAPE_MARKET_SCOPE_OMITTED | The query set or relevant market/location is absent, making the stated competitive conclusion uninterpretable. | Landscape methodology | D; T/E research scope |
| OSEO_LANDSCAPE_SMALL_SAMPLE_CERTAINTY | A narrow query sample is described as a comprehensive market conclusion without a directional caveat. | Small-sample landscape conclusions | D; E actual sample and limits |
| OSEO_LANDSCAPE_ESTIMATE_AS_EXACT | Provider-estimated organic footprint is written as exact measured traffic. | Footprint comparisons | D; E metric definitions |
| OSEO_LANDSCAPE_LOCAL_ORGANIC_CONFUSED | Organic-page winners are presented as Maps/local-pack winners. | Local market landscapes | D; E separate organic and local results |
| OSEO_LANDSCAPE_PATTERN_EVIDENCE_MISSING | A content/theme/authority winning pattern is asserted without corresponding observed evidence or an inference label. | “Why they win” findings | D; E relevant pages, rankings, or backlinks |
| OSEO_LANDSCAPE_GAP_OWNER_DEMAND_UNSUPPORTED | A gap's owner or demand is stated without supporting query/theme evidence. | Gap and opening recommendations | D; E demand and competitor evidence |
| OSEO_LANDSCAPE_NEXT_WORKFLOW_UNSPECIFIC | The default landscape report gives no actionable next research/content workflow tied to the opening it identified. | Default report next steps, unless an approved template replaces them | D; T applicable template; E conclusion |

External-data limitation: the diff alone cannot establish current winners, volume, footprint, backlink advantage, or a winnable gap. Do not fetch them automatically during a secret-bearing content review. Judge supplied evidence and wording; otherwise mark the factual check unavailable.

## 2. competitor-analysis

Source: Workflow 1–10, Output format, and Guardrails. Actual guidance: analyze one named competitor with relevant ranking rows and themes; use first-party GSC for the user's baseline when available; filter for business fit; distinguish evidence from inference. Crucial instruction: “Do not infer competitor page/content-type patterns from keyword rows alone; use SERP or web evidence for page-level claims.” Local-pack claims need local evidence. Recommend a stronger angle rather than copying. If the user's domain is unavailable, keep the work competitor-only. Missing backlink data permits continuing and is not evidence of a backlink defect.

| Proposed rule ID | Defect statement | Apply only to | Evidence required |
| --- | --- | --- | --- |
| OSEO_COMPETITOR_BASELINE_INCOMPARABLE | A head-to-head footprint comparison mixes materially different market, language, scope, or metric definitions without disclosure. | Competitor comparison tables | D; E metric scopes; T intended market |
| OSEO_COMPETITOR_FIRST_PARTY_UNACKNOWLEDGED | The user's performance is described as an actual baseline using third-party estimates while supplied GSC evidence establishes a different first-party baseline. | Own-site comparisons with supplied GSC | D; E both datasets and definitions |
| OSEO_COMPETITOR_KEYWORD_BUSINESS_MISMATCH | A competitor keyword is recommended despite a clear mismatch with the user's product or audience. | Proposed target pages/terms | D; T business/positioning; E term intent |
| OSEO_COMPETITOR_BRAND_DEMAND_UNSEPARATED | Branded competitor demand is treated as a directly available generic opportunity without explaining the distinction. | Theme/opportunity conclusions | D; E branded/nonbranded rows; T product fit |
| OSEO_COMPETITOR_PATTERN_FROM_KEYWORDS | Page layout, page type, or content quality is asserted as directly observed using only keyword rows. | Content-pattern claims | D; E source types and any actual page captures |
| OSEO_COMPETITOR_INFERENCE_AS_OBSERVATION | A material inferred strength or vulnerability is presented as a verified fact. | Analytical findings | D; E observation/inference provenance |
| OSEO_COMPETITOR_LOCAL_STRENGTH_FROM_ORGANIC | National domain metrics are used to conclude local-pack/Maps strength. | Local competitor conclusions | D; E local versus national sources |
| OSEO_COMPETITOR_COPYING_RECOMMENDED | The recommendation is to copy a competitor's content rather than answer the intent with a stronger, distinct angle. | Competitor-derived content recommendations | D; T proposed brief; E cited competitor page if needed |
| OSEO_COMPETITOR_VULNERABILITY_NO_ACTION | A claimed exploitable opening identifies no concrete page, keyword, or counter-positioning action. | Vulnerability recommendations | D; E supporting opening |
| OSEO_COMPETITOR_USER_COMPARISON_UNAVAILABLE | The report makes an own-site comparison when the user's domain/baseline is unavailable. | Competitor reports with missing own-site inputs | D; T scope; E available coverage |
| OSEO_COMPETITOR_BACKLINK_ABSENCE_OVERCLAIM | Unavailable backlink data is described as proof the competitor has weak/no links. | Authority findings | D; E provider status/coverage |

External-data limitation: a ranking table can substantiate rankings, not unseen page design or a causal explanation. Current competitor facts, the user's actual performance, and backlink strength require source captures.

## 3. keyword-clustering

Source: Goal, Workflow 1–7, Output format, and Guardrails. Actual guidance: this is page-level mapping, not just semantic grouping. Same intent and similar ranking pages can share a cluster; different intent, buyer stage, or SERP format should split. Assign existing URL, proposed new page, or do-not-target/later. Ground existing mappings in URL inventory and GSC query/page data when available. Report cannibalization only with real evidence; multiple pages with similar terms alone are insufficient. Briefs specify page type, searcher's problem, required sections, and internal links. With no URL data, label pages proposed. Fewer than ten usable terms calls for a simple map rather than elaborate clustering; it is not a ten-keyword requirement for a website.

| Proposed rule ID | Defect statement | Apply only to | Evidence required |
| --- | --- | --- | --- |
| OSEO_CLUSTER_LEXICAL_ONLY | The map groups terms solely by shared words despite supplied evidence of different SERP intents. | Keyword maps | D; E intent/SERP overlap |
| OSEO_CLUSTER_MIXED_INTENT | One target page combines incompatible search intents without explaining how it serves both. | Cluster-to-page assignments | D; E intent evidence; T page purpose |
| OSEO_CLUSTER_MIXED_STAGE | A cluster merges materially different buyer stages whose required answers conflict. | Cluster briefs | D; E/T stage and searcher problem |
| OSEO_CLUSTER_MIXED_FORMAT | Terms requiring different SERP/page formats are assigned to one page without justification. | Borderline format clusters | D; E ranking-page formats |
| OSEO_CLUSTER_DUPLICATE_TARGET_TERMS | Duplicate terms remain in a mapping in a way that creates conflicting assignments or inflated coverage. | Final keyword maps | D; entire relevant term set |
| OSEO_CLUSTER_OFF_AUDIENCE_TARGET | A recommended cluster clearly requires another product or audience. | Targeted rather than later/rejected clusters | D; T product/audience; E intent |
| OSEO_CLUSTER_UNASSIGNED | A retained cluster has no existing URL, proposed page, or explicit later/do-not-target disposition. | Final page maps | D; T existing pages |
| OSEO_CLUSTER_EXISTING_PAGE_FIT | A cluster is mapped to an existing page whose known purpose cannot answer its searcher's task. | Existing-URL assignments | D; T/E page content and intent |
| OSEO_CLUSTER_PROPOSED_AS_EXISTING | A target URL is presented as an existing verified page when no URL evidence was supplied. | Maps without verified URL inventory | D; T/E URL coverage |
| OSEO_CLUSTER_CANNIBALIZATION_OVERCLAIM | Similar wording or overlapping intended targets are described as confirmed cannibalization without real query-to-URL evidence. | Cannibalization diagnoses | D; E query/page rows or equivalent evidence |
| OSEO_CLUSTER_BRIEF_SEARCHER_TASK_MISSING | A page brief does not identify the page type and searcher's problem it is meant to solve. | Default per-cluster page briefs | D; T template/brief scope |
| OSEO_CLUSTER_BRIEF_SECTIONS_MISSING | A deliverable claiming to be a page brief provides no required content sections. | Default per-cluster briefs; not finished public pages | D; T applicable brief format |
| OSEO_CLUSTER_INTERNAL_LINK_PLAN_MISSING | A page brief omits its required internal-link plan. | Default per-cluster briefs; not every web page | D; T/E existing page inventory |

External-data limitation: actual intent divergence and cannibalization require SERP or query/page evidence. A reviewer may flag visibly missing map assignments using D alone, but should not invent a target URL, cluster volume, or preferred canonical page.

## 4. keyword-research

Source: tools descriptions, Workflow 1–10, Output format, and Guardrails. Actual guidance: prioritize business/intent fit, practical competition, useful demand/CPC signals, and local proximity over raw volume. Start with existing GSC demand when connected. Hydrate known terms with returned metrics and use SERP checks where intent would change the recommendation. Missing metrics must be `unknown`; close-variant volumes may represent one bucket. Important local nuance: a `locationName` makes volume, CPC, and competition local, while keyword ideas, KD, and intent remain national. The numeric striking-distance filters and API batch sizes are research defaults, not content defect thresholds.

| Proposed rule ID | Defect statement | Apply only to | Evidence required |
| --- | --- | --- | --- |
| OSEO_KEYWORDS_METRIC_INVENTED | A metric is filled with a numeric value that the cited data does not return or support. | Keyword metrics tables/claims | D; E source rows |
| OSEO_KEYWORDS_VOLUME_ONLY_PRIORITY | The recommendation chooses a high-volume term while ignoring a demonstrated mismatch in intent or business fit. | Prioritized keyword shortlists | D; T business goal; E candidate intents/metrics |
| OSEO_KEYWORDS_INTENT_MISMATCH | The proposed page answers a different task from the supported search intent. | Keyword-to-page recommendations | D; T page brief; E intent/SERP evidence |
| OSEO_KEYWORDS_BUSINESS_MISMATCH | The proposed target serves demand clearly unrelated to the user's offer or audience. | Keyword opportunities | D; T product/audience; E term meaning |
| OSEO_KEYWORDS_LOCAL_SCOPE_NATIONAL | National demand or organic evidence is described as locally measured demand/Maps opportunity. | City/county/service-area research | D; E tool scopes; T location |
| OSEO_KEYWORDS_LOCAL_FIELD_CONFUSION | Localized volume/CPC is used to imply that the returned KD, intent, or keyword ideas were also localized. | Location-specific metric explanations | D; E returned fields and tool semantics |
| OSEO_KEYWORDS_VARIANT_DOUBLE_COUNT | Close-variant volume buckets are added as independent demand without accounting for overlap. | Demand totals/scenarios | D; E bucket/variant definitions |
| OSEO_KEYWORDS_TARGET_PAGE_MISSING | A supposedly actionable target shortlist identifies no page to create or update. | Default shortlist/opportunity tables | D; T applicable template |
| OSEO_KEYWORDS_MISSING_METRIC_HIDDEN | An unavailable metric is silently omitted or disguised in a way that makes the prioritization appear fully evidenced. | Research risks/caveats and tables | D; E missing-field coverage |
| OSEO_KEYWORDS_AMBIGUOUS_INTENT_CERTAINTY | An acknowledged or evidenced ambiguous intent is stated as settled without a caveat or supporting SERP check. | Intent-sensitive recommendations | D; E conflicting intent evidence |
| OSEO_KEYWORDS_SOURCE_UNATTRIBUTED | The report does not identify which sources produced the material metrics or SERP observations. | Research methodology | D; E tool/source inventory |
| OSEO_KEYWORDS_MARKET_SCOPE_UNDECLARED | The recommendation omits country, language, or local scope where it materially changes the presented metrics. | Market-sensitive research reports | D; T market; E request/result scopes |

External-data limitation: do not fabricate KD, CPC, volume, seasonality, current ranking, or competitiveness. Absence of GSC access is a coverage gap; it does not prove there is no existing demand. A user goal is not a ranking guarantee.

## 5. link-prospecting

Source: Contact discovery tools, Workflow 1–9, Output format, and Guardrails. Actual guidance: explain why a real page/asset deserves citation; qualify topical editorial prospects; personalize the page-level reason and exact ask. Contact details must actually be found and include a source URL. OpenSEO discovers SEO prospects; browsing/search may discover contact paths and must receive that attribution. Flag direct competitors and likely paid placements. If no contact is found, give a specific discovery path. Drafting outreach does not authorize sending it.

| Proposed rule ID | Defect statement | Apply only to | Evidence required |
| --- | --- | --- | --- |
| OSEO_LINK_ASSET_CITATION_REASON_MISSING | The pitch gives no concrete reason the asset would be useful for this prospect to cite. | Prospect plans/outreach drafts | D; T asset/positioning; E prospect content |
| OSEO_LINK_PROSPECT_TOPICAL_MISMATCH | A recommended prospect has no supported topical or audience fit with the asset. | Qualified prospect lists | D; T asset; E prospect page |
| OSEO_LINK_UNQUALIFIED_PRIORITY | A homepage, login page, spam page, thin affiliate page, or direct competitor is given high outreach priority without a valid editorial/comparison angle. | Prioritized prospects | D; E actual page type; T angle |
| OSEO_LINK_OUTREACH_ANGLE_UNSPECIFIC | An outreach draft uses a generic benefit unrelated to the prospect page's content or need. | Personalized outreach drafts | D; E prospect page; T asset benefit |
| OSEO_LINK_EXACT_ASK_MISSING | The draft leaves the recipient unable to tell what reference, inclusion, update, or comparison mention is requested. | Outreach messages | D; T intended angle |
| OSEO_LINK_CONTACT_INVENTED | A contact name, email, or handle is asserted despite source evidence not containing it. | Contact records and outreach headers | D; E actual contact source |
| OSEO_LINK_CONTACT_SOURCE_MISSING | A recorded contact detail lacks the source URL needed to verify it. | Prospect/contact tables | D; E source capture if supplied |
| OSEO_LINK_CONTACT_TOOL_MISATTRIBUTION | Contact discovery is attributed to OpenSEO when the record shows it came from browsing, search, or another source. | Provenance claims | D; E/W source/tool records |
| OSEO_LINK_COMPETITOR_UNFLAGGED | A known direct competitor is offered as an ordinary outreach prospect without flagging that relationship. | Prospect limitations/priority | D; T competitor roster; E domain |
| OSEO_LINK_PAID_PLACEMENT_UNFLAGGED | Supplied evidence of a likely paid placement is omitted from the prospect's limitations. | Prospect qualification | D; E editorial/pricing evidence |
| OSEO_LINK_MISSING_CONTACT_NO_PATH | A prospect with no found contact is presented as ready to send without a concrete next discovery path. | Contact-incomplete prospect plans | D; E search coverage |
| OSEO_LINK_GENERIC_MASS_OUTREACH | The proposed messages form indiscriminate outreach without a page-specific reason or ask. | Outreach campaign drafts | D; T campaign scope; E target pages |

External-data limitation: lack of a supplied contact page means a contact cannot be verified, not that it is invented. Flag fabrication only with contradictory evidence or an explicit unsupported construction. Never generate guessed emails to repair a finding.

## 6. local-seo

Source: Required inputs, Workflow 1–8 including Multi-location businesses, Output format, and Guardrails. Actual guidance: identify the correct business with `cid`/`place_id`, confirm storefront coordinates, use real customer queries, compare primary/additional categories, claim status, reviews, completeness, and location-page links. Category and claim problems outrank posting cadence. Grid coverage is spatial and keyword-specific. A missing rank means not among returned results: a full set suggests outranked; a near-empty set is sparse evidence, not invisibility. Never recommend review gating, fake reviews, or keyword-stuffed business names. Multi-location snapshot scope must be clear.

| Proposed rule ID | Defect statement | Apply only to | Evidence required |
| --- | --- | --- | --- |
| OSEO_LOCAL_ENTITY_AMBIGUOUS | Findings are assigned to a business by name when supplied IDs show a different branch or similarly named listing. | Local audits/chain reports | D; E `cid`/`place_id`/branch records |
| OSEO_LOCAL_GRID_CENTER_MISMATCH | Coverage conclusions use a grid centered somewhere other than the intended storefront without disclosure. | Maps grid interpretation | D; T location; E coordinates/grid |
| OSEO_LOCAL_BRAND_QUERY_AS_CUSTOMER_DEMAND | A brand-only query is represented as evidence of generic customer-service visibility. | Local visibility conclusions | D; E exact queries; T services |
| OSEO_LOCAL_PACK_FROM_NATIONAL_METRIC | National organic metrics are asserted to prove Maps/local-pack strength. | Local ranking diagnoses | D; E metric scopes |
| OSEO_LOCAL_PRIORITY_IGNORES_SETUP_BLOCKER | Posting cadence is prioritized over a demonstrated category or claim-status problem without explaining why. | Prioritized local action plans | D; E profile evidence |
| OSEO_LOCAL_WRONG_LOCATION_LINK | A listing is described as correctly linked while supplied evidence points to a homepage, wrong location, or stale domain. | Listing website-link assessments | D; T project/location URLs; E listing link |
| OSEO_LOCAL_REVIEW_DIAGNOSIS_UNSUPPORTED | A review-strength diagnosis rests solely on count while claiming conclusions about recency, rating, or owner replies that were not checked. | Review comparisons | D; E review dates, ratings, reply fields |
| OSEO_LOCAL_MISSING_RANK_INVISIBILITY | A missing grid rank is described as proof the business is invisible. | Grid coverage prose | D; E rank/result count for that point |
| OSEO_LOCAL_SPARSE_SERP_OUTRANKED | A near-empty result set is interpreted as a full competitive loss without acknowledging sparse coverage. | Grid-point diagnoses | D; E point `resultsCount` and returned rows |
| OSEO_LOCAL_MAP_SCOPE_OMITTED | Coverage claims omit the keyword/location or map extent needed to interpret them. | Maps coverage summaries | D; E grid specification |
| OSEO_LOCAL_STOREFRONT_AS_AREA_COVERAGE | A storefront-only ranking is asserted to establish service-area visibility. | Spatial generalizations | D; E grid or single-point scope |
| OSEO_LOCAL_CHAIN_SCOPE_HIDDEN | A chain-wide conclusion hides that the evidence covers only selected branches. | Multi-location reports | D; T complete branch roster; E sampled branches |
| OSEO_LOCAL_REVIEW_GATING_ADVICE | The recommendation gates review solicitation based on customer satisfaction. | Local growth/review recommendations | D; exact proposed flow |
| OSEO_LOCAL_FAKE_REVIEW_ADVICE | The recommendation asks for fabricated or purchased fake reviews. | Review recommendations | D; exact proposal |
| OSEO_LOCAL_STUFFED_NAME_ADVICE | The recommendation adds service keywords to the business name rather than using its real name. | Business-profile recommendations | D; T known business name |

External-data limitation: local visibility changes by query, position, radius, branch, and time. Do not translate a missing rank into a universal defect or treat a single coordinate as the entire service area. Recommendations about claims, reviews, and names can be assessed as advice; actual profile defects require profile evidence. Paid-grid cost confirmation is a workflow safeguard, not a public-page requirement.

## 7. seo-audit

Source: Inputs/context; tools; Workflow 1–6; Output format; Guardrails. Actual guidance has several directly useful page checks: read main content rather than shared navigation, answer the searcher's actual decision with specific accurate sourced information, detect sibling pages that only substitute a vendor/location/keyword, and distinguish switching/comparison questions from competitor-pricing questions. Check technical basics on named pages with real evidence.

Its report methodology is unusually explicit: rankings that drive recommendations require live checks; returned raw rank counts all result blocks, so count organic listings and report `#10 (page 1)`/`#11 (page 2)`; absence beyond checked depth and failed lookups are different. Provider metric dates are not ranking dates. One snapshot is not a baseline; same-day changes are not trends. Choose a bounded demonstrated opportunity rather than the loudest crawler warning. Account for every serious shortlist row, explain why the leader beats the runner-up, protect pages already near the top, and put supporting evidence in a self-contained disclosure. Benefit estimates must distinguish volume from visits, total from additional potential, overlaps, geography, assumptions, and hypothetical scenarios.

| Proposed rule ID | Defect statement | Apply only to | Evidence required |
| --- | --- | --- | --- |
| OSEO_AUDIT_PAGE_QUESTION_UNANSWERED | Changed main content fails to answer the searcher's known decision/question and substitutes generic assertions. | Search-targeted page copy with a known intent/brief | D; T searcher task; E intent if contested |
| OSEO_AUDIT_SIBLING_TOKEN_SWAP | Changed sibling copy substitutes only a name/location/keyword while leaving material decision-specific questions unanswered. | Templated comparison, pricing, service, or location pages | D; T/E sibling main content and user task |
| OSEO_AUDIT_PRICING_SWITCHING_INTENT_MIXED | A page meant to answer pricing or switching substitutes the other question's generic answer. | Competitor pricing versus comparison/alternative families | D; T page purpose; E intent/pages |
| OSEO_AUDIT_TECH_DEFECT_UNSUPPORTED | A named status, canonical, indexing, or internal-access defect is asserted without corresponding page/crawl evidence. | Technical audit findings | D; E response, HTML directives, or link graph |
| OSEO_AUDIT_FAMILY_OVERGENERALIZATION | A site-wide/page-family diagnosis is claimed from a limited sample without disclosing coverage or accounting for contrary sampled siblings. | Family-level audit conclusions | D; E sample and sibling results |
| OSEO_AUDIT_RANK_UNVERIFIED | A ranking claim driving a recommendation is presented as current without a live observation made for the audit. | Audit recommendation ranking claims | D; E query, matching URL, observation date and SERP capture |
| OSEO_AUDIT_ORGANIC_RANK_CONVENTION | A raw result-block rank is reported as organic rank or a position lacks the page convention needed by the audit. | Audit ranking tables | D; E organic listing count/order |
| OSEO_AUDIT_ABSENCE_OVER_DEPTH | Not seeing a page in checked results is presented as having no ranking rather than absence within the checked depth. | Negative ranking claims | D; E successful lookup/depth |
| OSEO_AUDIT_LOOKUP_FAILURE_AS_ABSENCE | A failed lookup is reported as “not in the first 20 results.” | Failed SERP checks | D; E error/status |
| OSEO_AUDIT_RANK_DATE_CONFUSION | Retrieval time or a keyword-metric update date is presented as the ranking observation date. | Dates in ranking evidence | D; E distinct timestamp fields |
| OSEO_AUDIT_SAME_DAY_VARIATION_TREND | Two same-day positions are described as a sustained rise/fall or trend. | Ranking change narratives | D; E observation times/history |
| OSEO_AUDIT_ONE_SNAPSHOT_BASELINE | One ranking snapshot is treated as a stable baseline for change or causal measurement. | Baseline/effect claims | D; E time coverage |
| OSEO_AUDIT_DOMAIN_SAMPLE_NO_RANKINGS | A page's absence from a limited domain keyword sample is asserted to prove it has no rankings. | Provider sample interpretation | D; E domain-sample scope and page coverage |
| OSEO_AUDIT_OBSERVATION_AS_CAUSE | Similar copy, a crawler warning, or missing provider data is said to prove a penalty, exclusion, or ranking cause. | Causal diagnoses | D; E actual evidence and competing explanations |
| OSEO_AUDIT_ESTIMATE_AS_MEASURED | Domain provider traffic/keyword counts are described as observed visits or as having a single measured observation date. | Orientation metrics | D; E provider definitions |
| OSEO_AUDIT_SHORTLIST_DISPOSITION_MISSING | A material serious candidate or diagnosis disappears from both recommendations and “What else we checked.” | Audit reports with supplied shortlist | D; E shortlist and diagnoses |
| OSEO_AUDIT_RUNNER_UP_REASON_MISSING | The report does not explain why the leading opportunity beats the strongest rejected candidate. | Audit choice rationale | D; E shortlist evidence |
| OSEO_AUDIT_LEAD_NO_DEMONSTRATED_PROBLEM | A leading recommendation relies solely on ease, raw volume, crawler severity, or hypothetical rank-one traffic without demonstrating a relevant problem. | Top audit recommendations | D; T goal; E candidate evidence |
| OSEO_AUDIT_WINNING_PAGE_REWRITE | The recommendation broadly rewrites a page already ranking near the top for its target query without an evidenced need to correct or protect it. | Page rewrite recommendations | D; E current ranking and content defect |
| OSEO_AUDIT_BENEFIT_MECHANISM_MISSING | Claimed benefit does not identify whether the action creates a ranking, improves a position, or improves clicks at the same position. | Quantified audit benefit scenarios | D; E current visibility; T action |
| OSEO_AUDIT_VARIANT_OVERLAP_SUMMED | Benefit sizing adds overlapping query variants as distinct searchers. | Cluster-based demand/visit scenarios | D; E variant overlap and formula |
| OSEO_AUDIT_GEOGRAPHY_UPSCALED | US demand is multiplied into an invented global opportunity or labeled as another market without evidence. | Opportunity sizing | D; E geography and calculation |
| OSEO_AUDIT_VOLUME_AS_VISITS | Search volume is presented directly as expected website visits. | Benefit calculations | D; E demand and formula |
| OSEO_AUDIT_CLICK_SHARE_HIDDEN | A visit estimate uses an undisclosed click-share assumption. | Volume-to-visits scenarios | D; E calculation/assumptions |
| OSEO_AUDIT_UNKNOWN_BASELINE_INCREMENTAL | Total potential visits are labeled additional visits despite an unknown current traffic baseline. | Incremental benefit claims | D; E known/unknown baseline |
| OSEO_AUDIT_HYPOTHETICAL_RANK_PROMISE | A position-one scenario is written as a promised or forecast ranking/traffic outcome. | Hypothetical scenarios | D; E scenario assumptions |
| OSEO_AUDIT_CONVERSION_REVENUE_INVENTED | A conversion rate or revenue estimate is invented to strengthen the recommendation. | Business-benefit numbers | D; T/E verified funnel or commercial data |
| OSEO_AUDIT_BUSINESS_FIT_INFERENCE_HIDDEN | Inferred commercial relevance is stated as observed conversion evidence. | Qualified-demand arguments | D; T product fit; E measured outcomes if claimed |
| OSEO_AUDIT_BENEFIT_UNCERTAINTY_SEPARATED | The stated benefit omits or obscures the main uncertainty that materially limits it. | Recommendation Why/benefit passages | D; E known limits |
| OSEO_AUDIT_EVIDENCE_APPENDIX_INCOMPLETE | The audit's required self-contained evidence disclosure omits material query, geography/language, date, returned organic count, URL, sample, or calculation details needed to reproduce a leading claim. | Default SEO audit report methodology, unless template changes section organization only | D; E underlying records; check each omitted field independently in implementation |
| OSEO_AUDIT_LOCAL_PATH_AS_EVIDENCE | A local file path is offered as the sole evidence for a reader of the shared report. | Self-contained audit reports | D; linked/embedded evidence coverage |

External-data limitation: ContentGuard should not perform the original audit during review. Without E, current rank, canonical/indexing state, a technical cause, business conversions, and sample sufficiency cannot be verified. A report can still be checked for falsely equating concepts, missing disclosures, faulty formulas, and explicit contradictory evidence. The last appendix rule is a catalog family: implementation should separate field checks rather than one omnibus Jev score.

## 8. seo-coach

Source: Response format; Coach answers vs. skill reports; Tool coaching; Coaching patterns; Guardrails. Actual guidance: short orientation in chat, answer/one next step first, beginner-friendly explanations, a plain-language gloss for numbers, and only the next needed input. A deeper analysis/shareable deliverable hands off to the relevant workflow/report. Explain the distinct capabilities of OpenSEO, GSC, browsing, local files, shared context, and reports; do not claim OpenSEO browses arbitrary pages or finds contacts itself. This is a chat/orchestration skill, not a landing-page copy standard.

| Proposed rule ID | Defect statement | Apply only to | Evidence required |
| --- | --- | --- | --- |
| OSEO_COACH_ANSWER_BURIED | The coach response postpones the requested answer or next action behind introductory explanation. | Explicit OpenSEO coaching output | D; user task |
| OSEO_COACH_NUMBER_GLOSS_MISSING | An unfamiliar metric is introduced without explaining what its number means in ordinary language. | Beginner-oriented coach replies | D; T known audience experience |
| OSEO_COACH_NEXT_STEP_OVERLOAD | The response overwhelms orientation with an unprioritized workflow menu rather than one next action or a few concrete choices. | Coach next-action advice | D; T goal/context |
| OSEO_COACH_TOOL_CAPABILITY_FALSE | The response claims OpenSEO itself browses arbitrary pages or discovers contacts when that capability belongs to other tools. | Tool coaching | D; T/E actual tool capabilities |
| OSEO_COACH_SOURCE_TYPES_BLENDED | SEO tool data, first-party GSC, web evidence, local files, and coaching judgment are presented as the same evidentiary source. | Evidence explanations | D; E/W provenance |
| OSEO_COACH_FULL_REPORT_WRONG_DELIVERY | A requested full/shareable analysis is claimed delivered as a fleeting coach answer without the promised workflow/report artifact. | Explicit full-report requests in coaching | D; W deliverable record; user request |
| OSEO_COACH_STRATEGY_NO_BUSINESS_FIT | A suggested strategic topic/workflow conflicts with known business goals and positioning. | Coach strategy recommendations | D; T goals/business |
| OSEO_COACH_KNOWN_CONTEXT_REASKED | The response requires information already supplied in trusted project context and offers no need to confirm/correct it. | Coach intake/next-input prompts | D; T available context |

External-data limitation: do not impose the coach's under-a-screen format or closing-question conventions on public copy, research reports, or this research catalog. Claims that a report exists, GSC is connected, or prior research returned a result require W/E. A missing output record is not proof the external artifact does not exist.

## 9. seo-project-setup

Source: Checklist 1–10; Output format; Guardrails. Actual guidance: confirm scope, goals with metric/timeframe, positioning, voice restrictions, competitor reasons, curated key-page roles/topics, and GSC status; merge new answers into existing context. Confirm inferred facts before saving. Never claim to see an uploaded CSV or a connected GSC integration without observation. It is a context setup workflow, explicitly not a full audit; it does not require website pages to contain all project-context fields. Example targets such as top-ten rankings are examples of user goals, not default performance demands.

| Proposed rule ID | Defect statement | Apply only to | Evidence required |
| --- | --- | --- | --- |
| OSEO_SETUP_SCOPE_LOCALE_INCONSISTENT | The setup record contradicts confirmed domains, products, countries, languages, or site stage. | Setup/context summaries | D; T confirmed scope |
| OSEO_SETUP_GOAL_METRIC_TIMEFRAME_MISSING | A setup marked complete contains no success metric or timeframe for a goal that required clarification. | Completed goal intake | D; T agreed goal; not a required field on public pages |
| OSEO_SETUP_POSITIONING_AUDIENCE_MISSING | Completed positioning omits who the product/site is for. | Completed positioning context | D; T agreed audience |
| OSEO_SETUP_POSITIONING_PROBLEM_MISSING | Completed positioning omits the pain/problem the product solves. | Completed positioning context | D; T agreed problem |
| OSEO_SETUP_POSITIONING_DIFFERENTIATOR_MISSING | Completed positioning omits why users choose it over alternatives. | Completed positioning context | D; T agreed differentiation |
| OSEO_SETUP_UNCONFIRMED_INFERENCE_AS_FACT | A site-derived guess is saved or summarized as an agreed business fact without confirmation. | Setup evidence/provenance claims | D; T/W confirmed answers |
| OSEO_SETUP_VOICE_PREFERENCES_LOST | A context update discards known voice restrictions, banned phrases, or avoided topics without an authorized change. | Writing-preference updates | D; T previous preferences and authorization |
| OSEO_SETUP_COMPETITOR_REASON_MISSING | A saved competitor list provides no reason the domain matters to the project. | Setup competitor entries | D; T competitor relation; E research if inferred |
| OSEO_SETUP_ASSET_ROLE_MISSING | A saved key page lacks its required role or misstates a known topic. | Setup key-page records | D; T URL purpose; topic required only when known |
| OSEO_SETUP_GSC_CONNECTION_FALSE | The setup claims GSC is connected despite supplied live evidence returning “not connected.” | Integration status claims | D; W actual response |
| OSEO_SETUP_FILE_UPLOAD_FALSE | The setup claims an export/upload was received despite no observable file or a contradictory supplied file record. | File-intake status claims | D; W visible files/intake record |
| OSEO_SETUP_SAVE_STATUS_FALSE | The setup claims context/competitors/pages were saved despite supplied records showing a failed or absent attempted write. | Completed-action claims with available workflow record | D; W returned save/update status |
| OSEO_SETUP_CONTEXT_MERGE_LOSS | A section update replaces existing valid context and silently loses material agreed information. | Context replacements | D; T full previous section and intended update |

External-data limitation: only assess saved/connected/uploaded status when W establishes what actually happened. A staged Markdown file is not the OpenSEO project state. Workflow steps such as asking in small batches, native integration preference, curated inventory size, optional local folders, or app UI navigation do not become universal content checks.

## 10. seo-report

Source: Before you write; Following a template; Writing rules; Title and summary; closing section; HTML constraints; Public sharing; Starter template; The primitives; Guardrails. Actual guidance: one self-contained HTML report in the intended project, a clear verdict and business implication, evidence-backed actions/benefits and honest uncertainty, concise scan-friendly writing, first-use explanations, and printed chart values. The producing skill's recommendation structure overrides generic Problem/Change/Expected effect. A requested matching project template can replace section organization, audience, and tone, but not HTML constraints or writing rules; project voice preferences still apply except conflicting template tone.

Title requirements are platform-specific: named report type/subject, actual full report date, under 120 characters, correct hostname treatment, and identical saved title/HTML title/H1. Summary is under 2,500 characters and must stand on its own. Last section is “How this report was made,” with producing-skill docs link, agent/date, and source/verification provenance. Viewer constraints include no external resources, no scripts, inline CSS, complete document ending in `</html>`, valid links and charts, and a 500,000-byte hard cap. The 80 KB recommendation is an aim, not a failure threshold. Only explicitly requested public sharing authorizes publication; private app URLs are not public links.

| Proposed rule ID | Defect statement | Apply only to | Evidence required |
| --- | --- | --- | --- |
| OSEO_REPORT_TITLE_TYPE_DATE | The title lacks a specific report type/subject or the actual full report date, uses a generic title, or exceeds the documented title bound. | OpenSEO saved report titles | D; W report date; exact bound from source |
| OSEO_REPORT_TITLE_SUBJECT_HOST | The title uses a full URL or wrong hostname treatment for the project/competitor subject. | OpenSEO report titles | D; T project hostname and report subject |
| OSEO_REPORT_TITLE_MISMATCH | Saved title, document title, and visible H1 differ. | OpenSEO HTML plus save metadata | D; W submitted title |
| OSEO_REPORT_SUMMARY_VERDICT_MISSING | The standalone saved summary omits the report's verdict. | Saved report summaries | D; report body |
| OSEO_REPORT_SUMMARY_ACTION_BENEFIT_MISSING | The summary omits the leading recommendation/benefit or why no material action was established. | Saved summaries | D; supported report conclusion |
| OSEO_REPORT_SUMMARY_EVIDENCE_MISSING | The summary omits the key evidence needed by a reader who never opens the HTML. | Saved summaries | D; report evidence |
| OSEO_REPORT_SUMMARY_OVERSIZE | The saved summary exceeds its documented character bound. | OpenSEO summary field | D; source bound under 2,500 characters |
| OSEO_REPORT_TEMPLATE_UNREQUESTED | A report claims to follow an arbitrary project template that the user's requested report kind did not select. | Template selection claims | D; T templates and user request; W selected template |
| OSEO_REPORT_TEMPLATE_STRUCTURE_WRONG | A selected applicable template's required audience/sections/order are not followed. | Explicitly selected template reports | D; T exact template |
| OSEO_REPORT_PRODUCER_FORMAT_OVERRIDDEN | Generic finding markup replaces the producing skill's explicitly required recommendation structure. | Producing skill with a specified structure, particularly seo-audit | D; T producing skill/template precedence |
| OSEO_REPORT_WRITING_PREFERENCE_CONFLICT | The report violates trusted project writing preferences without a conflicting selected template tone. | Reports with applicable preferences | D; T preferences and template |
| OSEO_REPORT_FINDING_PROBLEM_MISSING | A recommendation gives a fix but no observed gap/evidence identifying why it is warranted. | Prescriptive report findings | D; E observed evidence |
| OSEO_REPORT_ACTION_NONCONCRETE | A recommended action is too vague to tell what changes on which page or asset. | Prescriptive report findings | D; T/E named scope |
| OSEO_REPORT_BENEFIT_NO_MECHANISM | Expected benefit is generic or disconnected from how the recommended change addresses the gap. | Expected-effect/Why passages | D; T business goal; E gap |
| OSEO_REPORT_UNSUPPORTED_PRESCRIPTION | The report invents a fix merely to fill the report format despite research establishing no worthwhile action. | Conclusions with no supported material action | D; E findings/limits |
| OSEO_REPORT_METRIC_PROVENANCE_MISSING | Material numbers are not distinguished as measured outcomes, tool estimates, or hypotheses. | Numeric observations/scenarios | D; E metric definitions |
| OSEO_REPORT_UNVERIFIED_LIMIT_HIDDEN | An unverified material claim is presented confidently with no caveat describing the checking limit. | Report confidence passages | D; E/W coverage |
| OSEO_REPORT_FIRST_USE_GLOSS_MISSING | A material SEO term of art is used without its first-use plain-language explanation for the intended audience. | Nonexpert OpenSEO reports | D; T audience; whole report first occurrence |
| OSEO_REPORT_CHART_NUMBER_UNPRINTED | A quantitative chart carries a value not also written as readable text. | Report charts | D; chart values and adjacent text |
| OSEO_REPORT_HOW_MADE_MISSING | The required final methodology section is absent or not last. | All OpenSEO reports, including templates | D; report section structure |
| OSEO_REPORT_ATTRIBUTION_INVALID | The methodology opening gives the wrong producing skill/docs slug, omits agent/date, or misattributes tool findings versus manual verification. | Methodology provenance | D; T producing skill; E/W sources/run identity |
| OSEO_REPORT_EXTERNAL_RESOURCE | The HTML depends on remote fonts, images, styles, scripts, or fetched data blocked by the viewer. | OpenSEO HTML reports only | D; complete HTML/resource references |
| OSEO_REPORT_SCRIPT_BLOCKED | The report relies on a script for displayed content or interaction. | OpenSEO HTML reports only | D; script markup/dependencies |
| OSEO_REPORT_LINK_FRAME_NAVIGATION | An external link lacks the required new-tab and `noopener` behavior, or an in-page anchor wrongly leaves the document. | OpenSEO report links | D; href/target/rel |
| OSEO_REPORT_CHART_RENDERING_INVALID | A chart uses unsupported remote/script rendering, or inline SVG lacks a viewBox or real text labels needed by the documented primitive. | OpenSEO chart markup | D; full chart markup |
| OSEO_REPORT_HTML_SIZE_CAP | The document exceeds the viewer's 500,000-byte hard cap. | Complete serialized OpenSEO HTML | D; exact encoded byte size; do not fail merely for exceeding the 80 KB aim |
| OSEO_REPORT_LITERAL_UNSAFE | HTML contains a backtick or template interpolation opener forbidden by the documented save path. | OpenSEO HTML payload only | D; exact literal characters; this is transport-specific |
| OSEO_REPORT_DOCUMENT_INCOMPLETE | The complete payload does not end with the required closing HTML element. | OpenSEO HTML saves | D; full payload, not a truncated display |
| OSEO_REPORT_DOCUMENT_SHELL_MISSING | The document omits doctype, HTML, head, or title required for whole-document rendering. | OpenSEO HTML reports | D; complete document |
| OSEO_REPORT_CONTENTS_TARGET_BROKEN | A contents link fails to target its section, or a required H2 has no ID/contents entry. | OpenSEO starter-template reports | D; heading and anchor map |
| OSEO_REPORT_HEADING_LEVEL_SKIPPED | The report skips the documented H2/H3 finding hierarchy. | OpenSEO report article structure | D; heading sequence |
| OSEO_REPORT_NUMERIC_ALIGNMENT_MISSING | Numeric table headers/cells omit the documented numeric class in a way that harms comparison. | OpenSEO template numeric tables | D; table markup |
| OSEO_REPORT_TABLE_PRINT_WIDTH | A report table disregards the compact table primitive and is demonstrably unreadable or clipped for the intended viewer/print context. | OpenSEO report tables | D; layout evidence; source recommends five columns but link-prospecting allows about eight, so do not use a universal count failure |
| OSEO_REPORT_PUBLIC_LINK_FALSE | A private app URL is described as a public share link or public sharing is claimed despite a failed sharing response. | Sharing claims | D; W successful sharing status and URL |

External-data limitation: viewer validity can often be judged from complete HTML and metadata, but cannot be judged from a truncated tool display. Exact structural evidence should be extracted locally rather than asking Jev to count bytes or characters. Do not assume every HTML file targets this viewer. Public-sharing authorization and actual publishing actions belong in workflow controls; this catalog checks claims only when applicable. Save deduplication, report IDs, ownership/project destination, and preserving sharing settings are tool-orchestration requirements rather than public-page content criteria.

## Recommended canonical rules and conditional routes

The 159 entries above preserve extraction/provenance; they are **not** a recommendation to activate 159 checks. Recommend the following **35 semantic canonical checks** for the SEO/research extension, with shared writing, unsupported-claim, actionability, uncertainty, audience-fit, and factual-accuracy checks supplied by the wider ContentGuard catalog. Several of these 35 may in turn alias those shared rules. Do not also run their source-level aliases. A canonical rule must report the particular changed claim/assignment it evaluated, not return a whole-artifact quality grade.

The table identifies exact supporting evidence and source-candidate aliases. Grouped aliases describe the same defect predicate in different artifact families; they are not instructions to score every listed source requirement at once. The original per-skill tables remain the provenance record for all 159 candidates, including ones not recommended for initial activation.

| Canonical proposed ID | Defect predicate and exact evidence minimum | Source candidates / provenance |
| --- | --- | --- |
| CGR_SEO_ESTIMATE_AS_MEASURED | A changed statement calls an estimated provider metric measured traffic. Need the statement and provider field definition. | LANDSCAPE_ESTIMATE_AS_EXACT; AUDIT_ESTIMATE_AS_MEASURED; COMPETITOR_FIRST_PARTY_UNACKNOWLEDGED only for the estimate-versus-measured distinction |
| CGR_SEO_MARKET_SCOPE_MISSTATED | A metric is labeled as covering a market/locality it does not cover. Need the statement, field-level country/locality/language semantics, and requested market. | KEYWORDS_LOCAL_SCOPE_NATIONAL; KEYWORDS_LOCAL_FIELD_CONFUSION; AUDIT_GEOGRAPHY_UPSCALED |
| CGR_SEO_METRIC_UNSUPPORTED | A numeric claim contradicts or invents a value absent from an identified source. Need the changed value and actual source rows/formula; missing source alone is insufficient to prove fabrication. | KEYWORDS_METRIC_INVENTED; AUDIT_CONVERSION_REVENUE_INVENTED; REPORT_METRIC_PROVENANCE_MISSING maps only when a value is actually unsupported |
| CGR_SEO_DEMAND_DOUBLE_COUNTED | A demand total treats overlapping buckets/variants as independent people. Need term-level source bucket definitions and the actual summation. | KEYWORDS_VARIANT_DOUBLE_COUNT; AUDIT_VARIANT_OVERLAP_SUMMED |
| CGR_SEO_VOLUME_AS_VISITS | A stated visit figure equals demand without a supported click-share transformation. Need demand units and the displayed calculation/claim. | AUDIT_VOLUME_AS_VISITS |
| CGR_SEO_CLICK_SHARE_UNDISCLOSED | A volume-to-visits scenario depends on a click-share assumption that is not disclosed. Need full scenario and formula; do not invent a benchmark CTR. | AUDIT_CLICK_SHARE_HIDDEN |
| CGR_SEO_INCREMENTAL_BASELINE_UNKNOWN | Total potential visits are labeled additional visits although current traffic is unknown. Need the claim/formula and explicit baseline coverage. | AUDIT_UNKNOWN_BASELINE_INCREMENTAL |
| CGR_SEO_SCENARIO_AS_PROMISE | A hypothetical ranking/visit scenario is stated as an expected guaranteed outcome. Need the changed promise and the scenario assumptions. | AUDIT_HYPOTHETICAL_RANK_PROMISE |
| CGR_SEO_RANK_KIND_WRONG | A raw result-block position is stated as organic rank. Need the claimed position and ordered SERP result types. | AUDIT_ORGANIC_RANK_CONVENTION |
| CGR_SEO_RANK_ABSENCE_OVERCLAIM | Limited successful result/sample coverage is stated as proof of no ranking. Need the negative claim, successful response, checked depth/sample scope, and matched URL. | AUDIT_ABSENCE_OVER_DEPTH; AUDIT_DOMAIN_SAMPLE_NO_RANKINGS |
| CGR_SEO_LOOKUP_FAILURE_AS_ABSENCE | An error/failed lookup is stated as a negative ranking result. Need the negative claim and exact failed status; distinguish from a successful empty response. | AUDIT_LOOKUP_FAILURE_AS_ABSENCE |
| CGR_SEO_RANK_DATE_WRONG | A non-ranking timestamp is labeled the ranking observation date. Need the claimed date and source fields distinguishing rank observation, metric update, and retrieval. | AUDIT_RANK_DATE_CONFUSION |
| CGR_SEO_TEMPORAL_CLAIM_UNSUPPORTED | A trend or stable baseline is asserted from insufficient temporal observations. Need the claim and complete supplied dated observations; no arbitrary minimum history. | AUDIT_SAME_DAY_VARIATION_TREND; AUDIT_ONE_SNAPSHOT_BASELINE |
| CGR_SEO_CAUSE_UNSUPPORTED | A correlation/crawl warning/missing provider row is said to prove a ranking cause, penalty, or exclusion. Need the causal sentence and evidence actually offered; evaluate the inference rather than asserting another cause. | AUDIT_OBSERVATION_AS_CAUSE; COMPETITOR_INFERENCE_AS_OBSERVATION when the inference is causal |
| CGR_SEO_PAGE_PATTERN_UNOBSERVED | A page/content pattern is claimed as observed from data that cannot show it. Need the claim and source types; verify whether any page/SERP capture supports it. | COMPETITOR_PATTERN_FROM_KEYWORDS; LANDSCAPE_PATTERN_EVIDENCE_MISSING |
| CGR_SEO_COMPETITOR_TYPE_CONFUSED | Search overlap is represented as direct business competition or a publisher as a product competitor. Need the classification, domain role, and trusted offer/positioning. | LANDSCAPE_DOMAIN_TYPE_MISSING; LANDSCAPE_BUSINESS_SEARCH_CONFUSED |
| CGR_SEO_TARGET_INTENT_MISMATCH | A recommended page's answer conflicts with supported searcher intent. Need the brief/main content plus trusted intent or supplied SERP evidence. | KEYWORDS_INTENT_MISMATCH; CLUSTER_EXISTING_PAGE_FIT; AUDIT_PAGE_QUESTION_UNANSWERED; AUDIT_PRICING_SWITCHING_INTENT_MIXED |
| CGR_SEO_CLUSTER_INTENT_CONFLICT | A single mapped page combines incompatible intents/stages/formats. Need the retained terms, target page, and evidence of incompatible answers; lexical overlap alone cannot prove compatibility. | CLUSTER_LEXICAL_ONLY; CLUSTER_MIXED_INTENT; CLUSTER_MIXED_STAGE; CLUSTER_MIXED_FORMAT |
| CGR_SEO_TARGET_ASSIGNMENT_MISSING | A retained target cluster/keyword has no existing page, proposed page, or explicit later/reject disposition. Need the complete relevant map and declared deliverable scope. | CLUSTER_UNASSIGNED; KEYWORDS_TARGET_PAGE_MISSING |
| CGR_SEO_PROPOSED_URL_AS_EXISTING | A proposed page is labeled existing/verified without URL support. Need the changed label and available trusted page inventory, or an explicit absence-of-URL-data disclaimer. | CLUSTER_PROPOSED_AS_EXISTING |
| CGR_SEO_CANNIBALIZATION_UNSUPPORTED | Confirmed cannibalization is asserted from similarity/intended overlap alone. Need the diagnosis and query-to-URL evidence; intended overlap may be called a risk. | CLUSTER_CANNIBALIZATION_OVERCLAIM |
| CGR_SEO_RECOMMENDATION_DIAGNOSIS_MISSING | A leading audit recommendation has no demonstrated relevant gap and relies only on ease, raw volume, warning level, or hypothetical traffic. Need the recommendation, cited evidence, and trusted business goal. | AUDIT_LEAD_NO_DEMONSTRATED_PROBLEM; REPORT_FINDING_PROBLEM_MISSING; REPORT_UNSUPPORTED_PRESCRIPTION |
| CGR_SEO_SELECTION_RATIONALE_MISSING | A serious rejected opportunity has no evidence-based disposition or the leader/runner-up choice lacks a reason. Need the full supplied shortlist and complete recommendations/checked table. | AUDIT_SHORTLIST_DISPOSITION_MISSING; AUDIT_RUNNER_UP_REASON_MISSING |
| CGR_SEO_WINNING_PAGE_REWRITE | A broad rewrite is recommended for a known near-top target page without an evidenced corrective need. Need the exact action, current target-query observation, and any claimed defect. | AUDIT_WINNING_PAGE_REWRITE |
| CGR_SEO_LOCAL_ENTITY_MISMATCH | A finding uses the wrong branch/business identity. Need the finding's entity, intended storefront, and supplied stable IDs. | LOCAL_ENTITY_AMBIGUOUS |
| CGR_SEO_LOCAL_SCOPE_OVERCLAIM | A local conclusion claims coverage outside the actual sampled branch, coordinate, keyword, or extent. Need the conclusion, intended scope, and exact grid/sample specification. | LOCAL_GRID_CENTER_MISMATCH; LOCAL_MAP_SCOPE_OMITTED; LOCAL_STOREFRONT_AS_AREA_COVERAGE; LOCAL_CHAIN_SCOPE_HIDDEN |
| CGR_SEO_LOCAL_ABSENCE_OVERCLAIM | Not appearing in returned local results is described as general invisibility or a full-set loss despite sparse results. Need the statement and each relevant point's rank, resultsCount, and returned rows. | LOCAL_MISSING_RANK_INVISIBILITY; LOCAL_SPARSE_SERP_OUTRANKED |
| CGR_SEO_LOCAL_PACK_FROM_ORGANIC | Organic/national evidence is stated to establish Maps/local-pack performance. Need the performance claim and source channel/scope. | LANDSCAPE_LOCAL_ORGANIC_CONFUSED; COMPETITOR_LOCAL_STRENGTH_FROM_ORGANIC; LOCAL_PACK_FROM_NATIONAL_METRIC |
| CGR_SEO_CONTACT_FABRICATED | A contact detail is contradicted by its cited source or explicitly constructed without evidence. Need the stated detail and actual source capture or generation admission. | LINK_CONTACT_INVENTED |
| CGR_SEO_CONTACT_PROVENANCE_MISSING | A contact detail lacks a source URL or attributes discovery to a tool that did not return it. Need contact fields and the source/tool record. | LINK_CONTACT_SOURCE_MISSING; LINK_CONTACT_TOOL_MISATTRIBUTION |
| CGR_SEO_OUTREACH_UNPERSONALIZED | An outreach ask lacks a prospect-page-specific reason to cite the asset. Need the message, actual prospect page, asset benefit, and intended ask. | LINK_ASSET_CITATION_REASON_MISSING; LINK_OUTREACH_ANGLE_UNSPECIFIC; LINK_EXACT_ASK_MISSING; LINK_GENERIC_MASS_OUTREACH |
| CGR_SEO_PROSPECT_CONFLICT_HIDDEN | A known competitor/likely paid placement is presented as an ordinary editorial prospect without disclosure. Need prospect identity and trusted competitor/paid-placement evidence. | LINK_COMPETITOR_UNFLAGGED; LINK_PAID_PLACEMENT_UNFLAGGED |
| CGR_SEO_COMPLETION_STATUS_FALSE | A completed connection/upload/save/publication is claimed despite supplied contradictory execution evidence. Need the exact completion claim and actual status response/file observation; no response means unknown. | SETUP_GSC_CONNECTION_FALSE; SETUP_FILE_UPLOAD_FALSE; SETUP_SAVE_STATUS_FALSE; REPORT_PUBLIC_LINK_FALSE |
| CGR_SEO_CONTEXT_FACT_LOST | A context update discards material previously confirmed information without an authorized change. Need full before/after sections and the requested update. | SETUP_CONTEXT_MERGE_LOSS; SETUP_VOICE_PREFERENCES_LOST |
| CGR_SEO_REPORT_PROVENANCE_MISSING | An SEO report omits producing workflow/source/verification provenance needed to interpret material conclusions. Need the complete report and known producing workflow/source inventory; this checks disclosure, not truth of missing data. | KEYWORDS_SOURCE_UNATTRIBUTED; REPORT_HOW_MADE_MISSING; REPORT_ATTRIBUTION_INVALID; AUDIT_LOCAL_PATH_AS_EVIDENCE |

Source aliases in this crosswalk omit the common `OSEO_` prefix for readability. For example `AUDIT_RANK_DATE_CONFUSION` refers to `OSEO_AUDIT_RANK_DATE_CONFUSION` above. These canonical entries are recommendations, and the wider catalog can supply stricter one-to-one aliases where it already has the same defect.

### Route predicates

Determine the artifact using trusted configured path/type/frontmatter and the changed artifact's actual purpose. Do not infer a research-report route merely because a page mentions rankings or search volume. All routes still sit after the deterministic content-presence gate and Jev content-task cutoff.

| Conditional route | Positive identification | Applicable canonical subset and inputs | Checks to exclude |
| --- | --- | --- | --- |
| Public search page | Finished public copy answering an identified search task | TARGET_INTENT_MISMATCH with D+T/E; shared page-specificity and supported-claims checks; source candidate AUDIT_SIBLING_TOKEN_SWAP with actual siblings | Report provenance, shortlist, grids, setup, contact discovery, OpenSEO viewer |
| Keyword research artifact | A supplied research table/plan with candidate terms, metric fields, and proposed targets | Metric/scope/estimate, demand double-count, target assignment, intent; D+T and E metric definitions/results | Live-rank or GSC requirements when those claims are not made |
| Cluster map or page brief | Terms assigned to pages or draft briefs | CLUSTER_INTENT_CONFLICT, TARGET_ASSIGNMENT_MISSING, PROPOSED_URL_AS_EXISTING, CANNIBALIZATION_UNSUPPORTED; D+T page inventory; E intent/query-page data for factual diagnoses | Requiring a finished public page, live rank, public share link |
| Competitive landscape report | Cross-domain market-winner/gap analysis | COMPETITOR_TYPE_CONFUSED, PAGE_PATTERN_UNOBSERVED, estimate/scope, applicable rank/metric claims, REPORT_PROVENANCE_MISSING; D+T positioning+E query roster/results | Treating publishers as products; requiring local grids for a national market |
| Named competitor report | Deep analysis of one named competitor | PAGE_PATTERN_UNOBSERVED, appropriate rank/metric/scope rules, TARGET_INTENT_MISMATCH for recommended pages, local-pack rule only for local claims; D+T offer+E relevant data | Mandatory own-site comparisons when own domain unavailable |
| Local visibility report | A business/location/query Maps or local-pack analysis | LOCAL_ENTITY_MISMATCH, LOCAL_SCOPE_OVERCLAIM, LOCAL_ABSENCE_OVERCLAIM, LOCAL_PACK_FROM_ORGANIC; D+T location+E IDs/grid/result counts | Organic-rank convention as a substitute for local rank semantics |
| Link prospect plan/outreach | Prospect list, contact table, or citation outreach draft | CONTACT_FABRICATED, CONTACT_PROVENANCE_MISSING, OUTREACH_UNPERSONALIZED, PROSPECT_CONFLICT_HIDDEN; D+T asset/competitors+E pages/contact evidence | Sending messages, guessing contacts, mandatory paid-enrichment research |
| SEO audit report | A diagnostic report selecting actions for a site's organic opportunity | Applicable research-number/rank/temporal/causal rules, RECOMMENDATION_DIAGNOSIS_MISSING, SELECTION_RATIONALE_MISSING, WINNING_PAGE_REWRITE, REPORT_PROVENANCE_MISSING; D+T goal+E shortlist/live captures/calculations | Checking all site defects afresh, forcing unsupported recommendations |
| Setup/context record | A project setup status summary or actual trusted-context update | COMPLETION_STATUS_FALSE and CONTEXT_FACT_LOST; D+T before/after+W actual status | Mandatory public-page goal metrics, positioning fields, GSC integration |
| Coach reply | Explicit short OpenSEO tool/strategy guidance | Shared clarity/actionability/claim checks; source COACH_TOOL_CAPABILITY_FALSE when a capability is misstated; D+T tool capabilities | Enforcing coach bullet/question style on other artifacts |
| OpenSEO report HTML | Complete HTML expressly intended for OpenSEO save/viewer, independently of research type | Above semantic route plus opt-in exact viewer validators from REPORT_* candidates; full payload and save metadata required | Applying OpenSEO script/resource/title restrictions to general websites |

Use the per-skill inventory as an opt-in tail rather than expanding the always-on semantic core. In particular, default section titles, report typography, first-use teaching style, setup completeness, and platform transport rules should activate only when that artifact contract is explicit. For viewer constraints, split exact HTML checks by the individual REPORT_* predicates; never replace them with one Jev “report quality” score. A deterministic parser can supply evidence, while the required per-rule Jev/grading architecture remains intact.

## Cross-skill normalization and exclusions

Likely shared canonical checks include unsupported metric/claim, estimate-as-measured, missing material uncertainty, intent mismatch, business-fit mismatch, local-versus-national scope, false tool attribution, invented contact, missing provenance, and conversion/revenue fabrication. Keep distinct evidence predicates where the failure differs: failed SERP lookup is not checked-depth absence; checked-depth absence is not domain-sample omission; sparse grid coverage is not outranked coverage.

Useful direct page/brief candidates from this package are searcher-question coverage, sibling token substitution, pricing-versus-switching intent, keyword/cluster mapping, internal-link planning in briefs, audience/offer fit, and personalized outreach asks. The report-specific candidates apply only to reports; coaching candidates only to coaching; setup candidates only to context records/status summaries.

Excluded as ContentGuard page requirements: mandatory API calls, research batch sizes, paid-credit budgets, how many seeds/domains/grid points to query, 30-day paid-research reuse, automatic context writes, `save_keywords` confirmation, save/report sharing operations, folder creation, and app navigation instructions. These may inform separate workflow validators if the product later reviews tool execution. They do not establish a defect in ordinary changed copy.

Do not add arbitrary word counts, keyword density, minimum traffic, KD/CPC targets, fixed CTA counts, review-count targets, schema requirements, backlinks quotas, or ranking promises: these ten sources do not justify them. No evidence-dependent rule should silently call external services, send outreach, or convert missing source data into a failure.
