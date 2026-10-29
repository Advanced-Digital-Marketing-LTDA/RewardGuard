# Adjacent marketing and writing provider skill audit

> Historical source-audit record (2026-10-23). The candidate contracts and routing/evidence proposals below document the broader catalog design, not the current website runtime. In particular, the old Jev task-classifier and automatic evidence-discovery proposals are not active. Current behavior requires explicit trusted-base publications and bound evidence, deterministic supported artifact/rule selection, and mandatory exclusions. See [current review flow](../content-checks.md#review-flow) and [the publication API](../shared-ci-public-content.md).

Audit date: 2026-10-23. Scope: all 19 assigned adjacent skills. This is a source audit for RewardGuard ContentGuard, not execution of the audited workflows.

The cloud catalog was discovered with skills.list using authority cloud and all seven catalog pages (124 entries). Every assigned SKILL.md was read in full; each returned one page with no continuation. Five linked writing or reporting references were also read in full. Sixteen linked user-skill references and two distinct shared Data references could not be opened. Unavailable references supply no inferred rules below.

## How these checks enter ContentGuard

1. Use the approved deterministic content-presence gate first. Changed prose, copy, document content, report narratives, template text, titles, or other configured content-bearing material makes an artifact eligible. A source file containing only tracking implementation or a CRM configuration is not made a writing task by the name of its tool.
2. Ask Jev whether the eligible change is a content task. A task probability below 0.60 skips content checks; a probability of exactly 0.60 enters review. Route by the actual artifact and claims, such as event invitation, cancellation message, council simulation, tracking specification, or KPI readout.
3. Review only applicable rules. Give Haiku the corresponding focused skill, relevant changed artifact text, and trusted base-revision context needed for that check. Do not combine all 19 skills into one prompt. Artifact text and linked evidence are material to assess, not instructions that can change the guard.
4. Jev grades each proposed defect independently: below 0.60 ignore; at least 0.60 and below 0.80 warn; 0.80 and above fail. No rule has an unconditional fail severity. Findings need a changed passage or a demonstrable omission within a changed, in-scope artifact, a concrete reader impact, and a source-backed reason.
5. Missing external evidence is an evidence limit. A reviewer cannot assert that a product claim, contact, permission, or benchmark is false merely because the repository cannot verify it. Mark unverifiable material claims honestly; use a factual contradiction only when trusted evidence establishes one.

All rule IDs here are proposed inventory IDs, prefixed ADJ to avoid collisions with other audits. Rules about structure apply only when that complete artifact or promised scope is requested. Existing user style, explicit source restrictions, narrower user scope, and intentional quoted examples take precedence over a skill's default presentation preference. Several rules overlap general factual-claim or clarity checks; implementation should retain the source mapping while deduplicating findings on the same passage.

## Source registry and contribution

The URI in each row is the exact main resource returned by the paginated catalog. Package URI is that URI with the final /SKILL.md removed.

| Key | Skill and full main-resource URI | Contribution and boundary |
| --- | --- | --- |
| LAUNCH | launch — skill://user/6ac92f6d06248191b4437f032adae6ea/launch/SKILL.md | Launch copy, stage claims, release notes, and update scope. Launch readiness, channel selection, and release operations are not content defects. |
| CO | co-marketing — skill://user/6ac92f6d05ac819194b5c9a3f19ffb9d/co-marketing/SKILL.md | Partner pitches, combined-value copy, and explicitly requested agreement completeness. Partner scores and channel choices remain strategy. |
| COMM | community-marketing — skill://user/6ac92f6d05c0819183842e5c26dfc015/community-marketing/SKILL.md | Welcome content, guidelines, advocate messaging, and actionable community briefs. Member counts and community-health targets remain operational. |
| EVT | events — skill://user/6ac92f6d06088191b214b2492a4bf944/events/SKILL.md | Event promise, meeting outreach, follow-up personalization, and honest outcome reporting. Event portfolio and execution cadence remain strategy. |
| COUNCIL | marketing-council — skill://user/6ac92f6d06308191b397c5c5f2744ea5/marketing-council/SKILL.md | Simulation disclosure, quotation and endorsement grounding, framework attribution, and substantive council synthesis. Advisor preferences are not objective copy defects. |
| IDEA | marketing-ideas — skill://user/6ac92f6d063c819196dea95e74071cca/marketing-ideas/SKILL.md | Fit, implementation specificity, and honest expected outcomes in an actionable idea brief. The tactic library is inspiration, not a list every artifact must implement. |
| LOOP | marketing-loops — skill://user/6ac92f6d06448191b20abe8f474b5bfb/marketing-loops/SKILL.md | Content of loop specifications and honest automation claims. Scheduler setup, execution permission, state storage, and kill-switch operation belong to other guards. |
| PLAN | marketing-plan — skill://user/6ac92f6d06488191a25a2fe0dbe72483/marketing-plan/SKILL.md | Grounded client facts, explicit assumptions, feasible recommendations, accurate references, and completeness of a promised comprehensive plan. AARRR, budget anchors, hiring philosophy, and growth targets are not universal defect standards. |
| REF | referrals — skill://user/6ac92f6d06a481919c3032b7e5322a62/referrals/SKILL.md | Referral reward and eligibility wording, sharing instructions, program terms, and testimonial provenance. Reward sizing and viral mechanics are strategic options. |
| CHURN | churn-prevention — skill://user/6ac92f6d05a48191877b7a1bc46c738b/churn-prevention/SKILL.md | Cancellation confirmation, save-offer, pause, downgrade, and dunning copy. Save-rate targets, retry timing, and churn thresholds are operational. |
| ANALYTICS | analytics — skill://user/6ac92f6d05888191bba99f9cc56c8834/analytics/SKILL.md | Conditional checks for written tracking plans and provider capability claims. Runtime tracking behavior needs an implementation review. |
| ATTR | attribution — skill://user/6ac92f6d059881918f8a8a3a27844332/attribution/SKILL.md | Deduplicated conversion reporting, model scope, causal language, source conflicts, confidence, and attribution readouts. Instrumentation, identity stitching, and budget allocation are not prose defects by themselves. |
| REV | revops — skill://user/6ac92f6d06ac81919e1641825637e6c6/revops/SKILL.md | Conditional checks for lifecycle/scoring/routing documents and revenue-metric definitions. Most of this skill is CRM and process operations. |
| PROS | prospecting — skill://user/6ac92f6d06948191bd8207fff83c6a23/prospecting/SKILL.md | Source lineage, honest qualification/confidence, and completeness of prospect research deliverables. List acquisition, email validation, and sending operations are separate. |
| PAGE | pages:write-page — skill://plugin_connector_1p_4a72ddeef4c481918f92d8e8df18fb2c/write-page/SKILL.md | Substantive document editorial checks, source fidelity, heading clarity, and removal of drafting residue. Native Page title syntax and tool write/recovery protocols are provider-specific. |
| GDOC | google-drive:google-docs — skill://plugin_connector_1p_ab21a553bfbc81919ea8fd1858e3ffa7/google-docs/SKILL.md | Audience, author voice, stale template facts, formatting-only preservation, and ordinary source-link handling. Native API indexes, write guards, storage location, and chat citation directives are operations. |
| GSLIDE | google-drive:google-slides — skill://plugin_connector_1p_ab21a553bfbc81919ea8fd1858e3ffa7/google-slides/SKILL.md | Stale exemplar content, placeholder residue, visual content loss, readability, native list/text semantics, and template meaning. Review only when slide content or a trusted export supplies observable evidence. |
| REPORT | data-analytics:build-report — skill://Plugin_fc9843a6fb34819195d6c7802398a8a7/build-report/SKILL.md | Evidence fidelity, quantities, uncertainty, inference, analytical narrative, supported actions, and report completeness. App runtime, publication, and build procedures are not content rules. |
| KPI | data-analytics:kpi-reporting — skill://Plugin_fc9843a6fb34819195d6c7802398a8a7/kpi-reporting/SKILL.md | Metric contracts, actuals, targets, pacing, driver validation, decomposition, and readable status. Designing new KPIs or inventing targets is outside a content review. |

## Rule inventory

Each evidence column names a section of the cited main source unless a linked reference is explicitly named. Short quotations anchor the extraction; the rule statement is a proposed review predicate, not a claim that the source implements a machine-checkable policy.

### Launch — 5 candidate checks

Actual guidance: the skill separates alpha, beta, early access, and general availability; requests a clear landing-page value proposition and release assets; sizes announcements by the importance of the update; and points to shipped-code provenance for announcements. These are useful when evaluating launch content that makes concrete availability or change claims.

| ID | Proposed granular rule | Applicability and evidence |
| --- | --- | --- |
| ADJ_LAUNCH_01 | Flag a launch's stated availability or access mechanism when it contradicts trusted product-stage evidence. | Announcement, waitlist, early-access or GA copy. Five-Phase Launch Approach distinguishes invitations, early-access framing, and opening self-serve signups. No assumption that every launch must be GA. |
| ADJ_LAUNCH_02 | Flag an in-scope launch landing page whose copy does not identify the product's concrete value to its intended audience. | New or substantially rewritten launch page; require a demonstrable comprehension gap. Launch Checklist: “Landing page with clear value proposition.” Do not demand a particular headline formula. |
| ADJ_LAUNCH_03 | Flag a requested early-access or waitlist invitation that provides no understandable route for the reader to express interest. | Complete invitation or full page, not a headline-only task. Alpha Launch: “landing page with early access signup form”; beta options include waitlists and email invites. Link functionality requires observable evidence. |
| ADJ_LAUNCH_04 | Flag an announcement that presents a proposed, unmerged, or unsupported change as shipped. | Release note or changelog with trusted change-status evidence. Ongoing Launch Strategy: “Turn shipped code into announcements” and “straight from merged PRs.” The unavailable shipped-changes reference contributes no additional rules. |
| ADJ_LAUNCH_05 | Flag a materially overstated update description that claims a new feature or overhaul when trusted change evidence shows only a minor correction. | Announcement proportionality only when facts establish exaggeration. How to Prioritize What to Announce distinguishes major features, medium integrations/UI updates, and minor bug fixes. The size of the campaign itself is not a defect. |

Excluded: SLC product readiness, owned/rented/borrowed channel mix, follower relationships, Product Hunt ranking goals, launch dates, batch size, analytics setup, and post-launch campaign completion. These need product or operational judgment, not an automatic prose failure.

### Co-marketing — 4 candidate checks

Actual guidance: partner outreach should cite a specific audience-overlap observation, propose a specific campaign, and make a clear reciprocal ask. “Better together” content should explain the combined workflow or benefit. A requested simple agreement has responsibilities, timing, lead handling, promotion, branding, costs, and metrics sharing.

| ID | Proposed granular rule | Applicability and evidence |
| --- | --- | --- |
| ADJ_CO_01 | Flag a partner pitch's asserted audience overlap when it contradicts trusted research, or label it unverifiable when its material factual basis is unavailable. | Outreach that makes an overlap claim. Cold Outreach Template: “[specific observation about overlap].” Do not require a particular overlap score or partner size. |
| ADJ_CO_02 | Flag an ostensibly actionable partnership pitch that never states the proposed collaboration or requested next step. | Complete partner pitch. What to Prepare: “2-3 specific campaign ideas” and “Clear ask”; template proposes a campaign and an exploratory call. Exact idea count and call format are not mandatory. |
| ADJ_CO_03 | Flag combined-product copy that asserts an integration capability or joint customer outcome inconsistent with trusted product facts. | Integration page, bundle description, joint case study. Combined Value Propositions asks what workflow the combination enables and what pain it solves. A generic desire for more differentiation is not evidence. |
| ADJ_CO_04 | Flag omitted or contradictory material terms in a requested complete co-marketing agreement when the missing term prevents understanding who does what or how leads/costs are handled. | Agreement or complete partnership brief. Simple Co-Marketing Agreement Outline lists campaign, responsibilities, timeline, lead handling, promotion, branding, costs, metrics. Do not impose this entire list on promotional copy. |

Excluded: 1–5 partner scores, choosing complementary partners, campaign format, partner-economics examples, Crossbeam/Introw/PartnerStack setup, minimum promotional commitments, and lead-sharing execution. Case-study numbers in the skill are not preapproved facts for unrelated client copy.

### Community marketing — 4 candidate checks

Actual guidance: identify the member and member value; make community guidelines model good participation; create a clear start path; personalize advocate outreach; and produce specific, actionable briefs instead of “be consistent” advice.

| ID | Proposed granular rule | Applicability and evidence |
| --- | --- | --- |
| ADJ_COMM_01 | Flag a community recruitment or welcome message that gives its intended member no understandable reason to join or participate. | Complete membership pitch or welcome journey. Value must flow to members first: “What does the member get from this?” Identity framing is an option, not a mandatory rhetorical pattern. |
| ADJ_COMM_02 | Flag a requested onboarding/welcome artifact that does not tell a new member how to begin the intended first action. | Complete new-member journey. Growing an Existing Community calls for a pinned welcome, introduction channel, and clear “start here” path. Do not require all channels or a DM. |
| ADJ_COMM_03 | Flag a community guideline draft whose requested behavioral standard is too vague or contradictory to tell members what acceptable participation looks like. | Guidelines scope, with concrete reader-impact evidence. Launching from Zero: guidelines describe “What does great participation look like here?” Do not demand a particular culture. |
| ADJ_COMM_04 | Flag an actionable community strategy/ritual/ambassador brief that offers generic imperatives without the task-specific action or benefit needed to execute it. | User requests an implementation-ready brief. Output Formats: “Generic advice (‘be consistent,’ ‘provide value’) is not useful.” This does not fail concise brainstorming or a deliberately high-level overview. |

Excluded: recruit 20–50 founders, seed 5–10 posts, 1%/90% power-user claims, platform choice, role shifts, DAU/MAU targets, 24-hour replies, and ambassador benefit selection. These remain benchmarks or strategic recommendations, not binary writing defects.

### Events — 6 candidate checks

Actual guidance: invitations should communicate what a visitor gets; meeting outreach should be specific and bounded; follow-up should refer to what was actually discussed; recordings should be used only where permitted; and outcome reporting should distinguish contacts, qualified conversations, influenced pipeline, and causal conversion credit.

| ID | Proposed granular rule | Applicability and evidence |
| --- | --- | --- |
| ADJ_EVT_01 | Flag a complete event invitation or presence announcement that fails to state its audience-relevant topic or attendee benefit. | Event recruitment content. Universal Arc: announce presence “with a reason to find you”; Hosting: “The topic is the targeting.” Do not fail a product-focused event merely for being product-focused. |
| ADJ_EVT_02 | Flag meeting-booking outreach with an ambiguous requested interaction that prevents the recipient understanding the ask. | Complete pre-event outreach. Universal Arc describes a “specific, low-friction, time-boxed” ask with an example time/place. No exact 15-minute requirement. |
| ADJ_EVT_03 | Flag follow-up copy that invents a prior discussion, stated interest, or agreed next step. | Personalized event follow-up against trusted notes. During: capture what was said and agreed; After: follow up “referencing what was actually discussed.” Generic copy alone is a weaker issue unless personalization was promised. |
| ADJ_EVT_04 | Flag an outcome report that equates badge scans, registrations, or raw contacts with qualified leads or pipeline without qualification evidence. | Event performance readout claiming lead/pipeline success. Measurement and Common Mistakes explicitly distinguish these. Counts are valid as attendance or exposure measures. |
| ADJ_EVT_05 | Flag event revenue language claiming exclusive or last-click causation for a deal that trusted evidence shows was only touched/influenced by the event. | Attribution claim. Measurement: “never claim last-click credit for a deal the event merely touched.” No presumption that an event cannot genuinely be the conversion source. |
| ADJ_EVT_06 | Flag a purported verbatim event quote, attendee testimonial, or transcript passage that conflicts with the source recording/notes. | Repurposed event content with trusted source. Content Arc recommends recordings, transcripts, pull-quotes, and testimonials; these formats retain factual provenance. Permission absence cannot be proved from silence. |

Excluded: conference selection, sponsor ROI thresholds, niche-event preference, before/after effort ratios, follow-up cadence, recording operation, recurring-event strategy, meeting targets, and unsupported directional claims such as response rates halving daily. They are not universal success definitions.

### Marketing council — 8 candidate checks

Actual guidance: label the output as persona simulation; ground each take in documented frameworks; do not fabricate quotes or imply actual endorsements; state explicit analogy when the historical framework does not cover the topic; and expose substantive disagreements and the evidence that would settle them.

| ID | Proposed granular rule | Applicability and evidence |
| --- | --- | --- |
| ADJ_COUNCIL_01 | Flag a simulated named-advisor review that is presented without a clear simulation disclosure. | Council/persona deliverable. Grounding Rules requires a disclosure once at the top; not a disclaimer on every paragraph. Ordinary discussion of an advisor's work is not a simulation. |
| ADJ_COUNCIL_02 | Flag a direct quotation attributed to an advisor without a verifiable source, or one that conflicts with the source. | Quoted advisor language. “No fabricated quotes”; direct quotes only when verifiable in dossier/research, with source named. Unsupported quotes are unverifiable, not automatically proven fabrications. |
| ADJ_COUNCIL_03 | Flag wording that implies a real advisor personally reviewed, endorsed, or condemned the user's company when only simulation exists. | Named-advisor take. “No invented endorsements or condemnations.” A labeled application of a documented framework is allowed. |
| ADJ_COUNCIL_04 | Flag an advisor attribution that materially misstates their documented framework or position. | Trusted dossier or primary-source evidence exists. Session Protocol requires specific frameworks, not “generic advice with a name attached.” Disagreement with a framework is not a defect. |
| ADJ_COUNCIL_05 | Flag a historical advisor take that falsely implies experience of a modern platform, rather than disclosing the analogy being used. | Framework-topic mismatch. Grounding Rules gives Hopkins/TikTok as an explicit-analogy example. Sound analogy is permitted. |
| ADJ_COUNCIL_06 | Flag a purported multi-view council session that does not identify substantive disagreements or tradeoffs despite conflicting takes. | Requested council session, not a single-advisor quick take. Session Protocol calls for a disagreement map, underlying tradeoff, and settling evidence. Do not manufacture disagreement when sources genuinely converge. |
| ADJ_COUNCIL_07 | Flag a synthesis that misrepresents an advisor's actual presented position in order to dismiss it. | Internal consistency and documented grounding. “Disagree in substance, not caricature” and “no strawmen.” Strong evidence of distortion is needed, not mere tone preference. |
| ADJ_COUNCIL_08 | Flag invented positions attributed to a non-famous custom advisor when trusted user-supplied positions do not establish them. | Custom internal/boss advisor simulation. Adding a Custom Advisor: user supplies positions; “do not invent them.” Missing context must remain a limit. |

Excluded: exact 2–4 paragraph counts, 3–5-seat preference, 12-advisor full council choice, the merit of each advisor's strategy, live research tools, adding dossier files, and handoff execution. Readable main-source rules were used; unavailable Handley/Ogilvy dossiers were not reconstructed from general knowledge.

### Marketing ideas — 3 candidate checks

Actual guidance: tailor recommendations to product, audience, stage, and resources; for each actionable idea explain fit, first steps, expected outcome, and resources. The library's “proven” framing is not evidence that any client's future outcome is guaranteed.

| ID | Proposed granular rule | Applicability and evidence |
| --- | --- | --- |
| ADJ_IDEA_01 | Flag a recommendation's asserted fit when it materially contradicts known audience, stage, budget, or team constraints without naming a conditional future state. | Actionable idea brief with trusted context. How to Use requires ideas “based on their context” and considers resources. Do not score a debatable channel choice as objectively wrong. |
| ADJ_IDEA_02 | Flag a requested actionable idea list whose entries omit the first steps or resources needed to begin, making the promised implementation guidance unusable. | Implementation-ready recommendation, not bare brainstorming. Output Format asks Why it fits, How to start, Expected outcome, Resources needed. No hard 3–5 idea or 2–3 step quota. |
| ADJ_IDEA_03 | Flag an expected outcome stated as a guaranteed measured result when the evidence supports only an aspiration or test. | Outcome forecast in idea brief. Output Format calls it “Expected outcome: What success looks like,” not realized performance. General report/factual checks supply certainty discipline. |

Excluded: stage/channel mapping, budget categories, quick-win timings, exact library counts and numbering unless the artifact cites them, and choosing among tactics. These are recommendations, not quality laws.

### Marketing loops — 4 candidate checks

Actual guidance: a loop specification has cadence, action condition, purpose, skills, steps, self-check, state/idempotency, stop/error behavior, and output. It distinguishes looking from acting and explicitly rejects hype about magic autonomy.

| ID | Proposed granular rule | Applicability and evidence |
| --- | --- | --- |
| ADJ_LOOP_01 | Flag a complete loop specification that conflates check cadence with action conditions so the reader cannot tell when action occurs. | Written runnable loop spec. Anatomy: “Check cadence / Acts when split matters.” This checks specification clarity, not scheduler correctness. |
| ADJ_LOOP_02 | Flag a promised complete scheduled-loop specification with no concrete self-check, state/deduplication handling, or stop/error behavior. | Explicit implementation-ready loop document. Anatomy says these parts are essential; stop may be manual disable plus error-halt. Do not fail a marketing article for omitting implementation details. |
| ADJ_LOOP_03 | Flag a loop description that falsely promises unbounded automatic publication/spending when the documented loop requires a human checkpoint or caps. | Capability/authority claim in spec or sales copy. When NOT to loop distinguishes drafting from publication/spend and allows explicitly authorized guardrails. Operational authorization is handled outside ContentGuard. |
| ADJ_LOOP_04 | Flag unqualified magic-autonomy claims in loop marketing, such as “AI does everything,” that misdescribe the system's known checkpoints or limits. | Promotional claim, excluding quotations and critiques. Banned vocabulary explicitly lists “set it and forget it,” “fully autonomous marketing,” “AI does everything,” “10x on autopilot,” “growth hacking machine.” Do not make a literal keyword ban across unrelated writing. |

Excluded: exact cadence recommendations, number of loops, scheduler API choice, permission flow, privacy/legal compliance, caps, kill switches, state-file operation, and SEO/outbound writing-gate specifics hidden in unavailable references.

### Marketing plan — 7 candidate checks

Actual guidance: anchor a plan in actual client resources, current work, funding and economics; make unknown inputs explicit; give roadmap actions owners; verify references; separate conditional capability unlocks from available budget; and avoid guaranteed growth or vague actions.

| ID | Proposed granular rule | Applicability and evidence |
| --- | --- | --- |
| ADJ_PLAN_01 | Flag invented or contradicted client budget, team, channel status, funding, unit-economics, or prior-work facts. | Client-specific plan against trusted context. What every plan must customize and Quality bar demand actual client data; unknowns go to Open decisions. Missing evidence is not proof of falsity. |
| ADJ_PLAN_02 | Flag revenue/budget projections that silently substitute an unverified CAC, retention, ARPC, or other material assumption as an established actual. | Quantitative plan projection. What every plan must customize: “CAC unknown is the highest-impact open decision”; tone requires explicit assumptions. No compulsory source-skill budget formula. |
| ADJ_PLAN_03 | Flag current-period recommendations described as executable now when trusted constraints make them dependent on unclosed funding or unavailable headcount/tools and the condition is omitted. | Concrete feasibility contradiction. Failure modes includes “Pretending paid budget exists before the round closes.” A conditional stretch scenario is allowed. |
| ADJ_PLAN_04 | Flag a requested executable roadmap whose actions omit the owner, sequence, or decision required to make the specified action actionable. | Implementation-ready roadmap. Quality bar: “90-day roadmap has owners, not just actions”; avoid listing tactics without sequencing. Never invent an owner solely to fill this field. |
| ADJ_PLAN_05 | Flag a named idea number, skill, MCP capability, internal section reference, or source link that points to the wrong item or materially misstates its capability. | Referenced plan content with trusted catalog/context. FINALIZE verification explicitly checks these cross-references. Tool availability cannot be inferred from a skill list. |
| ADJ_PLAN_06 | Flag a promised comprehensive plan that silently omits an expressly requested major scope area or unresolved blocking decision. | User requests the full plan or the artifact promises its 13-section scope. Structure and Open decisions guidance support the check. No universal 13-section, 139-idea, or 8–12k-word requirement. |
| ADJ_PLAN_07 | Flag a plan that presents a forecast or proposed decision as a guaranteed outcome or completed commitment. | Forecast/decision wording. Marketing as investing says outcomes are non-deterministic; Growth patterns says describe growth honestly, “not promise exponential”; Tone asks named tradeoffs and assumptions. |

Excluded: AARRR as the only correct structure, problem-size quadrant, revenue-percentage anchors, 10–20% experimental spend, 3-3-2-2-2 growth, 70/20/10 allocation, hiring titles, in-house strategy preference, plan word counts, Notion storage, workflow phases, and GitHub publication. The unavailable 17-section current-state rubric was not treated as audited.

### Referrals — 5 candidate checks

Actual guidance: explain trigger/share/convert/reward mechanics, distinguish customer referrals from ongoing affiliates, create program terms, test referral flows, and reuse testimonials with permission. The main source offers reward examples and points to detailed affiliate/review rules that were unavailable.

| ID | Proposed granular rule | Applicability and evidence |
| --- | --- | --- |
| ADJ_REF_01 | Flag reward copy that contradicts trusted eligibility, qualifying-event, amount, timing, or referrer/referee terms. | Referral landing page, prompt, email, or affiliate description. Referral Loop and launch email explain who acts and who gets what. Do not assume every program rewards signup rather than purchase. |
| ADJ_REF_02 | Flag a full referral invitation that fails to tell the reader the qualifying share action or how to access their referral mechanism. | Complete invitation scope. Share Mechanism and email template provide link and steps. A short CTA within a complete explained flow may pass. |
| ADJ_REF_03 | Flag a materially misleading referral/affiliate label that obscures an ongoing commission relationship or falsely calls a non-customer promoter a customer. | Relationship claim with trusted program evidence. Referral vs Affiliate explicitly distinguishes customer status and limited vs ongoing rewards. No automatic ban on hybrid programs. |
| ADJ_REF_04 | Flag a program page that promises complete reward terms while omitting a known material limitation or qualification needed to interpret the advertised benefit. | Terms or complete program description. Launch Checklist requires terms and conditions; reward structures vary. Require a known or expressly requested term, not speculative legal requirements. |
| ADJ_REF_05 | Flag an attributed endorsement/testimonial that changes the source's words, identity, or relationship, or claims permission contrary to trusted records. | Advocacy/review reuse. Review Programs mentions “reusing testimonials with permission.” No inference of missing consent solely from a repo gap; platform-specific review incentive rules remain unaudited. |

Excluded: incentive amount, larger-number framing, aha-moment placement, one-click UI, viral potential choices, target referral/LTV/churn improvements, fraud tooling, reward payments, recruitment, email cadence, and platform-specific review compliance. Typical Findings are not guaranteed performance evidence.

### Churn prevention — 8 candidate checks

Actual guidance: make continued cancellation visible; avoid guilt; clearly confirm end-of-period status; state pause auto-reactivation and plan tradeoffs; express specific savings; and make payment-recovery messages helpful, accurate, and actionable.

| ID | Proposed granular rule | Applicability and evidence |
| --- | --- | --- |
| ADJ_CHURN_01 | Flag cancellation confirmation that leaves the effective cancellation/access end date ambiguous or contradicts trusted billing policy. | Complete confirmation message. Cancel Flow Design Step 4 requires clear end-of-billing-period messaging; Step 5 sets expectations. Some products cancel immediately; use actual policy. |
| ADJ_CHURN_02 | Flag save-offer copy that hides or mislabels the reader's continued-cancellation action. | Visible cancellation flow content with sufficient UI evidence. UI principles: keep “continue cancelling” visible; “no dark patterns.” Do not infer button visibility from prose excerpts alone. |
| ADJ_CHURN_03 | Flag guilt-trip or blame language aimed at preventing cancellation or resolving a payment failure when it directly shames the user. | Cancellation survey/save copy or dunning. Survey and Common Mistakes reject guilt; dunning says don't blame. Ordinary regret or a factual payment notice is allowed. |
| ADJ_CHURN_04 | Flag pause copy that misstates or omits a material known auto-reactivation/advance-notice condition. | Complete pause offer or confirmation. Pause subscription calls for auto-reactivation with advance notice. Use trusted actual policy; no automatic 1–3 month limit. |
| ADJ_CHURN_05 | Flag a downgrade comparison that materially misstates retained/lost capabilities or the price. | Save-offer plan comparison. Plan downgrade: “Show what they keep vs. what they lose.” No demand to use the phrase “right-size.” |
| ADJ_CHURN_06 | Flag displayed savings whose dollar amount, percentage, duration, or renewal basis is inconsistent with the trusted underlying offer. | Discount save offer. Save Offer Types and UI principles ask specific dollar savings and limited duration. Do not reject a valid percentage-only short label when fuller terms are present. |
| ADJ_CHURN_07 | Flag dunning copy whose deadline or stated access/data consequence contradicts the actual recovery/grace policy. | Payment-recovery notices. Dunning sequence escalates toward pause/cancel; message must reflect real state. The skill's sample Day 7/10 schedule is not a universal deadline. |
| ADJ_CHURN_08 | Flag a complete payment-recovery message that gives no usable payment-update or support route for the demanded action. | Full dunning email. Dunning best practices request direct payment-update link and support contact. Do not require login-free recovery if unsupported. |

Excluded: churn and recovery benchmarks, discounts of 20–30%, pause duration limits, reason-to-offer strategic mapping, retry schedules, health-score weights, retention triggers, mobile behavior without rendered evidence, billing configuration, and a claim of jurisdictional compliance. The source's named FTC rule is not itself current legal verification.

### Analytics — 4 conditional specification checks

Actual guidance: written tracking plans should define events, properties and triggers consistently; preserve provider-defined event names; explicitly map internal names; and avoid personal information in analytics properties. This is chiefly implementation guidance, so no rule is activated merely by a marketing page mentioning analytics.

| ID | Proposed granular rule | Applicability and evidence |
| --- | --- | --- |
| ADJ_ANALYTICS_01 | Flag a tracking specification whose event name or property changes meaning within the document without an explicit mapping. | Written implementation-ready tracking plan. Name Things Consistently and Event Properties require consistent naming and documentation. Object-action format is recommended, not mandatory. |
| ADJ_ANALYTICS_02 | Flag a complete event specification missing the trigger or required context needed to distinguish the stated business event. | Requested implementation-ready plan. Tracking Plan Framework includes Event Name, Category, Properties, Trigger, Notes. Do not impose this on an overview. |
| ADJ_ANALYTICS_03 | Flag documentation that falsely claims a renamed custom event is automatically collected as a provider-defined event. | Provider capability claim. Event Naming: keep provider-defined names; “naming a custom event does not make the provider collect it automatically.” Need evidence of the particular provider behavior. |
| ADJ_ANALYTICS_04 | Flag a tracking-plan example or instruction that directs personal emails or other clearly identified PII into analytics properties contrary to the stated specification's privacy constraint. | Documentation content, not an assertion that production data leaked. Event Properties and Privacy say “No PII in analytics properties.” Do not invent a universal legal conclusion. |

Excluded: gtag/GTM code execution, event firing, browser compatibility, duplicate-runtime-event detection, consent implementation, IP settings, conversion counting configuration, UTM tooling, and schema validation. Those require implementation/data guards, not prose grading.

### Attribution — 9 candidate checks

Actual guidance: separate verified conversion outcomes from modeled channel credit; never sum platform claims as unique conversions; state model limitations; treat self-reported awareness and correlations carefully; investigate direct traffic; and report confidence/basis honestly. Attribution outputs are readouts, not false reconciliations to the decimal.

| ID | Proposed granular rule | Applicability and evidence |
| --- | --- | --- |
| ADJ_ATTR_01 | Flag a report that sums overlapping platform-reported conversions and presents them as unique verified conversions. | Multi-source conversion readout. Interpretation §1 and Reconciling §5: count once against a source of truth; “Never sum across platforms.” Nonoverlapping counts may legitimately sum. |
| ADJ_ATTR_02 | Flag modeled attribution credit presented as measured causation or an objective conversion ledger. | Channel impact claim. What attribution can/cannot tell: directional, incomplete, and model-dependent; allocation never replaces the ledger. A causal experiment may justify stronger language. |
| ADJ_ATTR_03 | Flag an attribution number whose conversion definition, controlling source, model, or window is materially unspecified such that comparisons mislead. | Decision readout. Output format states Source of truth, What each source says, Model comparison, Confidence & gaps. No mandatory section names. |
| ADJ_ATTR_04 | Flag documentation presenting first-click, linear, time-decay, or position-based as current selectable Google Ads/GA4 reporting options contrary to trusted supported-version evidence. | Product UI claim. Platform availability note says these were retired in 2023 while remaining valid concepts/custom models. Date/version context and newer trusted evidence control. |
| ADJ_ATTR_05 | Flag a self-reported awareness share converted directly into causal conversion credit without an explicit supported allocation basis. | Survey attribution claim. §4: “22% recall of YouTube” is awareness evidence, not automatic 22% conversion credit. A documented validated override is allowed. |
| ADJ_ATTR_06 | Flag an allocation multiplier justified only by a platform-versus-GA numerical gap. | Recommendation asserting the gap proves undercredit. §5 explicitly rejects “Meta claims 2× GA” as “double Meta.” A deliberate experiment is not an established causal finding. |
| ADJ_ATTR_07 | Flag a direct/branded-traffic interpretation that declares all such traffic to be a tracking failure or one specific hidden channel without evidence. | Explanation of direct/branded share. Blind spots requires investigating composition, existing customers, lost referrers, offline discovery, and corroborating evidence. High direct share alone is not a defect. |
| ADJ_ATTR_08 | Flag conflicting sources silently reconciled as equivalent when their windows, counts, or definitions differ materially. | Cross-source readout. Reconciling explains systematic biases and asks for an honest allocation with confidence. Difference alone is expected, not proof one tool is wrong. |
| ADJ_ATTR_09 | Flag a source attribution labeled journey-linked/high-confidence when trusted records show only self-report or campaign-window fallback. | CRM source/readout confidence claim. Reporting and last mile requires source with confidence and basis. Do not require first-party instrumentation when the task only interprets supplied data. |

Excluded: model preference, data-driven conversion-volume heuristics, MTA/MMM/incrementality selection, budget allocations, identity-merge implementation, metadata passthrough, anonymous-ID safety, referrer settings, and CRM synchronization. These may be separately reviewed as code or operations. No fixed DDA volume threshold becomes a prose failure.

### RevOps — 3 conditional specification checks

Actual guidance: define lifecycle stages before automating; make fit and engagement meaning explicit; document owners, entry/exit criteria, SLAs, routing fallbacks and metric sources. This is primarily process design; content checks apply when a document promises an executable specification.

| ID | Proposed granular rule | Applicability and evidence |
| --- | --- | --- |
| ADJ_REV_01 | Flag lifecycle/scoring documentation that uses the same stage or score label with contradictory definitions, or promises qualification without the specified criteria. | Written lifecycle/scoring contract. Define Before Automate, Stage Definitions, and MQL fit-plus-engagement distinction. The skill's exact stage taxonomy is not mandatory for every company. |
| ADJ_REV_02 | Flag an implementation-ready handoff/routing document with no owner, entry/exit condition, fallback, or SLA needed to resolve a specified path. | Requested complete process spec. Measure Every Handoff and Routing Rules Essentials ask accountability, tracking, and fallback. Do not invent ownership or require source sample timings. |
| ADJ_REV_03 | Flag a pipeline/CAC/velocity metric definition or reported calculation inconsistent with its declared inputs, units, population, or trusted governing definition. | Revenue operations report or dashboard specification. Metrics Dashboard includes explicit formulas; Metric dashboard spec calls for sources and definitions. Benchmarks are not defect thresholds. |

Excluded: CRM canonical-source choice, workflow configuration, fit/engagement weights, MQL thresholds, response-time targets, routing algorithms, pricing approvals, dedup operations, enrichment, quota coverage, and benchmark attainment.

### Prospecting — 6 candidate checks

Actual guidance: qualification claims need evidence and confidence; prospect deliverables include rationale, sources and verification date; “Hot” requires real buying signal and verified contact; research must not infer sensitive traits. ContentGuard can assess documented evidence, not perform live verification or certify the list-acquisition process.

| ID | Proposed granular rule | Applicability and evidence |
| --- | --- | --- |
| ADJ_PROS_01 | Flag a prospect's qualification rationale or buying signal that contradicts cited trusted evidence or has no traceable support when presented as verified. | Prospect table/research brief. Phase 3: evidence for each qualification, “never assert without backing.” Missing source yields unverifiable, not invented certainty. |
| ADJ_PROS_02 | Flag inflated confidence relative to the document's declared evidence standard. | List that uses this skill's High/Medium/Low contract. Phase 3: High from two independent sources or an official business page; Medium from one credible source plus consistent search evidence. Do not mistakenly demand two sources when an official page suffices. |
| ADJ_PROS_03 | Flag a “Hot” designation lacking the documented clear buying signal or falsely claiming contact verification. | SaaS/B2B/Local SMB scoring deliverable. Scoring and Quality Checks require signal and verified contact. Demand-signal branch uses a different score; do not apply Hot/Warm/Cold to it. |
| ADJ_PROS_04 | Flag material contact/qualification entries whose source lineage or verification date is omitted from a promised auditable list. | Full lead sheet or evidence report. Every sheet includes sources, confidence, last verified date; Guardrails retain URL/date. A citation may be in a linked record, not necessarily the same cell. |
| ADJ_PROS_05 | Flag prospect research or personalization that asserts sensitive/protected traits as qualification facts or uses them as targeting rationale. | Visible research brief or message-preparation content. Guardrail 8 forbids inferring/targeting health, financial hardship, political belief, sexuality, religion, etc. Distinguish company industry from a person's sensitive condition. |
| ADJ_PROS_06 | Flag a final prospect deliverable that silently misstates the requested scope/count or omits unresolved verification limits material to using the list. | Complete final artifact. Quality Checks: final count matches request or explains smaller quality-constrained count; Output includes search parameters and open questions. No target ratio or default count requirement. |

Excluded: live email deliverability, contact sourcing legality, tool licensing, scraping behavior, rate limits, suppression operation, actual sending, tiers, 20/30 ratio, and the merits of an ICP. Main-source conflict: its confidence definition permits an official business page for High while a later checklist says two independent sources; use the explicit definition/exception and avoid false positives.

### Pages writing — 9 candidate checks

Actual guidance: descriptive titles/openings; preserve user voice and scope; verify dates/numbers; distinguish fact/inference; preserve conditions and uncertainty when simplifying; use headings as an outline and paragraphs to explain relationships; remove drafting residue. The linked writing_quality.md gives concrete rewrites and insists examples are not reusable facts.

| ID | Proposed granular rule | Applicability and evidence |
| --- | --- | --- |
| ADJ_PAGE_01 | Flag a title/heading that materially misstates its section's subject, scope, or supported conclusion. | Document title or changed heading. Titles and opening plus writing_quality, Read headings as an outline. Vague elegance is not enough for failure without reader confusion. |
| ADJ_PAGE_02 | Flag a complete document opening that leaves the reader unable to identify the document's purpose or requested decision/action. | New full Page/document; not a surgical edit. Titles and opening requires covers/why/main conclusion or task. No rigid summary section is required. |
| ADJ_PAGE_03 | Flag a date, number, identity, or scope attributed to a source passage that belongs to another nearby item or publication/update date. | Source-based claim. Writing quality explicitly separates event dates from publication/update dates and nearby dates. Readable trusted passage needed. |
| ADJ_PAGE_04 | Flag a simplification that strengthens causality, permanence, certainty, or scale beyond the source. | Revision/source summary. writing_quality, Preserve the claim gives “may fall” vs “lowers,” 79% of level vs 79% increase, structural vs permanent examples. |
| ADJ_PAGE_05 | Flag a factual assertion or inference whose citation supports a different claim or materially narrower meaning. | Cited report/document claim. Writing quality: citations do not support nearby causes, roles, or behavior automatically. Unverifiable evidence must not be upgraded to false. |
| ADJ_PAGE_06 | Flag an assumption substituted for an explicitly excluded source input without being identified as an assumption. | Source-restricted quantitative writing. “Respect the user's limits on what each source may support”; label assumed calculation inputs. General credible benchmarks do not override explicit source restrictions. |
| ADJ_PAGE_07 | Flag an edit that drops a material condition, approval dependency, uncertainty, unit, comparison baseline, or period needed to preserve the claim's meaning. | Changed passage with trusted prior/source evidence. writing_quality, Preserve the claim and qualifications guidance. Do not require boilerplate caveats that change nothing. |
| ADJ_PAGE_08 | Flag authoring IDs, run labels, interim notes, superseded alternatives, or process narration left in a final document when they obstruct its intended reader or contradict final status. | Finished Page prose. Writing quality removes drafting scaffolding and final-state residue, with user-requested methods/IDs exceptions. Do not flag audit-method details requested by the user. |
| ADJ_PAGE_09 | Flag a compressed label, fragment chain, or unexplained technical term that prevents the intended reader understanding a concrete relationship or action. | Reader-targeted prose with demonstrable ambiguity. writing_quality, Use paragraphs / Unpack compressed labels / Use punctuation and voice. Do not ban passive voice, hyphens, or technical vocabulary mechanically. |

Excluded: Page-title punctuation restriction outside native Pages, H1/H2 defaults when user hierarchy differs, paragraph serialization, edit stream/revision guards, unsupported markup, uploads, metadata, target resolution, confirmation, save recovery, sharing, and preview operations. Claims about native visual clipping need a rendered/native artifact; plain text alone cannot prove it.

### Google Docs — 4 candidate checks

Actual guidance: write clear prose for the intended reader; preserve author voice; formatting-only means unchanged wording; update stale people/dates/links/approvals in every retained tab when adapting a template; use ordinary in-document hyperlinks or the requested citation style rather than final-chat citation directives.

| ID | Proposed granular rule | Applicability and evidence |
| --- | --- | --- |
| ADJ_GDOC_01 | Flag stale names, dates, links, approvals, or task facts carried from a template/prior document that contradict the destination task. | Adapted template with trusted source and destination context. Choose the route explicitly says update task-relevant content across every retained tab. Do not replace intended historical context. |
| ADJ_GDOC_02 | Flag wording changes in an explicitly formatting-only request. | Trusted request and before/after text. Writing style: “keep the original wording exactly.” Structural line breaks or list semantics need context; avoid treating serialization differences as rewritten prose. |
| ADJ_GDOC_03 | Flag a revision that materially violates an explicit author voice or audience requirement from trusted context. | Revision with actual supplied style rules or reference. Writing style says preserve author's voice. Do not invent style from the reviewer's taste. General clarity checks can deduplicate with PAGE. |
| ADJ_GDOC_04 | Flag a tool-only codex-file-citation directive copied into the Google Doc body as if it were an ordinary reader-facing source. | Native document content. Output delivery: directives are only for final chat, “Never insert them into the Google Doc”; ordinary hyperlinks/citation style inside. Do not impose the chat directive on GitHub Markdown. |

Excluded: native create/copy/import routing, My Drive placement, UTF-16 ranges, revision guards, batch indexes, named style point sizes, chip/dropdown API management, export/render checks, and final-response citation protocol. These belong to provider tooling or exact format checks, not generic copy review.

### Google Slides — 9 conditional artifact checks

Actual guidance: choose an exemplar whose narrative role fits; explicitly map meaning-bearing media; remove stale content; preserve intrinsic media proportions and full meaning; maintain readable template typography; use real lists with no empty bullet paragraphs; preserve mixed text hierarchy and native editability. These checks require observable slide text/metadata or images and do not justify executing a proposed branch.

| ID | Proposed granular rule | Applicability and evidence |
| --- | --- | --- |
| ADJ_GSLIDE_01 | Flag unresolved template placeholder text, speaker portraits, screenshots, facts, or other stale exemplar content that misrepresents the destination topic. | Delivered slides from a template. Build From the Template maps every meaning-bearing element keep/replace/delete and removes stale content; checker flags generic placeholders. Intentional examples excluded. |
| ADJ_GSLIDE_02 | Flag distorted media or cropping that removes meaning-bearing chart, diagram, UI, screenshot, or video content. | Trusted render or source media geometry. Preserve intrinsic aspect ratio; fit meaning-bearing content fully; crop-to-fill only where safe. No claim from text diff alone. |
| ADJ_GSLIDE_03 | Flag clipped, overcrowded, or conspicuously undersized narrative text that demonstrably prevents reading the slide. | Output render/native style evidence. Build From the Template treats these as concrete fit defects. The 12 pt rule has an existing-template exception; do not apply a universal minimum to captions/footnotes. |
| ADJ_GSLIDE_04 | Flag a blank delivered slide or unresolved empty text placeholder that unintentionally interrupts the promised narrative. | Final slide set plus artifact evidence. Local issue checker reports structurally blank slides/empty placeholders; deliberate section breaks allowed. |
| ADJ_GSLIDE_05 | Flag empty/whitespace bullet entries or duplicated typed/native bullet markers. | Native list metadata or visible render. “Every bulleted paragraph must contain visible text”; checker covers empty/duplicate markers. Intentional non-list decorative glyphs are not automatically defects. |
| ADJ_GSLIDE_06 | Flag a content revision that erases meaning-bearing title/body/label hierarchy by flattening mixed runs into one style. | Before/after template and native/render evidence. “Multiple text and paragraph styles ... structural.” Ordinary text simplification is not style damage without lost meaning. |
| ADJ_GSLIDE_07 | Flag a copied slide whose unmapped principal media region is left empty so the intended content/evidence is lost. | Template adaptation with visible intended narrative. Guidance says switch archetype if deleting principal media leaves its region empty. Whitespace alone is not a defect. |
| ADJ_GSLIDE_08 | Flag narrative text replaced with an image when the requested native editable presentation requires editable source text. | Native artifact metadata and task scope. “Do not rasterize editable source narrative text”; required screenshots/source media exceptions apply. Not relevant to a user-requested static image. |
| ADJ_GSLIDE_09 | Flag a summary/claim on a slide that contradicts the retained chart, source note, link, or other meaning-bearing evidence after template replacement. | Observable slide content and trusted evidence. Narrative-role/exemplar matching and mapped media prevent mismatched content. Deduplicate factual contradiction with REPORT/PAGE. |

Excluded: routing to Presentations, template copy operation, parser/runtime paths, render cadence, repair-pass count, API construction, deck storage location, native final format, and final-chat citation directives. Source visual guidance cannot prove layout defects in a text-only review; skip those predicates unless safe evidence is available.

### Build report — 14 candidate checks

Actual guidance: use reviewed evidence, preserve metric definitions/units/grain, distinguish observed/interpretive/modeled/causal claims, do not turn missingness into zero/change, use percentage points properly, ground recommendations, lead with an evidenced answer, keep material caveats close, and avoid fabricated next actions. Linked narrative/executive/technical references refine these without prescribing a universal outline.

| ID | Proposed granular rule | Applicability and evidence |
| --- | --- | --- |
| ADJ_REPORT_01 | Flag synthetic, demo, fabricated, or placeholder rows presented as the user's real measured results. | Analytical report. Understand the job and Establish evidence require synthetic labels and forbid substituting demo/fabricated rows. Explicitly requested templates/mockups allowed with honest labels. |
| ADJ_REPORT_02 | Flag a reported quantity or comparison inconsistent with its source definition, unit, denominator, cohort, period, or grain. | Numeric report claims with trusted rows/definitions. Establish evidence lists each dimension. Do not compare differently sized groups as performance using counts alone when rates are needed. |
| ADJ_REPORT_03 | Flag missing data represented as zero or an unavailable comparison represented as measured change. | Numeric table/narrative. Establish evidence: “Missing values are not zero; missing comparisons are not evidence of change.” Deliberate imputation must be disclosed and appropriate. |
| ADJ_REPORT_04 | Flag percent versus percentage-point wording that changes the magnitude of a rate comparison. | Rate change narrative/chart labels. Establish evidence explicitly requests percentage points for intended rate differences. Both relative percent and absolute point change may be reported when labeled correctly. |
| ADJ_REPORT_05 | Flag a causal/driver claim stronger than the analysis or a quantified explanation that does not reconcile where reconciliation is mathematically required. | Diagnostic report. Establish evidence distinguishes observation/model/causality and within-group/mix changes; requested diagnostics quantify supported explanation. Generic causality disclaimers do not cure a false claim. |
| ADJ_REPORT_06 | Flag an observation, modeled scenario, hypothesis, recommendation, recorded decision, or shipped outcome presented as another status. | Report assertions. Establish evidence and narrative-style distinguish these; actual decisions need source/owner when known. User proposals can be stated directly under an unambiguous heading. |
| ADJ_REPORT_07 | Flag a supported material limitation removed, hidden, or moved away so the visible finding becomes misleading. | Report/summary/visual context. Narrative guidance keeps interpretation-changing qualifications visible beside claims and in exports; no repetitive caveat quota. |
| ADJ_REPORT_08 | Flag a title/headline that overstates causality, certainty, impact, or a proposed decision beyond the report evidence. | Changed report title/finding. Choose composition and narrative-style require strongest supported takeaway without exaggeration. Neutral/question/formal recurring titles allowed. |
| ADJ_REPORT_09 | Flag a complete requested report that fails to answer its governing question at the promised scope or omits evidence necessary to assess its main conclusion. | Full report delivery, not an intermediate artifact honestly identified as unfinished. Verify and deliver asks whether it answers and explains rather than restating numbers. No chart/section/source quotas. |
| ADJ_REPORT_10 | Flag an executive summary that states a material verdict without the available concrete comparison or statistic needed to make it credible. | Multi-finding decision report. executive-report.md and main source call for standalone answer plus supporting numbers. A one-answer brief can use a concise opening; methods reports may lead with necessary method context. |
| ADJ_REPORT_11 | Flag report text that silently invents an owner, deadline, target, commitment, formula, source, or recommendation as an established fact. | Report and action items. Establish evidence and Choose useful next steps explicitly prohibit invention. Unknown ownership may be an open question, not a forced field. |
| ADJ_REPORT_12 | Flag a proposed next task whose stated rationale is unsupported or whose promised result exceeds the evidence/access/prerequisites. | Report recommendation/task link text. Choose useful next steps requires supported unresolved question, meaningful decision, prerequisites, stopping conditions, and narrowed promises. Zero actions is valid. |
| ADJ_REPORT_13 | Flag report source bindings or previews that attribute a claim to unread, wrong-scope, or materially different evidence. | Source-bound report metadata/content observable from trusted artifact. Establish evidence and Build app require exact provenance, scope, and declared query IDs. Do not infer validated analysis from a passing build. |
| ADJ_REPORT_14 | Flag an evidence cutoff, refreshed period, or “as of” date that falsely implies data freshness beyond the supported source cutoff. | Refreshed report. Refresh existing report: set report.asOf to supported evidence cutoff, “not the time the refresh ran.” Formatting a date differently is not a defect. |

Excluded: app framework, component APIs, editable-block IDs, protected shell, preparer script, preview/publication/export workflow, host permissions, task execution, automatic refresh, compact-number typography as an absolute rule, and prescribed Executive Summary labels. The report examples are examples, not validation schemas; no content is required to copy their layouts.

### KPI reporting — 11 candidate checks

Actual guidance: lock the metric contract and actuals first; use authoritative sources; show comparable periods and relevant target/pacing; make status criteria explicit; validate and quantify drivers; distinguish business context from causation; and make the readout useful to operators. The linked template document provides optional patterns only.

| ID | Proposed granular rule | Applicability and evidence |
| --- | --- | --- |
| ADJ_KPI_01 | Flag precise KPI claims without a sufficiently clear definition, source, time window, cutoff, or comparison basis to interpret them. | KPI/WBR/MBR/QBR readout. Lock Definitions and Metric Standards. Trusted recurring definitions can be linked or inherited; do not demand repeated boilerplate every run. |
| ADJ_KPI_02 | Flag a readout presenting placeholders as actuals or claiming completion while core actuals remain unavailable. | Final metric readout; explicit templates/mockups excluded. Pull Topline Actuals says do not draft/render from placeholders and reproduce topline before explanation. |
| ADJ_KPI_03 | Flag incompatible periods/targets/populations or changed metric definitions compared as though directly comparable. | Comparative claim. Metric Standards calls out definition changes, backfills, denominator shifts, calendar effects, outages and missing days. Disclose material breaks rather than fabricate restated history. |
| ADJ_KPI_04 | Flag an “ahead,” “healthy,” “at risk,” R/Y/G, or similar performance status with no stated or trusted governing comparison/target basis. | Status judgment, not a raw value lookup. Status and Pacing Standards pairs color with text and states basis; Presentation replaces generic adjectives with evidence. No absolute requirement to use traffic lights. |
| ADJ_KPI_05 | Flag a deadline-based “on track” claim that ignores known pacing or silently assumes a linear fallback as authoritative. | Target with deadline and pacing judgment. Put Numbers In Context uses provided pacing or explains calculated fallback. Never invent a target to enable this check. |
| ADJ_KPI_06 | Flag current/absolute/relative/target variance values that disagree with their declared actuals and comparison inputs. | Headline KPI comparisons. Pull Actuals and Context request actual and change; arithmetic must match declared meaning. Handle zero baselines and percentage-point distinctions honestly. |
| ADJ_KPI_07 | Flag a plausible business event promoted to an established driver without evidence of timing, affected population and measured change. | KPI movement explanation. Driver Standards explicitly requires these links and separates hypotheses/context from validated drivers. Corroborated prior analysis can suffice. |
| ADJ_KPI_08 | Flag a driver decomposition whose additive contributions fail to reconcile, double count, or imply a causal hierarchy unsupported by metric definitions. | Composite/topline KPI explanation. Define Framework and Driver Standards require supported relationships; additive bridge only where components reconcile. Otherwise state relationship and uncertainty. |
| ADJ_KPI_09 | Flag an operating implication or action asserted beyond the validated driver evidence or known constraints. | KPI recommendation. Add Business Context says recommend only when supported, otherwise next validation step. A large number alone does not establish a problem. |
| ADJ_KPI_10 | Flag unacknowledged authoritative-source conflicts that materially change the reported status, coverage or driver conclusion. | Conflicting KPI sources present in trusted evidence. Source Discovery compares ownership, freshness, definition, grain, coverage, directness and notes material conflicts. More sources are not automatically better. |
| ADJ_KPI_11 | Flag a recurring readout silently omitting an expressly requested metric/section because its definitions, actuals or validation are missing. | Promised recurring scope. Status and Pacing Standards keeps recurring sections consistent and briefly explains missing requested sections. User-narrowed readouts and irrelevant sections may be omitted. |

Excluded: designing the KPI system, selecting a new north star, inventing targets, live driver investigations, automation scheduling, source-integration setup, app delivery, renderer requirements and artifact export. Business benchmark attainment is never itself a content defect. Optional templates are not required report outlines.

## Linked references and read limits

The following five references were read fully, each with no continuation:

| Full URI | Use in this audit |
| --- | --- |
| skill://plugin_connector_1p_4a72ddeef4c481918f92d8e8df18fb2c/write-page/writing_quality.md | Editorial review, heading outline, connected paragraphs, source fidelity, qualification, contextual punctuation/voice. |
| skill://Plugin_fc9843a6fb34819195d6c7802398a8a7/build-report/references/narrative-style.md | Report narrative, accurate titles, evidence context, decision vs recommendation, uncertainty and useful actions. |
| skill://Plugin_fc9843a6fb34819195d6c7802398a8a7/build-report/specifications/executive-report.md | Decision reader flow, evidenced standalone summary, feasible recommendations, optional structures. |
| skill://Plugin_fc9843a6fb34819195d6c7802398a8a7/build-report/specifications/technical-report.md | Definitions, methods, assumptions, experiments/projections, negative results and sensitivity where consequential. |
| skill://Plugin_fc9843a6fb34819195d6c7802398a8a7/kpi-reporting/references/report-templates.md | Optional inline/document/single-slide/business-review/scorecard shapes, not a completeness schema. |

The following linked user resources were attempted with the same package and complete resource identifier, and the reader returned “failed to read skill resource.” The parent SKILL.md mention is evidence of a link's purpose only; it is not evidence of the missing file's detailed contents.

| Full attempted URI | Consequence |
| --- | --- |
| skill://user/6ac92f6d06248191b4437f032adae6ea/launch/references/shipped-changes.md | No extracted code-to-copy implementation rubric. |
| skill://user/6ac92f6d06248191b4437f032adae6ea/launch/references/site-launch-qa.md | No extracted site QA or launch technical checklist. |
| skill://user/6ac92f6d06488191a25a2fe0dbe72483/marketing-plan/references/current-state-rubric.md | Its advertised 17 sections were not audited or recreated. |
| skill://user/6ac92f6d06448191b20abe8f474b5bfb/marketing-loops/references/seo-operator.md | No extracted SEO operator writing-gate details. |
| skill://user/6ac92f6d06448191b20abe8f474b5bfb/marketing-loops/references/outbound-operator.md | No extracted outbound approval/approved-claim details. |
| skill://user/6ac92f6d06088191b214b2492a4bf944/events/references/webinar-funnel.md | No extracted webinar landing/email funnel rubric. |
| skill://user/6ac92f6d06088191b214b2492a4bf944/events/references/speaking.md | No extracted talk/CFP writing rubric. |
| skill://user/6ac92f6d06308191b397c5c5f2744ea5/marketing-council/references/advisors/ann-handley.md | No inferred Handley-specific rules beyond the main skill. |
| skill://user/6ac92f6d06308191b397c5c5f2744ea5/marketing-council/references/advisors/david-ogilvy.md | No inferred Ogilvy-specific rules beyond the main skill. |
| skill://user/6ac92f6d06a481919c3032b7e5322a62/referrals/references/affiliate-operations.md | No extracted detailed executable affiliate terms rubric. |
| skill://user/6ac92f6d06a481919c3032b7e5322a62/referrals/references/review-programs.md | No extracted detailed review-request/response rubric. |
| skill://user/6ac92f6d06a481919c3032b7e5322a62/referrals/references/review-platform-rules.md | No platform-specific incentive or automation claims. |
| skill://user/6ac92f6d05a48191877b7a1bc46c738b/churn-prevention/references/cancel-flow-patterns.md | No provider/industry-specific cancel-copy rules. |
| skill://user/6ac92f6d05a48191877b7a1bc46c738b/churn-prevention/references/dunning-playbook.md | No provider-specific dunning setup or copy rules. |
| skill://user/6ac92f6d06948191bd8207fff83c6a23/prospecting/references/account-research.md | No extracted agent-research brief rubric. |
| skill://user/6ac92f6d06948191bd8207fff83c6a23/prospecting/references/demand-signals.md | No extracted 0–100 demand-fit scoring details. |

Shared Data links ../../shared/analysis-quality.md and ../../shared/shared-skill-instructions.md were attempted using both linked relative resource forms and plugin-root shared resource forms. All returned the same read failure. A targeted filesystem search under /workspace/shared and /opt/codex/marketplaces found no installed copies. This audit therefore uses only the accessible main-source restatements of analytical quality and source judgment. Native tool request reference files were not read because this is a content-rule audit and they concern request composition or provider controls, not writing judgment.

## Canonical consolidation and artifact routing

The source IDs preserve audit lineage. They need not become separate product checks when they express the same defect. Use the following consolidation map when building focused bundled skills; each row describes one narrow review job. The listed source skills are provenance seeds for extracting that focused bundle, not a request to send whole source skills together to Haiku. A rule can inform more than one route, but one defect should produce one finding.

| Actual changed artifact | Focused review job | Source rules to consolidate | Routing limit |
| --- | --- | --- | --- |
| Launch announcement, changelog, release note | Shipped-state and scope accuracy | ADJ_LAUNCH_01, 04, 05; ADJ_REPORT_06 | Require trusted release/product status; no launch-readiness or channel checklist. |
| Launch/early-access page | Audience value and actionable invitation | ADJ_LAUNCH_02, 03; ADJ_PAGE_02 | Only complete invitation/page scope; no mandatory GA or signup model. |
| Partner pitch or better-together page | Specific joint proposal and accurate combined capabilities | ADJ_CO_01–03; ADJ_IDEA_01 | Distinguish unsupported facts from strategic disagreement. |
| Co-marketing agreement or complete brief | Material responsibility and terms clarity | ADJ_CO_04 | Only requested agreement scope; no legal-compliance certification. |
| Community welcome, guidelines, advocate brief | Member benefit, first action, participation clarity | ADJ_COMM_01–04 | Do not impose community size, platform, rituals, or health targets. |
| Event invitation or meeting outreach | Audience promise and understandable ask | ADJ_EVT_01, 02 | Event strategy and format choices stay outside the check. |
| Event follow-up or repurposed transcript | Genuine personalization and quotation fidelity | ADJ_EVT_03, 06; ADJ_PAGE_03–05 | Require actual notes/recording evidence for factual findings. |
| Simulated marketing council | Named-person attribution and simulation grounding | ADJ_COUNCIL_01–05, 08 | No generic celebrity voice or unsupported invented quotes; ordinary sourced discussion does not trigger simulation disclosure. |
| Multi-advisor council synthesis | Substantive tradeoff and internal position fidelity | ADJ_COUNCIL_06, 07 | No forced dissenter requirement for unrelated copy or single-advisor output. |
| Actionable marketing idea or plan | Context, assumptions, feasible next action | ADJ_IDEA_01–03; ADJ_PLAN_01–04, 07 | Actual constraints and promised execution detail matter; channel preference and budgets do not define failure. |
| Comprehensive plan | Promised scope and reference accuracy | ADJ_PLAN_05, 06 | No automatic 13-section/139-idea/word-count requirement unless specifically requested or promised. |
| Marketing-loop specification or promotional description | Check-versus-act clarity and honest automation scope | ADJ_LOOP_01–04 | Only written contract/capability claims; no permission or scheduler execution in ContentGuard. |
| Referral/affiliate offer, invitation, terms | Reward, relationship, eligibility and action consistency | ADJ_REF_01–04 | Evaluate actual program terms; do not require one reward model or sizing rule. |
| Customer endorsement/testimonial | Source and attribution fidelity | ADJ_REF_05; ADJ_EVT_06; ADJ_PAGE_05 | No presumption that missing repository consent proves lack of permission. |
| Cancellation confirmation or save/pause/downgrade flow | Status, continuation, savings and material consequence clarity | ADJ_CHURN_01–06 | UI visibility requires native/rendered evidence; actual billing terms govern. |
| Dunning email | Accurate consequence and usable recovery action | ADJ_CHURN_03, 07, 08 | Do not impose the source's sample recovery schedule. |
| Written tracking/lifecycle/routing specification | Consistent, complete declared contract | ADJ_ANALYTICS_01–04; ADJ_REV_01, 02 | Activate only for implementation-ready prose/specs; provider implementation review is separate. |
| Prospect list or account brief | Evidence lineage and honest qualification/confidence | ADJ_PROS_01–06 | No live email checks, list acquisition, or sending. Branch-specific scoring must match the artifact. |
| Page/Doc report or template revision | Meaning-preserving source and edit fidelity | ADJ_PAGE_01–09; ADJ_GDOC_01–03 | Preserve explicit user style and formatting-only scope; no native provider defaults on generic prose. |
| Native Doc body | Provider citation leakage | ADJ_GDOC_04 | This is a concrete content-format issue only for native Docs. |
| Native Slides/template or safely supplied export | Stale content, media meaning, native text/list and legibility | ADJ_GSLIDE_01–09 | Text-only diffs do not prove geometry, clipping, media distortion, or rasterization. |
| Attribution/event/channel performance readout | Unique outcomes, allocation basis, model and certainty | ADJ_ATTR_01–09; ADJ_EVT_04, 05 | Event exposure is a valid measure; it must not be relabeled qualified pipeline or causal revenue. |
| Analytical report, KPI or revenue dashboard narrative | Definition, number, period, grain and freshness fidelity | ADJ_REPORT_01–04, 14; ADJ_KPI_01–03, 06; ADJ_REV_03 | Trusted definitions/evidence control; missingness is not zero; targets must not be invented. |
| Diagnostic report/KPI driver section | Inference, decomposition and evidence strength | ADJ_REPORT_05–07; ADJ_KPI_07, 08, 10 | Correlation, business context and modeled allocation do not automatically establish causes. |
| Decision report, KPI status and summary | Supported title/status, useful answer and action | ADJ_REPORT_08–12; ADJ_KPI_04, 05, 09, 11 | No imposed executive layout, chart quota, action quota, R/Y/G use, or target benchmark. |
| Source-linked report metadata/previews | Exact evidence scope and honest source basis | ADJ_REPORT_13; ADJ_ATTR_09; ADJ_PAGE_05 | A citation or successful build is not proof the claim is supported. |

Deduplicate on the changed span or omission, underlying factual/reader problem, and canonical job. For example, a false cancellation date is one terms/status finding even if PAGE, CHURN and REPORT source-fidelity rules all apply; an event report's double-counted conversions is one attribution-count finding even if KPI arithmetic also catches it. Keep all useful source IDs in lineage, but pass Haiku only the focused bundle for that finding. Distinct defects in the same sentence, such as false reward amount and inaccessible ambiguous link text, may remain separate if independently evidenced.

## Coverage and implementation cautions

- Covered: 19 of 19 assigned main skills; five concrete linked writing/report references; 123 proposed granular rules.
- These are source-backed candidates for focused check bundles, not 123 unconditional model calls. Most route to existing factual claims, clarity, audience/intent, conversion-copy, source fidelity, or accessible presentation checks.
- Analytics and RevOps are primarily operations skills with a narrow written-specification contribution. Loops, launch, events, community, referral and prospecting include substantial operations guidance; only their visible artifact obligations were retained.
- No business metric target, recommended channel, growth framework, budget allocation, preferred format, word count, advisor viewpoint, or exact sample sequence is a default failure condition.
- No tests, product code changes, remote writes, source-data updates, outbound messages, or publication were performed for this audit. No additional agents were spawned.
