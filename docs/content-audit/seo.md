# ContentGuard research: SEO, AI discovery, commerce, and comparisons

> Historical source-audit record (2026-10-23). The candidate contracts and routing/evidence proposals below document the broader catalog design, not the current website runtime. In particular, the old Jev task-classifier and automatic evidence-discovery proposals are not active. Current behavior requires explicit trusted-base publications and bound evidence, deterministic supported artifact/rule selection, and mandatory exclusions. See [current review flow](../content-checks.md#review-flow) and [the publication API](../shared-ci-public-content.md).

Research date: 2026-10-23. This is a rule-design audit of source skills, not execution of their SEO workflows. No live-site audit, external fact verification, code change, test, remote write, or subagent work was performed.

## Coverage and architecture

Read all ten requested `SKILL.md` files in full after discovering their exact packages through all seven pages of `skills.list(authority=cloud)`. The ten mains expose 72 distinct package-relative reference paths. Every reference was requested with its complete URI and failed with `failed to read skill resource`; a representative alias retry also failed. No referenced checklist, rubric, template, or specialist procedure is represented here as having been read. No relevant packaged reference was found in the workspace. The inventory at the end identifies the missing material precisely.

This proposal records **202 granular source mappings**, consolidated into **172 canonical candidate checks and 30 alias rows** in 12 focused families. Only canonical checks should be implemented; aliases preserve the per-skill audit trail and route surface-specific cases to the canonical check. A candidate is available for selection; it is not a requirement that every page satisfy every rule. Several candidates require an explicit repository editorial policy, page contract, approved brief, or current evidence snapshot. No prerequisites means no finding.

The implementation contract is:

1. A deterministic content-presence gate runs first. Recognize changed public copy, editorial files, SEO metadata, structured data, and configured content-delivery controls. An unrelated refactor of a router or component is not automatically a content task.
2. Jev classifies eligible diffs. `p(content_task) >= 0.60` enters content review. A lower probability skips content checks.
3. Select each independent rule only when its applicability predicate and required evidence are satisfied. Jev evaluates **the probability of the particular evidenced defect**. `< 0.60` is ignored; `0.60 <= p < 0.80` warns; `p >= 0.80` fails. Probability is not business severity, estimated ranking impact, or a score for how closely a page follows a tactic.
4. Haiku receives only the matched focused rule/skill excerpts, the relevant changed lines, and the minimum trusted base context/evidence needed for that finding. Do not pass these ten entire source workflows to every finding.
5. A finding names the rule, changed line(s), concrete contradiction or omission, prerequisites/evidence, and a local repair. Do not turn missing research access into an inferred defect. Report an external check as untested outside the finding list when useful.
6. Deduplicate overlapping rules. For example, a wrong price shared by markup and visible copy can have two affected surfaces but one underlying catalog-fact defect. A broken link should not additionally fail five content-quality categories.

The current five broad design checks can remain report groups, but should not be the only independent judgments. Crawl controls, locale annotations, product offers, comparison claims, and page-format policies require their own narrow predicates and prompts.

## Evidence and context vocabulary

| Code | Required material |
|---|---|
| D | Changed content plus enough unchanged enclosing source to identify its meaning and affected surface. |
| T | Relevant approved context from the trusted base: product facts, author/proof registry, audience/intent, editorial policy, offers, dates, or page contract. Proposed changes cannot approve their own claims or weaken their own rules. |
| R | Complete effective page or template representation: resolved metadata, rendered DOM/text, generated-page snapshot, HTTP headers/status, or configuration interpretation. A partial text fetch cannot prove an absent element. |
| I | Trusted route/link/locale/product inventory, redirects, sitemap records, page-family membership, or generated records. |
| X | Dated external primary-source/crawl/measurement snapshot provided through a trusted process, with provenance, market, scope, and freshness suitable for the claim. The commit diff is not this evidence. |
| H | Comparable dated historical snapshots or a verified prior publication/update record. |

`D` rules may often be evaluated from the patch. `T/R/I/H/X` in a rule are required when their facts cannot be established by D alone. Production model output must cite which prerequisite was actually available. A flag can express a directly evidenced contradiction; it cannot invent the missing context. Optional renderer/crawl evidence should be generated in a separate job that does not expose review secrets to branch code.

Page types should be explicit when possible: editorial article, service, location, single marketing URL, PDP, PLP/category, comparison, documentation, utility, or programmatic record. Scope also needs locale/market, target publication state, intended discovery/indexation, format policy, canonical strategy, source freshness, and user exceptions. A page can have more than one type; resolve conflicting policies from trusted project instructions before evaluating it.

## Source-to-rule map

Each URI below was read completely. The specific section names identify the guidance used. Rule families also state their source keys. These are source mappings, not claims that every tactic in a skill is suitable as a blocking check.

| Key / exact SKILL.md URI | Guidance used | Candidate mappings |
|---|---|---|
| GROW — `skill://user/6ac4f4934c608191a85711765895945d/plan-seo-geo-growth/SKILL.md` | Delivery by page type; External links; Execute 1–7; Avoid common errors; concrete deliverable fields | PUB-01–18; ONP-01–18; LNK-01–12; TEC-01–23; AI-01–18; LOC-01–13; CMP-01–20; PLAN-01–14. For technical/local detail only the statements actually present in this main were used. |
| SHOP — `skill://user/6ac4f7c9b1c0819193568de0cda345e3/grow-ecommerce-seo-geo/SKILL.md` | Delivery by page type; External links; Execute relevant scope; Return a usable deliverable; Check common mistakes | PUB-01–18; ECOM-01–20; PSEO-01–14; AI-01–18; LOC-01–13; PLAN-01–14. Exact commerce checks refine the explicit catalog/raw/rendered/markup/feed/landing comparison requirement. |
| ONE — `skill://user/6ac51fd16b00819194f1b75ec1116c6d/rank-one-page-emd/SKILL.md` | Delivery by page type; External links; Execute 1–7; Avoid common mistakes | PUB-01–18; ONP-01–18; TEC-01–23; AI-01–18; LOC-01–13; PLAN-01–14. One-page and EMD-specific rows are ONP-15–18, LOC-08–11, PLAN-03–04. |
| AI — `skill://user/6ac92f6d05808191abb1d6c36eeb07cd/ai-seo/SKILL.md` | Extractability check; bot access; authority/sourcing; pricing data; agentic experiences; visibility measurement; what not to do | ONP-06–09; TEC-18–23; AI-01–18; SD-01–18 only where consistent with SCHEMA. Exact answer lengths, alleged uplift, file mandates, and platform assertions are excluded below. |
| AUDIT — `skill://user/6ac92f6d06c08191a0135dbb12324cda/seo-audit/SKILL.md` | Schema detection limitation; crawlability/indexation; international SEO; on-page SEO; local-business checks; evidence/fix findings | ONP-01–14; LNK-01–12; TEC-01–23; I18N-01–14; LOC-01–07; SD-01–18. Recommendations that overstate platform behavior are bounded below. |
| SCHEMA — `skill://user/6ac92f6d06b88191aa3b24acc3c35935/schema/SKILL.md` | Accuracy first; feature support versus vocabulary; values; content match; validation checklist | SD-01–18. Required properties and appearance eligibility must be selected from current documentation, not hardcoded from its shorthand table. |
| SCALE — `skill://user/6ac92f6d068c8191bbc7ba9b1573d221/programmatic-seo/SKILL.md` | Unique value; intent match; data sources/updates; conditional templates; linking; indexation; quality checklist | PSEO-01–14; ONP-01–14; LNK-01–12; TEC-01–17; SD-01–18. Subfolder preferences and assumed penalties are excluded. |
| ARCH — `skill://user/6ac92f6d06d08191bed2dcae98137742/site-architecture/SKILL.md` | Preserved URLs; navigation; URL consistency; breadcrumbs; internal-link audit | LNK-01–12; TEC-03–10; I18N-10; PSEO-07–08. Numeric layout/link heuristics are excluded. |
| COMPARE — `skill://user/6ac92f6d05d08191b3cf17811e21d4f5/competitors/SKILL.md` | Honesty; evidence discipline; page formats; decision criteria; pricing; migration; centralized data; claim audit | CMP-01–20; ONP-06–09; PLAN-11–12. Format elements are conditional on approved comparison format and available truthful evidence. |
| PROFILE — `skill://user/6ac92f6d05c481918ca71b0e9807e29e/competitor-profiling/SKILL.md` | Facts/inference/implication; not observed versus absent; snapshots/history; untrusted input; comparable metrics; raw sources | CMP-01–12, CMP-17–20; PLAN-01–02, PLAN-09–12. Raw data storage conventions are workflow preferences, not public-page defects. |

## PUB — declared editorial and publishing policy (18)

Focused pack: `editorial-page-policy`. Sources: GROW/SHOP/ONE, Delivery by page type and External links. **Every rule in this family requires T explicitly adopting this personal skill's policy**, with page type and any user exception resolved. These are user-specific publishing requirements, not universal SEO requirements. A shared layout/CMS can supply each field; do not demand duplication in the article file.

| ID | Concrete defect to evaluate | Applicability and evidence |
|---|---|---|
| PUB-01 | A published editorial article lacks its required named author. | Editorial publication; D+T+R or complete publication model. |
| PUB-02 | The article lacks its required brief author bio. | Editorial publication; D+T+R; linked bio satisfies policy if configured. |
| PUB-03 | An author credential, affiliation, or biography claim conflicts with the approved author record. | Changed author facts; D+T. Never invent a bio to satisfy PUB-02. |
| PUB-04 | The article omits its required relevant FAQ section. | Editorial publication; D+T+R. |
| PUB-05 | The article omits its required summary before the main body. | Editorial publication; D+T+R. |
| PUB-06 | The article omits its required Key Takeaways before the main body. | Editorial publication; D+T+R. |
| PUB-07 | An article lacks the required visible estimated reading time near the title/byline. | Editorial publication; D+T+R. Metadata alone is insufficient if policy says visible. |
| PUB-08 | The displayed reading time contradicts `ceil(final words / configured speed)`, minimum one minute. | Complete final reader text and trusted speed (200 wpm only when policy adopts fallback); D+T+R. Do not count navigation, JSON, or hidden editorial notes. |
| PUB-09 | An article lacks the required visible update date near the title/byline. | Editorial publication; D+T+R. |
| PUB-10 | The update date falsely implies a substantive update, uses an unsupported future date, or disagrees with verified publication/update history. | Date change; D+T+H. Never infer the actual last update from filesystem timestamps. |
| PUB-11 | Service/location copy includes an author byline prohibited by the adopted format. | Service/location page; D+T+R. |
| PUB-12 | Service/location copy includes an author biography prohibited by the adopted format. | Service/location page; D+T+R. |
| PUB-13 | Service/location copy adds a prohibited top summary or Key Takeaways section. | Service/location page; D+T+R; ordinary hero copy is not automatically a summary. |
| PUB-14 | Service/location publication omits its required relevant FAQ. | Service/location publication; D+T+R. |
| PUB-15 | Reader copy exposes editorial QA, SEO production notes, task instructions, or an editorial appendix that policy requires outside the article. | Editorial publication; D+T+R; user-requested notes/bibliography override. |
| PUB-16 | A bottom Sources/Primary source register is added despite an adopted inline-citation-only article format. | Editorial publication; D+T+R; explicit bibliography exception disables. |
| PUB-17 | A changed external HTML link omits the required new-tab target. | Actual external anchor; D+T+R; distinguish downloads, same-origin links, and CMS resolution. |
| PUB-18 | A required new-tab external anchor omits `noopener` or drops previously required `sponsored`, `ugc`, or `nofollow` values. | Actual external anchor; D+T+R; preserve existing disclosure/link policy. |

## ONP — query, title, metadata, and useful page content (18)

Focused pack: `seo-page-intent`. Sources: GROW Execute 3–5; ONE Execute 3–4 and Avoid common mistakes; AUDIT On-Page; AI Structure; COMPARE decision formats; SCALE intent/quality. Meaning and information needed by the intended reader take precedence over exact keyword strings.

| ID | Concrete defect to evaluate | Applicability and evidence |
|---|---|---|
| ONP-01 | The effective title is missing/empty after the change on a page contract requiring a public search title. | Public indexable page; D+R+T. A framework-generated title counts. |
| ONP-02 | The title makes a materially false promise about the page's actual topic, result, or offer. | Changed title or page scope; D+R, and T for product/offer facts. |
| ONP-03 | A changed title or description promises a price, availability, feature, or deal that the page/approved offer contradicts. | Search/social metadata; D+R+T. |
| ONP-04 | A metadata template introduces identical or unresolved titles/descriptions across distinct records that require unique meaning. | Shared template/generated family; D+I+R. Duplicate wording is a defect only where it hides actual distinctions. |
| ONP-05 | Search/social metadata contains exposed placeholders, markup fragments, stale variables, or a wrong entity/locale name. | Changed resolved metadata; D+R+T/I as needed. |
| ONP-06 | The content answers a different task, audience, product, or market from the approved primary intent. | Trusted brief/intent exists; D+T+R. No invented search intent. |
| ONP-07 | A changed answer to an explicit question omits its actual answer or contradicts it elsewhere on the page. | Q&A/definition/decision section; D+R. Does not mandate an FAQ or definition on every page. |
| ONP-08 | An answer block loses a necessary subject, condition, unit, or referent and now conveys a misleading standalone claim. | Evidently extractable answer/quote/block; D+R+T for factual condition. No universal 40–60 word rule. |
| ONP-09 | A comparison/procedure table or list omits a decision-critical condition supplied in trusted context, changing the meaning. | Table/list with known decision criteria; D+T+R. Tables and lists themselves are optional formats. |
| ONP-10 | A heading labels a materially different topic from the content it introduces. | Changed heading/body; D+R. |
| ONP-11 | The page's content-heading structure loses the required primary heading or introduces incoherent hierarchy that obscures section relationships. | Complete effective page; D+R+T when one-H1 policy is project-specific. Do not treat every multiple H1 or skipped number as an automatic SEO failure. |
| ONP-12 | Keyword/entity repetition visibly harms comprehension or creates a misleading place/service list without distinct information. | Changed prose/alt/headings; D+R. Identify exact repetition and reader effect, never use density quotas. |
| ONP-13 | A new title/H1/URL uses a different entity or primary task from its approved destination mapping. | Destination mapping is authoritative; D+T+I+R. Natural synonyms are allowed. |
| ONP-14 | The page removes information explicitly required to complete its stated task, leaving the reader unable to decide or act. | Known task contract; D+T+R; name missing fact/function rather than saying 'thin content.' |
| ONP-15 | A one-page brief maps separately indexable URL outcomes to fragment anchors and represents them as separate pages. | Declared one-URL project; D+T+I. |
| ONP-16 | A declared one-page change introduces extra marketing routes or presents an SPA's distinct routes as one URL. | One-page scope means one marketing URL; D+T+I. Legal/transaction routes follow agreed scope. |
| ONP-17 | One-page copy claims coverage of an excluded distinct intent without providing that service/task. | Trusted suitability decision and exclusions; D+T+R. |
| ONP-18 | An EMD/one-page claim guarantees ranking position, timeline, or uplift without its explicit valid evidence. | Changed claim; D+T/X. A domain's words do not establish guaranteed performance. |

## LNK — navigation, URLs, and internal links (12)

Focused pack: `seo-links-and-destinations`. Sources: ARCH URL/navigation/internal-link sections; AUDIT crawlability/internal linking; GROW URL preservation and links; SCALE hub/spoke and orphan prevention. Do not impose mandatory breadcrumbs, related posts, exact navigation counts, or link-density ratios universally.

| ID | Concrete defect to evaluate | Applicability and evidence |
|---|---|---|
| LNK-01 | A changed internal href resolves to a missing route/asset in the relevant build/locale. | Internal link; D+I/R. Absence from the patch is not absence from the site. |
| LNK-02 | A changed fragment link has no matching destination ID on the resolved page. | Fragment navigation; D+R. |
| LNK-03 | Link text materially misdescribes the destination or action. | Changed anchor/CTA; D+R+I or T. |
| LNK-04 | A standalone meaningful link loses an accessible descriptive name. | Content/navigation link; D+R; surrounding accessible context may satisfy it. |
| LNK-05 | Removing/replacing a route breaks existing known incoming links without a correct destination or redirect. | Route move/removal; D+I+T. Not every retired page needs a redirect. |
| LNK-06 | A redirect maps an old task/entity to an unrelated page despite a known equivalent destination. | Migration/redirect change; D+I+T. Homepage redirects are not equivalent by default. |
| LNK-07 | A published page becomes genuinely orphaned from the known crawlable site graph. | Complete graph/inventory; D+I+R. A small patch cannot establish orphan status. |
| LNK-08 | Navigation removes the agreed path to a critical page or function. | Approved nav/priority contract; D+T+I+R. Three clicks is a diagnostic heuristic, not a universal gate. |
| LNK-09 | Breadcrumb labels/targets represent the wrong hierarchy or link to nonexistent ancestors. | Breadcrumbs implemented; D+T+I+R. No demand that URL strings mirror taxonomy exactly. |
| LNK-10 | A configured hub/spoke family loses a required parent/child relationship and its discovery path. | Approved page-family contract; D+T+I+R. |
| LNK-11 | New URL generation violates the declared slash/case/locale pattern and yields duplicate or broken destinations. | Trusted URL policy; D+T+I+R. Do not demand migrations merely to remove dates, IDs, or parameters. |
| LNK-12 | A conversion/related-content link sends readers to the wrong product, market, locale, or intent destination. | Changed href/context; D+T+I+R. |

## TEC — content discovery and technical eligibility (23)

Focused pack: `seo-content-access`. Sources: AUDIT Technical SEO and detection limitations; GROW eligibility/URL preservation; ONE Execute 5 and bot distinctions; AI bot access/agentic experiences; SCALE crawl/index quality. Run only for changed content-delivery controls or affected publication records. These checks can be technical without interpreting arbitrary application code as public copy.

| ID | Concrete defect to evaluate | Applicability and evidence |
|---|---|---|
| TEC-01 | A changed indexation/publication control contradicts the explicit intended eligibility of the page or record class. | Intended indexation known; D+T+R (including headers and meta). Covers unintended noindex and unintended exposure of excluded records. |
| TEC-02 | Robots/CDN/WAF controls newly block a required discovery crawler from the affected public content. | Crawler purpose and discovery intent known; D+T+R/X. Not every bot must be allowed. |
| TEC-03 | The effective canonical points at an unrelated entity/task or the wrong approved preferred URL. | Canonical changed/resolved; D+T+I+R. |
| TEC-04 | Canonical generation emits an empty, malformed, unresolved, or contradictory canonical set. | Effective page metadata; D+R. A missing canonical is only a defect when required by a known duplicate/URL policy. |
| TEC-05 | The canonical target is confirmed unavailable, redirected incorrectly, blocked, or explicitly nonindexable against the chosen strategy. | Target evidence available; D+I+R/X+T. |
| TEC-06 | A redirect change introduces a loop or a broken terminal destination. | Changed route/redirect configuration; D+I+R. |
| TEC-07 | Publishing changes return an error/soft-error page for content expected to remain available. | Status and actual content verified; D+T+R/X. Soft 404 is an observed behavior, not a guessed penalty. |
| TEC-08 | Known permanently removed content is changed to a misleading successful empty page against the lifecycle policy. | Declared removal/status policy; D+T+R. |
| TEC-09 | Required secure/preferred origin is contradicted across links, canonical, redirects, or sitemap. | Trusted origin policy; D+T+I+R. |
| TEC-10 | A migration removes known equivalent legacy destinations without preserving agreed redirects and intent. | Explicit migration scope; D+T+I+R. |
| TEC-11 | A changed sitemap includes a URL known to be noncanonical, nonexistent, or intentionally nonindexable. | Sitemap and eligibility records; D+I+R+T. |
| TEC-12 | A changed sitemap record contains malformed locations, XML, namespaces, or unresolved variables that prevent use. | XML sitemap changed; D+R. Protocol conformance can be checked deterministically before model review. |
| TEC-13 | A publication required in the sitemap by the project contract is omitted by changed generation/filter logic. | Trusted sitemap publication policy and records; D+T+I+R. Sitemap inclusion does not guarantee indexing. |
| TEC-14 | A pagination/infinite-scroll change makes known deeper records inaccessible by the agreed crawlable discovery path. | Listing/page-family and deeper inventory; D+T+I+R. |
| TEC-15 | Parameter/facet/session generation introduces an unbounded or duplicate crawl space contrary to explicit URL/indexation rules. | Large-site/facet policy and generated examples; D+T+I+R. Do not infer crawl-budget harm from any parameter. |
| TEC-16 | A rendering change removes meaningful primary text or links from the representation required by the target reader/crawler. | Required consumer and actual representation verified; D+T+R/X. JavaScript usage alone is not a defect. |
| TEC-17 | A mobile publication change removes material facts/actions available on the intended desktop equivalent. | Comparable effective mobile/desktop representations; D+T+R. |
| TEC-18 | An audit states that schema is absent or broken based only on a method unable to detect the actual markup/type or validate its intended consumer. | Changed audit report; D plus recorded method and current consumer profile. Need rendered/equivalent complete evidence for an absence claim; Google-only tools do not cover every Schema.org type. |
| TEC-19 | A changed access claim confuses model-training permission with search-discovery inclusion. | Claim about bot controls; D+T/X with current documented roles. |
| TEC-20 | A configuration contradicts the approved separate search/training/user-retrieval policy by applying the wrong user-agent group. | Trusted per-purpose bot policy; D+T+R/X. |
| TEC-21 | An access report marks a platform check passed without performing the stated test or while the recorded result fails. | Audit/report artifact; D+T/R/X and test record. Missing access is 'untested.' |
| TEC-22 | A content-accessibility change leaves an essential interactive control without a usable accessible name/role. | Essential action on content/commerce page; D+R. Native controls can satisfy this without ARIA additions. |
| TEC-23 | A report asserts measured speed, Core Web Vitals, indexation, or crawl failure without appropriate measurement evidence. | Changed audit/performance claim; D+X/R. No diff-only speed inference or automatic live crawling. |

## I18N — multilingual and multiregional content (14)

Focused pack: `seo-locale-consistency`. Source: AUDIT International SEO & Localization; ARCH URL consistency. Treat AUDIT's unconditional statements about cross-locale canonicalization, `x-default`, prefixes, and ranking effects as overgeneralizations. Select the actual approved locale/indexing strategy before reviewing annotations. Regional duplicates can legitimately consolidate; `x-default` is not universally mandatory.

| ID | Concrete defect to evaluate | Applicability and evidence |
|---|---|---|
| I18N-01 | A changed hreflang code is invalid for the documented scheme or uses a confirmed invalid country/language combination. | Hreflang implemented; D+R+T/X for current code definitions. |
| I18N-02 | An intended reciprocal hreflang pair is one-sided in the complete published cluster. | Cluster complete and inclusion intended; D+I+R. |
| I18N-03 | A changed hreflang set omits the current canonical member where the chosen cluster requires self-reference. | Intended cluster and canonical identity known; D+I+R+T. |
| I18N-04 | A language-region code maps to two different destinations within one effective alternate set. | Same alternate set; D+I+R; distinguish alternate placement duplicates that agree. |
| I18N-05 | A changed alternate points to a confirmed nonexistent, ineligible, or wrong-language destination. | Complete target evidence; D+I+R/X+T. |
| I18N-06 | HTML/header/sitemap alternate declarations materially contradict each other. | Multiple mechanisms actually used; D+I+R. |
| I18N-07 | A canonical change contradicts the explicit intention to index a distinct locale independently. | Trusted locale strategy; D+T+I+R. Cross-locale canonicalization alone is not always wrong. |
| I18N-08 | A paginated locale URL is canonicalized to a different page despite having distinct required inventory and an independent-page policy. | Pagination and index policy; D+T+I+R. |
| I18N-09 | Sitemap alternate markup is malformed or lacks required namespace/absolute destinations for the implemented format. | XML alternates implemented; D+R+I. |
| I18N-10 | Locale URL generation disagrees with the declared path/domain/case/slash policy and produces the wrong destination. | Known locale strategy; D+T+I+R. Subdomains, ccTLDs, and unprefixed defaults are not defects by themselves. |
| I18N-11 | Mandatory IP/language redirection makes an intended locale inaccessible to its required discovery consumer. | Effective request behavior; D+T+R/X. No assumption that every content negotiation is broken. |
| I18N-12 | A locale page claims translation/localization while its material body or offer remains in the wrong language. | Target locale and complete page; D+T+R. Shared brand names/code/quotes are allowed. |
| I18N-13 | Localized price/currency/contact/address units contradict the approved market data. | Market facts exist; D+T+R. |
| I18N-14 | A configured `x-default` or locale-selector fallback points to an unavailable or wrong approved destination. | Fallback actually required/implemented; D+T+I+R. Absence alone is not a universal defect. |

## SD — structured data truth and syntax (18)

Focused pack: `structured-data-integrity`. Sources: SCHEMA Core Principles, Feature Support, Values, Validation; AUDIT detection limitations; SHOP consistency across catalog/markup; AI schema only as optional semantics. Evaluate actual consumer requirements from a versioned trusted schema profile or dated current specification. A valid Schema.org type is not proof of a Google search feature. Do not require schema universally or promote recommended fields to required fields.

| ID | Concrete defect to evaluate | Applicability and evidence |
|---|---|---|
| SD-01 | Changed JSON-LD is invalid JSON or cannot be serialized as intended. | Structured-data source; D+R. No comments/trailing commas in actual JSON. |
| SD-02 | Type/context/property syntax contradicts the chosen documented vocabulary or consumer profile. | Schema profile available; D+T/X+R. Unknown custom fields need contextual review, not reflexive rejection. |
| SD-03 | A property required by the identified current consumer/type is absent. | Explicit type+consumer+current profile; D+T/X+R. Ignore generic shorthand required-field tables. |
| SD-04 | A changed date, URL, enumeration, number, or currency has an invalid format/value under the selected profile. | Property value; D+T/X+R. |
| SD-05 | Structured data describes a different page/entity/product from the actual visible destination. | Effective page and graph; D+R+T. |
| SD-06 | Markup asserts facts not actually present in required visible content or otherwise violates its current consumer's content-match requirement. | Consumer content-match rule established; D+T/X+R. Some identity metadata can legitimately exceed prose. |
| SD-07 | A structured price, currency, stock state, or variant contradicts the approved offer/page. | Product/offer data; D+T+R. |
| SD-08 | A rating/review/award is invented, attributed to the wrong entity, or contradicted by the trusted proof record. | Claimed proof in markup; D+T+R. Do not infer fake reviews merely from missing repository evidence. |
| SD-09 | Review/rating markup is used for an explicitly ineligible target or consumer context. | Current eligibility rule and actual entity relationship; D+T/X+R. |
| SD-10 | Article author, publisher, or affiliation contradicts approved identity records. | Article markup; D+T+R. |
| SD-11 | `datePublished` or `dateModified` contradicts known history or falsely represents a refresh. | D+T+H+R. |
| SD-12 | Graph `@id`/reference reuse merges unrelated entities or leaves a required graph relationship unresolved. | Complete graph and identity map; D+T+R. |
| SD-13 | Breadcrumb structured data disagrees with the actual agreed page hierarchy/destinations. | Breadcrumb markup and route map; D+T+I+R. |
| SD-14 | FAQ/HowTo markup materially contradicts the visible questions/answers/steps it purports to encode. | Such semantic markup present; D+R. Presence is optional. |
| SD-15 | Duplicate markup generators emit mutually inconsistent material facts for the same entity. | Complete effective markup, including injected blocks; D+T+R. Multiple valid blocks alone are allowed. |
| SD-16 | A comparison/list/offer schema emits unresolved record variables, stale entity labels, or another record's data. | Template output and records; D+I+R+T. |
| SD-17 | A recommendation promises a Google appearance from a schema feature whose current support has been confirmed retired or unavailable. | Changed implementation plan/public claim; D+T/X. The skill names FAQ/HowTo/SearchAction examples; verify current support before hardcoding. |
| SD-18 | An audit calls semantic markup broken solely because a Google-only tool/report does not support that type. | Report artifact and actual validation method; D+T/X+R. Use vocabulary versus consumer distinction. |

## AI — AI discovery, evidence, and reporting (18)

Focused pack: `ai-discovery-evidence`. Sources: AI access/patterns/pricing/measurement/what-not-to-do; GROW measurement and facts limits; ONE no guarantees and separate metrics; SHOP product-choice/offer/citation/business distinctions. Never claim that a missing `llms.txt`, OKF bundle, answer length, statistic, FAQ schema, listicle, or third-party mention is an established cause of lost AI visibility.

| ID | Concrete defect to evaluate | Applicability and evidence |
|---|---|---|
| AI-01 | A public product/positioning statement contradicts the approved primary identity, audience, or capability. | Changed factual identity; D+T+R. External model hallucination is not necessary evidence. |
| AI-02 | A maintained machine-readable knowledge/pricing file contradicts the approved public product/offer. | File actually exists or is required; D+T+R. Do not require creation of such files universally. |
| AI-03 | Structured pricing omits/changes units, billing interval, seat basis, or limits so that its amount is materially misleading. | Pricing file/page; D+T+R. Custom pricing is permitted and should be described honestly. |
| AI-04 | A generated knowledge bundle mislabels source origin, entity, locale, or last-updated facts. | Bundle implemented; D+T+I+R/H. Optional format does not excuse false data. |
| AI-05 | A claim says training-bot access is required for search citations without current supporting platform evidence. | Changed advice/claim; D+T/X. Prefer explicit known policy contradiction over absence-of-proof speculation. |
| AI-06 | A claim presents a tactic/format as a confirmed ranking, citation, or eligibility requirement, or promises a supported appearance, when current trusted platform evidence contradicts that status. | Changed advice; D+T/X establishing current status. Covers experimental agent protocols and retired structured-data appearances. |
| AI-07 | An AI-visibility result equates retrieved material with a citation, brand mention, or recommendation that the recorded answer lacks. | Captured answer and labels; D+X/R. |
| AI-08 | A cited source is reported as an endorsed merchant/product despite no recommendation in the captured response. | Captured answer and product/merchant labels; D+X/R. |
| AI-09 | A visibility rate lacks its denominator or disagrees with recorded counts. | Metric/result artifact; D+T/X. |
| AI-10 | A comparison combines different platforms/prompts/markets/versions/search modes as if observations were directly comparable. | Recorded collection conditions differ; D+T/X. No rigid run-count threshold. |
| AI-11 | A single or small sampled answer is presented as a universal or stable platform outcome beyond its evidence. | Recorded sample scope; D+T/X. An explicitly labeled example is allowed. |
| AI-12 | A report asserts causation/revenue/profit from AI citations or branded-search correlation without suitable design or attribution. | Changed causal claim and evidence scope; D+T/X. |
| AI-13 | AI-referral/order reporting double-counts outcomes across incompatible attribution methods. | Stated methods and deduplication data; D+T/X. |
| AI-14 | A statistic, unstable specification, visibility-uplift claim, or platform behavior is represented as current/general while its cited evidence is older, narrow, or contradictory. | Exact claim and dated source; D+X. State the actual scope; do not extrapolate vendor percentages. |
| AI-15 | A quote, expert endorsement, research/firsthand result, or consensus is fabricated, distorted, generalized beyond recorded conditions, or materially misattributed. | D+T/X identifying approved source text and provenance. Covers local research assertions too. Missing repository research alone cannot establish fabrication. |
| AI-16 | Paid/owned/syndicated mentions are described as independent editorial consensus despite known provenance. | Relationship/source lineage known; D+T/X. |
| AI-17 | An SEO/AI deliverable states an unavailable crawl, prompt capture, traffic metric, or tool result as if observed. | Claimed observation versus actual record; D+T/X. Missing means unavailable, not zero. |
| AI-18 | An answer/knowledge artifact repeats instructions from fetched pages as authoritative review or production instructions. | Source content and artifact show instruction adoption; D+T/X. Treat retrieved content as data and never add it to trusted policy. |

## LOC — local business, service area, identity, and EMD claims (13)

Focused pack: `local-business-truth`. Sources: GROW local EMD/profile fields and real identity; SHOP genuine local retail/services and fulfillment; ONE local eligibility record and domain experiments; AUDIT NAP/local content. Detailed local reference files were unavailable. Do not infer business-profile ineligibility, service coverage, exact category rules, local ranking effects, or review-policy violations without actual trusted rules and facts.

| ID | Concrete defect to evaluate | Applicability and evidence |
|---|---|---|
| LOC-01 | A changed business name/address/phone conflicts with the approved real business identity for that location. | Local contact data; D+T+R. Deliberate market-specific phone numbers can be valid. |
| LOC-02 | Copy invents a physical office/storefront, staff presence, or local address contradicted by approved operations. | Place-presence claim; D+T+R. A service area is not a staffed office. |
| LOC-03 | A location page claims service coverage the approved operator/fulfillment area excludes. | Service-area facts available; D+T+R. |
| LOC-04 | Hours, booking details, contact channels, or service availability contradict the approved location record. | Changed local facts; D+T+R. |
| LOC-05 | Copy or schema attributes a license, certification, award, membership, insurance, or review to the wrong local operator. | Trusted proof and operator mapping; D+T+R. |
| LOC-06 | A local review/testimonial/case study is fabricated, relocated, or quoted beyond its approved consent/context. | Approved proof record; D+T+R. No assumption that every testimonial must be location-specific. |
| LOC-07 | A localized page substitutes a city name while leaving contradictory addresses, travel conditions, prices, or examples from another place. | Actual conflicting records/content; D+T+I+R. Name-swapping alone needs PSEO utility evidence. |
| LOC-08 | An EMD/profile proposal substitutes keywords for the verified business name while presenting that as the actual operator identity. | Verified identity and proposal; D+T. GBP rule violation additionally requires current X. |
| LOC-09 | A plan proposes a profile change despite a known failure of its actual required business eligibility/verification conditions. | Trusted eligibility record + current rule; D+T+X. No guessed eligibility. |
| LOC-10 | A plan describes changing one profile's website URL as a complete main-site migration or the reverse, omitting required scope consequences. | Trusted intended scope and affected URLs; D+T+I. |
| LOC-11 | An EMD claim asserts automatic ranking advantage, domain value uplift, or guaranteed local outcomes beyond supplied evidence. | Claim/forecast; D+T/X. Domain choice is a business decision. |
| LOC-12 | A local experiment/readout attributes outcomes to a URL/profile change while its own evidence contains unresolved geography, scope, or baseline differences. | Experimental claim and dated records; D+T+X. |
| LOC-13 | A local-content research claim invents place-specific facts/interviews/photos/results that contradict or exceed its approved source record. | Original local research represented as observed; D+T/X. General city knowledge is not proof of firsthand work. |

## ECOM — product, offer, assortment, and shopping consistency (20)

Focused pack: `commerce-content-integrity`. Source: SHOP Execute 1–7, exact variant comparisons, usable deliverables, and common mistakes; AUDIT ecommerce checks. These rules unpack the explicit SKU/catalog/raw/rendered/markup/feed/landing comparison into independent defects. Require authoritative catalog/offer context and actual affected records. Do not infer merchant-center or AI-shopping eligibility from generic SEO rules.

| ID | Concrete defect to evaluate | Applicability and evidence |
|---|---|---|
| ECOM-01 | Product copy names the wrong SKU/model/brand/variant for its destination. | PDP/record identity; D+T+I+R. |
| ECOM-02 | A price or currency contradicts the approved current offer for that market/variant. | Offer facts; D+T+R; stale external snapshots cannot establish current truth. |
| ECOM-03 | Copy claims in-stock/immediate availability when authoritative inventory says otherwise. | Inventory state/freshness known; D+T+R. |
| ECOM-04 | Size, dimensions, quantity, material, capacity, or unit facts contradict the exact SKU record. | Product attributes; D+T+R. |
| ECOM-05 | Compatibility/fit/safety/suitability claim exceeds the approved product evidence or omits a known material limitation. | Exact supported use and limits; D+T+R. |
| ECOM-06 | Delivery, region, lead time, shipping cost, or pickup promise contradicts approved fulfillment terms. | Market/offer and fulfillment; D+T+R. |
| ECOM-07 | Return, warranty, cancellation, or guarantee terms contradict approved policy for the product/market. | Policy and exceptions known; D+T+R. |
| ECOM-08 | A product demonstration/test/original result is presented as performed despite the trusted record identifying it as hypothetical or nonexistent. | Evidence registry; D+T/X+R. An honestly labeled demo is allowed. |
| ECOM-09 | Product reviews, counts, ratings, or endorsements are assigned to an unsupported product/variant or misstate the known data. | Approved proof with variant scope; D+T+R. |
| ECOM-10 | Visible page, JSON-LD, product feed, and maintained knowledge file disagree on a material fact for the same exact offer. | At least two comparable effective surfaces, same market/time/variant; D+T+R/I. Deduplicate underlying price/stock error. |
| ECOM-11 | A feed/entry selects a landing variant different from the represented product/offer without disclosing the selection. | Feed record, landing selection, variant map; D+T+I+R. |
| ECOM-12 | Variant URLs/canonicals/identifiers merge distinct offers or split equivalents contrary to the approved platform/catalog strategy. | Trusted variant strategy and records; D+T+I+R. No universal variant URL rule. |
| ECOM-13 | A category/PLP promises an assortment its actual filters/inventory do not provide. | Listing promise versus matched records; D+T+I+R. |
| ECOM-14 | A shopping filter/attribute label contradicts the actual product selection, making the comparison materially wrong. | Filter logic/output and verified attributes; D+T+I+R. |
| ECOM-15 | A category/facet page is made indexable despite violating its explicit utility/assortment publication criteria. | Criteria and inventory counts/attributes exist; D+T+I+R. No arbitrary minimum products. |
| ECOM-16 | Stock-lifecycle edits remove/redirect a product contrary to its approved temporary/permanent state and equivalent-destination policy. | Lifecycle/URL policy; D+T+I+R. Do not prescribe universal 404/noindex/redirect behavior. |
| ECOM-17 | Pagination/facet changes hide known purchasable deeper inventory from the required discovery path. | Inventory + discovery contract; D+T+I+R. Deduplicate TEC-14. |
| ECOM-18 | Buying guidance recommends a product contradicted by its own stated selection criteria or trusted compatibility/availability limits. | Guide criteria and verified product data; D+T+R. |
| ECOM-19 | Product comparison ranks offers using noncomparable units, packs, markets, tax/shipping assumptions, or price periods without disclosure. | Comparable records and chosen assumptions; D+T+R/X. |
| ECOM-20 | Commerce results equate product inclusion, merchant-offer order, brand mention, citation, visit, order, revenue, or profit despite distinct evidence. | Report and definitions/counts; D+T/X. Deduplicate AI-07–13 where same result. |

## PSEO — generated-page utility and data quality (14)

Focused pack: `programmatic-content-quality`. Sources: SCALE unique value, conditional content, data requirements, crawl/quality checklists; SHOP useful assortment and destination decisions; GROW one intent/page and no wording-variant explosion. Public data and templating are allowed. The relevant question is the actual user task and record evidence, not whether text was AI-generated or shares a template.

| ID | Concrete defect to evaluate | Applicability and evidence |
|---|---|---|
| PSEO-01 | Generated public content exposes missing/null/undefined fields, unresolved tokens, or nonsensical fallbacks. | Generated sample with source record; D+I+R. |
| PSEO-02 | A template places another entity/location/product's facts into the current record. | Record identity and authoritative values; D+T+I+R. |
| PSEO-03 | A page claims record-specific information while all meaningful facts belong to a different/general record and the promised task is unsatisfied. | Complete sample, data and task contract; D+T+I+R. Mere textual similarity is insufficient. |
| PSEO-04 | Publishing logic creates pages with no usable required data under the project's explicit utility criteria. | Required fields/utility contract and generated records; D+T+I+R. |
| PSEO-05 | The template omits required conditional caveats/sections when the record data makes them necessary. | Conditional requirements and record values; D+T+I+R. |
| PSEO-06 | A generated claim uses stale, incorrect, unlicensed-for-this-use, or unverified data contrary to an explicit trusted source contract. | Versioned data/source contract and discrepancy; D+T+I/X. Do not assume all scraped/public data is unusable. |
| PSEO-07 | New records have no required crawlable hub/category/related-page path. | Complete family inventory and linking contract; D+T+I+R. Deduplicate LNK-07/10. |
| PSEO-08 | Generated related links or breadcrumbs point to wrong/nonexistent entities or parents. | Family mapping and output; D+I+R. |
| PSEO-09 | Generated records produce indistinguishable metadata for distinct promised tasks because identity/intent variables are missing or wrong. | Family metadata outputs; D+T+I+R. Deduplicate ONP-04. |
| PSEO-10 | Page-generation logic creates separate URLs for identical intent/records despite an explicit merge/canonical ownership decision. | Approved ownership map; D+T+I+R. Similar queries alone do not prove cannibalization. |
| PSEO-11 | Indexation/publication controls contradict the approved page-class policy or known record eligibility. | Class/record policy; D+T+I+R. |
| PSEO-12 | A generated location/integration/persona page claims actual service, integration, or suitability contradicted by product/operations data. | Capabilities and record mapping; D+T+I+R. |
| PSEO-13 | A template's conversion CTA promises a different task or product than the record can fulfill. | Record intent and destination; D+T+I+R. |
| PSEO-14 | A launch/report asserts reviewed quality for the full generated set despite evidence covering only a stated sample and known unresolved failures. | Actual review/sample log; D+T/I/X. Sampling is allowed when labeled accurately. |

## CMP — competitor profiles and buyer comparisons (20)

Focused pack: `comparison-claim-integrity`. Sources: COMPARE Evidence Discipline, formats, pricing, migration, claim audit; PROFILE facts/snapshots/untrusted input/metrics. This family applies to public comparisons and any committed profile, deck, or internal asset making the same claims. A lack of public documentation is not evidence of product absence.

| ID | Concrete defect to evaluate | Applicability and evidence |
|---|---|---|
| CMP-01 | A competitor capability/pricing claim contradicts a current authoritative source snapshot or trusted centralized fact for the same plan/market/edition/time. | Source and check date available; D+X/T. Covers a fact assigned to the wrong plan, region, or version and inconsistent repetitions. |
| CMP-02 | A checkmark/cross/'not available' claim treats 'not observed on checked pages' as confirmed absence. | Research record only establishes non-observation; D+T/X. Absence needs docs/trial evidence adequate for that claim. |
| CMP-03 | Pricing hides billing interval, per-seat/usage basis, minimum commitment, currency, tier, or material limits in a way that changes its meaning or comparison. | Current applicable offer facts; D+T/X. Applies to ordinary public pricing and machine-readable pricing as well as competitor tables. |
| CMP-04 | A sample-team/total-cost calculation disagrees with verified tiers, limits, or its own stated assumptions. | Inputs and arithmetic; D+T/X. |
| CMP-05 | A feature limit/paywall is assigned to the wrong plan, region, edition, or time. | Exact scoped source; D+T/X. |
| CMP-06 | A pricing/feature table represented as verified current omits its required as-of/check date. | Comparison format requires date; D+T+R. A 'current' label needs actual verification, not today's date alone. |
| CMP-07 | A claim of unchanged pricing/features/history is based only on a single snapshot. | Research provenance shows one snapshot; D+T/X/H. |
| CMP-08 | Copy assigns a competitor's motive without an attributed public statement establishing it. | Claim and research record; D+T/X. Explain observed change without inferred motive. |
| CMP-09 | Analyst inference or implication is presented as an observed competitor fact. | Source record differentiates layers; D+T/X. |
| CMP-10 | A strength/weakness/superiority claim contradicts the approved product evidence or hides a known material limitation. | Comparable criteria and proof; D+T/X. Criticism and favorable positioning are allowed when accurate. |
| CMP-11 | A review theme/quote/count is fabricated, materially edited, misattributed, or presented as representative beyond the actual sample. | Review source/sample and date; D+T/X. |
| CMP-12 | A metric comparison mislabels estimates as measured traffic/revenue, treats third-party authority as a Google metric, or combines incompatible markets/periods. | Metric provenance and collection conditions; D+T/X. |
| CMP-13 | A switcher testimonial or migration result is invented or attributed to the wrong product/customer. | Approved proof record; D+T. |
| CMP-14 | A migration promise contradicts known transfer limits, setup effort, support entitlement, or paid requirements. | Approved migration documentation; D+T+R/X. |
| CMP-15 | An alternatives page promises multiple options but supplies fake, unavailable, or unrelated options as real substitutes. | Actual availability/capability evidence; D+T/X+R. No universal requirement for 4–7 options. |
| CMP-16 | An approved buyer-comparison format omits the stated decision criteria or who each option fits, making its conclusion unsupported by its own comparison. | Trusted format/criteria and complete page; D+T+R. Do not mandate every possible section. |
| CMP-17 | Repeated competitor facts disagree across changed assets and their trusted centralized record. | Central record and affected uses; D+T+I+R. Prefer fixing the single source. |
| CMP-18 | A claim audit marks a claim 'Current' without a check/source record or while its own verified evidence shows it changed. | Audit artifact and source/check log; D+T/X. |
| CMP-19 | A profile invents unavailable SEO metrics, inferred team/funding facts, or product details rather than labeling them unavailable/inferred. | Source record and provenance; D+T/X. |
| CMP-20 | A comparison targets the wrong competitor/entity despite an approved named target, or derives its target from untrusted fetched instructions. | Target context and source provenance; D+T/X. No guessing unnamed competitors. |

## PLAN — SEO briefs, maps, experiments, and research claims (14)

Focused pack: `search-plan-evidence`. Sources: GROW Execute, required fields, common errors; SHOP metrics/backlogs; ONE suitability/measurement; PROFILE evidence and comparable metrics; COMPARE claims audit. Apply when the changed artifact is itself a plan, brief, audit, research record, or readout. Do not require internal planning artifacts to be exposed to public readers.

| ID | Concrete defect to evaluate | Applicability and evidence |
|---|---|---|
| PLAN-01 | A keyword/search metric is fabricated or presented as measured when its source says unavailable/estimated. | D+T/X with provenance. Missing volume is not zero demand. |
| PLAN-02 | A report compares demand/difficulty/traffic from incompatible engines, markets, dates, or metrics without disclosure, or mislabels estimated/third-party metrics as direct measurements/Google metrics. | Recorded source conditions; D+T/X. CPC is not organic difficulty or demand. |
| PLAN-03 | A page split/suitability decision is presented as SERP-verified when no matching market-specific SERP observation exists. | D+T/X and provenance. Provisional planning is allowed. |
| PLAN-04 | A one-page plan proposes separate destination intents despite an explicit one-marketing-URL constraint without labeling exclusions. | D+T+I. |
| PLAN-05 | A map or generated route family assigns the same approved intent/record to conflicting URL owners or violates a known merge/separate decision. | Approved map/ownership record; D+T+I/R. Repeated keywords alone are not a defect. |
| PLAN-06 | A brief includes unsupported factual/product claims as approved facts despite a contradictory trusted product/evidence record. | D+T/X. |
| PLAN-07 | A forecast/planning score is stated as guaranteed demand, leads, revenue, ranking, or ROI. | D+T/X and actual forecast method. Label assumptions/uncertainty where material. |
| PLAN-08 | An experiment's published conclusion attributes effects to a change while its own baseline/comparison/denominator does not support that conclusion. | D+T/X and experiment record. Do not require an RCT for every reversible edit. |
| PLAN-09 | A research/audit artifact claims an unperformed inspection, tool call, transcript/claim check, or review beyond the recorded scope. | Claimed method/status versus actual provenance; D+T/X. Covers a false 'Current' claim status and a sample presented as a complete review. |
| PLAN-10 | A recommendation relies on a materially outdated unstable specification while presenting it as current. | D+X and dates/version evidence. Old foundational work is permitted when dated and scoped. |
| PLAN-11 | A source quotation/research finding is misattributed, materially distorted, or generalized beyond its recorded study conditions. | Exact source evidence; D+T/X. |
| PLAN-12 | A plan counts syndicated copies/paid placements/owned reviews as independent corroboration despite known lineage. | D+T/X. |
| PLAN-13 | A release/backlog says an unresolved required access/content check has passed, or omits a known blocking dependency while representing work as ready. | Required acceptance contract and status evidence; D+T/I/R/X. Missing optional checks are not failures. |
| PLAN-14 | An outcome readout conflates product inclusion, merchant-offer order, brand mention, qualified leads, signups, activation, visits, citations, orders, revenue/profit, or self-attribution as equivalent results. | Definitions and recorded metrics; D+T/X. |

## Canonical consolidation: 30 aliases, 172 implementable checks

The 202 rows above preserve the specific guidance and surfaces found during the source audit. The following 30 rows are **aliases, not additional independent checks**. Do not dispatch them to Jev separately. Route them to the named canonical ID using the narrower surface/context in the original row. A mapping to several IDs selects the actual contradicted field or failure; it does not automatically emit several findings.

| Alias row | Canonical check(s) | Reason |
|---|---|---|
| AI-03 | CMP-03 | Pricing units/terms are the same defect on ordinary, competitor, and machine-readable surfaces. |
| AI-08 | AI-07 | A citation mislabeled as a recommendation is a visibility-stage misclassification. |
| AI-17 | PLAN-09 | An invented AI observation is an unperformed research claim. |
| CMP-05 | CMP-01 | Wrong plan/region/time is an incorrectly scoped competitor fact. |
| CMP-12 | PLAN-02 | Competitor metric provenance is the general metric-comparability check. |
| CMP-17 | CMP-01 | Centralized fact contradictions have one owner regardless of repetition. |
| CMP-18 | PLAN-09 | A false checked/current status misrepresents the performed research. |
| CMP-20 | ONP-06 or AI-18 | Wrong approved entity is intent mismatch; adopted fetched instructions are untrusted-instruction contamination. |
| ECOM-10 | ECOM-01–09 | Surface disagreement should use the specific product fact that is wrong. |
| ECOM-17 | TEC-14 | Hidden deeper inventory is the same broken discovery path. |
| ECOM-20 | PLAN-14 | Commerce outcome labels require the same metric separation. |
| LOC-11 | ONP-18 | EMD performance guarantees are the same claim regardless of local context. |
| LOC-12 | PLAN-08 | Local experiments require the same baseline/comparison inference. |
| LOC-13 | AI-15 | Fabricated or distorted local research is a research-evidence defect. |
| PLAN-10 | AI-14 | Unstable specifications and platform claims share freshness/scope evidence. |
| PLAN-11 | AI-15 | Misquoted or generalized research is one attribution defect. |
| PLAN-12 | AI-16 | False independent consensus is one provenance defect. |
| PSEO-07 | LNK-07 or LNK-10 | Generated pages use the same orphan/required-family-link checks. |
| PSEO-08 | LNK-01 or LNK-09 | Generated related links and breadcrumbs use ordinary destination checks. |
| PSEO-09 | ONP-04 | Generated duplicate metadata is the same record-resolution defect. |
| PSEO-10 | PLAN-05 | Generated routes must obey the same approved ownership decision. |
| PSEO-11 | TEC-01 | Record-class eligibility is the intended-indexation check. |
| PSEO-13 | LNK-12 | A generated CTA still points to an intent destination. |
| PSEO-14 | PLAN-09 | Claiming full review from a sample overstates research scope. |
| SD-07 | ECOM-01, ECOM-02, or ECOM-03 | Markup offer truth is the specific product/price/stock fact. |
| SD-13 | LNK-09 | Structured breadcrumbs describe the same hierarchy. |
| SD-14 | SD-06 | FAQ/HowTo mismatch is schema-to-content mismatch. |
| SD-16 | PSEO-01 or PSEO-02 | Markup templates can have the same unresolved/wrong-record data defect. |
| SD-17 | AI-06 | A retired-feature promise is a contradicted format-support claim. |
| SD-18 | TEC-18 | An unsuitable validation method cannot establish broken markup. |

For remaining overlaps, use one finding per **canonical rule + affected entity/record + independent field/failure + source contradiction**. Multiple changed surfaces are evidence/locations on that finding. For example, one wrong approved price rendered in a title, body, and JSON-LD is ECOM-02 once, rather than ONP-03 + SD-07 + ECOM-02. Two unrelated wrong facts can still receive separate probabilities. A factual mismatch should win over a generic 'intent/quality' finding for the same text. Static aliasing is intentionally limited where two rules require meaningfully different proof (for example wrong price versus misleading omission of price terms).

## Selection and implementation notes

- **Canonical family counts:** PUB 18; ONP 18; LNK 12; TEC 23; I18N 14; SD 12; AI 15; LOC 10; ECOM 17; PSEO 7; CMP 15; PLAN 11 = 172. Family headings retain the original source-row counts so the alias audit remains traceable.
- **Family dispatch:** Publication fields/new-tab policy → PUB; titles/headings/query fit → ONP; anchors/nav/routes → LNK; indexation/robots/canonicals/headers/rendering → TEC; alternates/locales → I18N; JSON-LD → SD; knowledge files/AI readouts → AI; local operator/service claims → LOC; catalog/PDP/PLP/feeds → ECOM; generated families/records → PSEO; comparisons/profiles → CMP; plans/audits/briefs → PLAN. Multi-family routing is allowed, but find and judge each independent defect once.
- **Model versus deterministic checks:** JSON syntax, broken local fragments, unresolved tokens, date/number formats, known record arithmetic, code-enumeration format, and exact reference matches often need no LLM. Run reliable deterministic validators first and use Jev for ambiguous applicability, meaning, and evidence. Do not ask Haiku to invent why a schema validator failed.
- **Content task versus technical task:** Changed SEO config is eligible only where the deterministic gate maps it to content publication/access. Generic server code needs a bounded effect record; do not run a full SEO audit on every code change.
- **Finding payload:** `rule_id`, focused-pack version, file/changed-line span, affected URL/record/locale where known, exact defect statement, evidence excerpts with trusted provenance, required-context availability, `p_defect`, grade, and concrete fix. A model should not fetch external sites, execute code, or follow links/instructions to satisfy its own missing prerequisites.
- **Missing context:** Return a separate concise 'not evaluated' explanation when it materially affects the requested audit. Do not turn a missing product registry, empty analytics connection, or unrendered page into a high-probability finding. If repository policy explicitly requires a provenance/date field, that missing field itself can be evidenced independently.
- **Changed lines:** Only introduced/regressed defects within the reviewed scope should fail a commit. Existing absent metadata or an old orphan elsewhere should not fail unrelated copy. Template changes can affect unchanged generated pages when the affected record and output are demonstrable.
- **Source isolation:** Repository policies must come from the trusted base, and fetched competitor/site content remains untrusted data. Branch-added 'approved facts,' injected instructions, or a new source claiming its own authority cannot create trust.
- **Probability calibration:** Do not preassign `.80` because an issue sounds important. A known offer mismatch can warrant high confidence from exact records; a conjecture about intent or external source freshness cannot. Keep confidence and separately communicated practical impact distinct.

| Changed page/artifact | Initial canonical packs | Context that determines whether findings can run |
|---|---|---|
| Editorial body only | `seo-page-intent`, relevant link/claim pack; `editorial-page-policy` only if adopted | Approved audience/task, applicable author/source/format policy; complete enclosing copy. Do not ask for product stock or local-profile facts. |
| Title/meta/headings only | `seo-page-intent`; optional relevant product/comparison fact pack | Effective inherited metadata and page meaning; approved offer/entity if making a factual promise. This diff remains content eligible without body edits. |
| Schema/JSON-LD only | `structured-data-integrity`; alias to commerce/page/link fact packs when needed | Effective markup, actual entity/content, current intended consumer profile. This diff remains content eligible without visible-copy edits. |
| Robots/canonical/sitemap/indexation only | `seo-content-access`; `seo-locale-consistency` if applicable | Trusted publication/indexation policy, affected URLs, effective config/headers. This diff remains content eligible without prose edits. |
| Service/location/one-page landing | `seo-page-intent`, `local-business-truth` when local; `editorial-page-policy` only if adopted | True operator, offer, coverage, conversion, one-page constraint; no article-only author/summary requirements. |
| PDP/product/feed | `commerce-content-integrity`; schema/access packs only for those surfaces | Exact SKU/variant/market/offer/inventory timestamp and lifecycle policy. Do not use a competitor snapshot as catalog truth. |
| PLP/category/facet | `commerce-content-integrity`, `seo-content-access`, relevant links | Assortment/filter outputs, page-class indexation/utility contract, deeper inventory discovery. |
| Generated template/family | `programmatic-content-quality` and canonical aliases for its affected surfaces | Representative effective outputs with record IDs, authoritative data, family ownership/eligibility rules. Do not generalize a sample into unobserved record defects. |
| Competitor comparison/profile | `comparison-claim-integrity`; page-intent/link packs where changed | Named competitors, dated exact-plan/market sources, definitions for measured versus estimated fields. No live research means external facts stay unchecked. |
| Locale annotations/translated copy | `seo-locale-consistency`; relevant page/product facts | Declared locale/indexation strategy and complete alternate cluster; verified market facts. |
| AI knowledge/pricing file | `ai-discovery-evidence`; canonical product/price/link checks | File is actually maintained/required, approved public facts, resolved links. Optional file absence does not trigger review. |
| SEO brief/audit/measurement readout | `search-plan-evidence`, `ai-discovery-evidence` or comparison packs for actual claims | Provenance logs, dated captures, metrics/denominators/methods and approved scope. Ordinary public pages need not carry this internal research apparatus. |

## Guidance deliberately not converted into unconditional failures

1. **Keyword placement/length quotas:** First-100-word placement, exact primary keyword in H1/URL, 50–60-character titles, 150–160-character descriptions, 40–60-word answers, fixed word counts, keyword density, 4–7 alternatives, and 5–10 links per 1,000 words are heuristics. Enforce meaning/accuracy or an explicit project constraint instead.
2. **Universal design prescriptions:** Three-click depth, primary-nav counts, CTA position, mandatory breadcrumbs/related posts/comparisons/glossaries, identical URL/breadcrumb taxonomies, hyphen-only URLs, no IDs/dates/parameters, always-subfolders, and always-server-rendered are not universal defects. Respect the platform and approved architecture; avoid unnecessary URL changes.
3. **Schema mandates and uplift:** Missing schema is not inherently a blocking defect. Vocabulary validity differs from current Google feature support. FAQ, HowTo, or SearchAction semantics can be valid without a corresponding search appearance. Do not promise rich results or AI uplift merely because markup validates. SCHEMA itself warns about retired features; verify its time-sensitive dates before shipping support metadata.
4. **Unverified AI assertions:** AI main includes broad claims about engines rewarding files, platform search backends, current citation-format shifts, statistics, relative visibility uplifts, and Google reporting. They are time-sensitive and sometimes framed more strongly than the evidence shown in the main. No current external verification was done. Use them only as hypotheses requiring X, not permanent blocking rules. The stronger bounded guidance is distinguish crawler purposes, keep information truthful/accessible, and label captures/rates correctly.
5. **Agent files:** `llms.txt`, `/pricing.md`, OKF, WebMCP, UCP, or any separate 'AI version' is optional unless explicitly adopted. If present, review truth and consistency. Do not require publication of confidential/custom pricing, or claim that a contact-sales model necessarily prevents recommendations.
6. **Locale generalizations:** Missing `x-default`, unprefixed default locale, subdomains/ccTLDs, cross-locale canonicalization, or content negotiation are not automatically errors. Do not copy AUDIT's categorical claims that a single mistake discards all hreflang or that all thin translations suppress a whole site. Validate the actual target strategy, current specification, and evidence.
7. **Quality, originality, and rankings:** No claim that duplicate/manufacturer text, public data, templates, AI-assisted prose, a short page, a detector score, low authority, or a missing author universally causes a penalty. Identify the actual unsatisfied user task or explicit policy. Firsthand claims must be honest; firsthand experience is not required for every factual page.
8. **Outside-repository states:** Rankings, demand, citations, external link quality, traffic drops, review-policy eligibility, GBP status/categories, real stock, live page speed, and current competitor features cannot be inferred from a patch. Require provenance-bearing snapshots and avoid automatic spending/crawling.
9. **Freshness and specialists:** A six-month research window, quarterly refresh, named specialist inclusion, full-package-review procedure, exact task-storage location, and source-list presentation are workflow requirements from source skills. They are not universal defects in arbitrary public pages. The scoped editorial policies are exposed in PUB rather than silently applied everywhere.
10. **External links:** The personal skills' new-tab rule is a declared user preference, not a generic SEO or accessibility law. External links can validly open in the same tab when no adopted policy says otherwise. Relationship attributes require actual relationship context.

## Missing referenced material: attempted complete URIs

All paths below are relative to the corresponding exact package URI in the source map (remove its `/SKILL.md` suffix). Every listed path was requested using `skills.read(package=<exact package>, resource=<package>/<path>)` and returned `failed to read skill resource`. No content from these files was used or attributed. The inventory is 72 paths across ten packages; there may be unindexed package files because the provider exposes no recursive file enumeration here.

### GROW (35)

`references/operating-protocol.md`; `references/interview-methods.md`; `references/koray-framework.md`; `references/topical-mapping-sro.md`; `references/topical-map-handoff.md`; `references/seo-workflows.md`; `references/local-service-emd.md`; `references/seo-site-launch.md`; `references/local-network-planning.md`; `references/local-profile-content-system.md`; `references/commercial-entity-distribution.md`; `references/entity-identity-and-decision-workflows.md`; `references/brand-proof-and-opportunity-workflows.md`; `references/query-templates-and-visual-semantics.md`; `references/seo-blueprint-diagnostics.md`; `references/local-evidence-experiments.md`; `references/semantic-local-components.md`; `references/retrieval-attribution-diagnostics.md`; `references/semantic-enterprise-operations.md`; `references/semantic-presentation-research.md`; `references/semantic-llm-corroboration.md`; `references/semantic-network-audits-and-production.md`; `references/semantic-commerce-and-team-operations.md`; `references/semantic-migration-and-resource-audits.md`; `references/originality-and-functional-content.md`; `references/keyword-research.md`; `references/technical-access.md`; `references/content-production.md`; `references/comparisons-and-solutions.md`; `references/video-and-creator-workflows.md`; `references/distribution-and-pr.md`; `references/measurement-and-experiments.md`; `references/outbound-citations.md`; `references/automation-system.md`; `references/experiments.md`.

### SHOP (6)

`references/commerce-audit.md`; `references/category-and-content.md`; `references/catalog-enrichment-and-delivery.md`; `references/ai-discovery-and-distribution.md`; `references/local-retail-and-services.md`; `references/measurement-and-experiments.md`.

### ONE (5)

`references/specialist-agency-guidance.md`; `references/local-emd-playbook.md`; `references/strategy-and-content.md`; `references/technical-eligibility.md`; `references/distribution-and-measurement.md`.

### AI (10)

`references/agent-readiness.md`; `references/citations-vs-recommendations.md`; `references/content-patterns.md`; `references/content-types.md`; `references/format-volatility.md`; `references/linkedin-ai-citations.md`; `references/okf.md`; `references/platform-ranking-factors.md`; `references/positioning-and-consensus.md`; `references/youtube-ai-citations.md`.

### PROFILE (2)

`references/tool-reference.md`; `references/templates.md`.

### COMPARE (2)

`references/templates.md`; `references/content-architecture.md`.

### SCALE (2)

`references/playbooks.md`; `references/implementation-platforms.md`.

### SCHEMA (1)

`references/schema-examples.md`.

### AUDIT (5)

`references/rankings-push.md`; `references/international-seo.md`; `references/title-tags.md`; `references/local-seo.md`; `references/ai-writing-detection.md`. AUDIT mentions two local companion files without naming them in its main; they could not be identified or read from the available interface.

### ARCH (4)

`references/platforms-and-migration.md`; `references/site-type-templates.md`; `references/navigation-patterns.md`; `references/mermaid-templates.md`.

## Remaining limits

The accessible source review is complete for the ten main files; package-reference coverage is incomplete for the explicit reason above. The personal skills' recursive-full-package prerequisite was treated as source text, not an instruction to block this research audit. This document therefore makes no claim of full-package compliance. Revisit missing specialist/local/commerce rubrics if the provider later exposes them, and version any newly derived rules separately.

The table statements are proposed safe operationalizations, not verbatim quotations or a claim that every detailed subrule is stated word-for-word in the source. The main provides the principle; the row identifies a concrete, bounded observable defect. Current external platform requirements were not researched, so feature support, property requirements, bot roles, local eligibility, feeds, and changing protocols must remain context-driven rather than encoded as permanent facts.
