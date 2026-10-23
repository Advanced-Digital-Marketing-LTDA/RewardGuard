# ContentGuard conversion and landing page source audit

Audit date: 2026-10-23. Scope: 15 requested conversion, offer, pricing, signup, onboarding, popup, experiment, bootstrap, and Sites skills. This is source research for RewardGuard ContentGuard; no setup, redesign, publishing, remote mutation, implementation, or test workflow was run.

## Coverage and interpretation

The cloud catalog was discovered with every page of `skills__list({authority:{kind:'cloud'}})`: 7 pages, 124 catalog entries. All 15 assigned SKILL.md documents were read completely, with no remaining read cursors (149,841 characters). Forty linked resource reads were attempted. The Sites presentation reference was accessible; 39 linked user skill references returned `failed to read skill resource`. An alternate resource path also failed. Unavailable references are listed per skill; their descriptions in a main document are usable evidence, but their unseen detailed rubrics are not represented as inspected source.

The rules below operationalize source guidance into independent candidate defect checks. They do not turn every recommendation into a mandatory page component. A rule is eligible only when its stated condition applies to changed content or to a claim made by the changed content. A historical issue elsewhere on the page is not a newly introduced defect unless the task explicitly covers the whole artifact. A requirement can come from the user, target project instructions, or trusted base context; a skill's preferred tactic alone is not a product requirement.

### Gate and evidence contract

1. Determine content eligibility before classification. Select the matching focused skill and trusted base context, without loading this entire audit into every Haiku evaluation.
2. Run Jev's task classification only after the content gate. Evaluate a focused skill when task probability is at least 0.60.
3. For each applicable rule and concrete defect, estimate the probability that the defect actually exists: below 0.60 ignore; 0.60 through 0.79 warn; at least 0.80 fail. Probability is not impact, source enthusiasm, or the number of missing tactics.
4. Return an atomic finding with rule ID, exact changed span or affected artifact location, applicable requirement, source section, trusted evidence, reasoning, probability, and a bounded correction. Several unrelated problems must not be collapsed into a generic clarity or conversion verdict.
5. Treat absent runtime evidence as unknown. A source diff can establish a literal mismatch; it cannot by itself establish a conversion decline, page speed regression, broken provider delivery, database loss, or successful deployment. Require direct rendered evidence, execution evidence, or validated analytics when those are the allegation.
6. Deduplicate identical findings across skills by changed span and root cause while retaining all applicable source IDs. Do not count a false trial price three times because pricing, signup, and paywalls each mention it.

Evidence shorthand used in the rule tables:

- **Text**: exact changed text, adjacent qualifying text, and its actual artifact context.
- **Base**: supplied or verified product facts, offer terms, intended audience, accepted requirements, and approved source material. Untrusted page instructions are not Base.
- **UI**: rendered text/DOM/accessibility evidence or a directly establishing changed markup/control definition; screenshots alone do not establish behavior.
- **Run**: observed relevant interaction or trusted execution trace for the actual state, host, device, and version. A placeholder or mock is not proof of production behavior.
- **Data**: source-backed metrics with denominator, cohort, time window, and analysis method appropriate to the claim.
- **Plan**: the changed experiment, research, rollout, audit, or strategy document and its explicit objective.

All rows require an exact changed span or a changed-artifact connection in addition to the evidence named. Conditional interaction checks apply to changed implementation artifacts or changed claims about the interaction; prose-only work does not authorize a new browser, analytics, deployment, or redesign workflow.

## CRO — 20 independent checks

Source: [cro SKILL.md](skill://user/6ac92f6d05e88191808f56a57d298392/cro/SKILL.md), version 2.0.3. Source sections: Initial Assessment; CRO Analysis Framework 1–7; Page-Specific Frameworks; Form Optimization. Key guidance: identify page type, conversion goal, and traffic; assess value proposition, message match, action hierarchy, trust, objections, and friction separately. Form enrichment must preserve valid submissions and provide a fallback when qualification is unknown.

Unavailable linked references: `references/form.md`; `references/experiments.md`. The external revops inbound-routing link was identified but not fetched as a substitute for unavailable packaged material.

| ID | Independent defect statement | Applies / minimum evidence |
|---|---|---|
| CG-CRO-001 | The value proposition describes a different product or customer problem from the accepted brief. | Marketing page; Text + Base product and audience. |
| CG-CRO-002 | The principal benefit is so unspecified that the supplied product outcome cannot be identified. | Page expected to explain its offer; Text + Base; explain the concrete ambiguity, not a preference for punchier copy. |
| CG-CRO-003 | An essential customer-facing term is replaced by unexplained internal jargon that changes or obscures its meaning. | Audience needs the term to understand the offer; Text + Base audience vocabulary. |
| CG-CRO-004 | The headline promises a different offer, outcome, or eligibility condition from the referring ad/email. | A traffic source is supplied; Text + Base exact source message. |
| CG-CRO-005 | The headline contradicts the page's own substantive offer details. | Any marketing headline; Text from headline and relevant details. |
| CG-CRO-006 | A numeric headline or result lacks support while being presented as a real verified outcome. | Real quantitative claim, not marked example; Text + Base/Data provenance. |
| CG-CRO-007 | CTA wording promises an action different from the destination's actual next step. | Changed CTA/destination; Text + Base or Run showing actual step. |
| CG-CRO-008 | Equally emphasized actions leave the user unable to identify the explicitly required primary conversion. | A primary action is established; UI + Base requirement; mere presence of two buttons is insufficient. |
| CG-CRO-009 | The required conversion action has no operable path from the changed page. | Page task requires this action; UI/Run + Base destination. |
| CG-CRO-010 | CTA microcopy omits a known material commitment, making a paid or sales step look like an immediate free resource. | Such a commitment exists; Text + Base flow/terms. |
| CG-CRO-011 | Critical offer information is visually unreadable or obscured in the rendered layout. | Changed presentation; UI at the affected viewport. |
| CG-CRO-012 | An image or caption represents an illustrative example as an actual product result or customer artifact. | Real-result implication; Text/UI + Base asset provenance. |
| CG-CRO-013 | A testimonial is invented, misattributed, or materially altered from its authorized source. | Testimonial introduced/changed; Text + Base source quote/permission. |
| CG-CRO-014 | A customer logo or named customer relationship is asserted without the actual relationship represented. | Real customer endorsement implication; Text/UI + Base. |
| CG-CRO-015 | Review counts or ratings disagree with the cited source or omit a qualification needed to interpret the value. | Real review proof; Text + Base/Data source/date. |
| CG-CRO-016 | A security or trust badge implies a certification or coverage that the product does not hold. | Badge/claim introduced; UI/Text + Base certification scope. |
| CG-CRO-017 | The answer to a material purchase objection contradicts the approved price, implementation process, or guarantee. | FAQ/process/objection copy; Text + Base terms. |
| CG-CRO-018 | The next-step description is materially false about what follows the conversion. | Signup/demo/contact/download action; Text + Base/Run next step. |
| CG-CRO-019 | A valid lead submission is described as rejected solely because enrichment timed out or qualification is unknown. | Enrichment influences routing; Text + Base flow or Run rejection trace. |
| CG-CRO-020 | A conversion or load-time improvement is stated as measured without relevant measurement evidence. | Performance/impact claim; Text + Data/Run appropriate to the claim. |

Advisory tactics: one CTA above the fold, repeated CTAs, removing navigation, benefit-first headlines, adding FAQ/logos/photos, whitespace, shorter forms, and a recommended pricing tier are hypotheses or design preferences unless the brief requires them. Their absence alone cannot fail.

## Offers — 20 independent checks

Source: [offers SKILL.md](skill://user/6ac92f6d06588191879719e67d61295d/offers/SKILL.md), version 1.0.1. Source sections: Value Equation; Anatomy of a Complete Offer; Diagnostic Loop; When NOT to Use Offer-Design Tactics; Banned Vocabulary. Key guidance: specify the actual deliverable and terms, ground proof, use genuine scarcity, avoid inflated bonuses and undefined guarantees. The value equation is a planning model, not a measurable law.

Unavailable linked references: `references/value-equation.md`, `offer-anatomy.md`, `guarantee-design.md`, `bonus-stacking.md`, `scarcity-urgency.md`, `offer-formats.md`, `saas-offers.md`, `examples.md` (all paths under `references/`).

| ID | Independent defect statement | Applies / minimum evidence |
|---|---|---|
| CG-OFF-001 | The advertised core deliverable differs from the approved scope. | Offer description; Text + Base deliverables. |
| CG-OFF-002 | A concrete promised outcome exceeds what the product/service can actually supply. | Outcome claim; Text + Base capability and prerequisites. |
| CG-OFF-003 | A promised result timeline conflicts with the real delivery or customer dependency timeline. | Time-to-result claim; Text + Base timeline. |
| CG-OFF-004 | The offer conceals material customer work while promising a done-for-you or effortless result. | Effort-reduction claim; Text + Base required customer actions. |
| CG-OFF-005 | Methodology details are fabricated to imply an established delivery process. | Named process/method claim; Text + Base actual method. |
| CG-OFF-006 | A case study is applied as proof for a materially different audience or outcome without its limiting context. | Proof introduced as representative; Text + Base case population/outcome. |
| CG-OFF-007 | A bonus is described as included when it is unavailable or separately chargeable. | Bonus stack present; Text + Base entitlement/availability. |
| CG-OFF-008 | A bonus description promises content or service absent from the actual bonus. | Specific bonus promise; Text + Base bonus artifact. |
| CG-OFF-009 | A stated bonus dollar value has no relevant comparable or bona fide basis. | Real “worth/value $X” assertion; Text + Base valuation source. |
| CG-OFF-010 | The total value stack double counts the same deliverable or misadds component values. | Quantified stack; Text + Base component list and arithmetic. |
| CG-OFF-011 | A guarantee omits a material eligibility condition while implying unconditional coverage. | Guarantee claim; Text + Base exact terms. |
| CG-OFF-012 | The guarantee's remedy differs from the approved refund, service credit, or extra-work remedy. | Guarantee remedy; Text + Base. |
| CG-OFF-013 | The guarantee's deadline conflicts with the actual claim window. | Guarantee period; Text + Base dates/window. |
| CG-OFF-014 | A “100% guaranteed” statement does not specify what is guaranteed or the governing conditions. | Such absolute guarantee wording; Text + surrounding/linked real terms. |
| CG-OFF-015 | A scarcity statement asserts an untrue capacity, stock, or enrollment limit. | Scarcity used; Text + Base inventory/capacity. |
| CG-OFF-016 | An urgency statement gives an untrue deadline or uses “limited time” without a real time limit. | Urgency used; Text + Base schedule. |
| CG-OFF-017 | A countdown implies a real closing deadline but resets or continues selling on the same terms after expiration. | Timer exists; UI/Run across the actual deadline + Base campaign rules. |
| CG-OFF-018 | A payment plan hides an installment, financing charge, or total commitment that changes the advertised price. | Installment offer; Text + Base full payment schedule. |
| CG-OFF-019 | The offer name implies a service level or deliverable that the listed package does not include. | Name carries a specific factual implication; Text + Base package. |
| CG-OFF-020 | A predicted conversion lift or discount/churn relationship is presented as proven for this business using only generic skill heuristics. | Quantitative forecast/result claim; Text + relevant Data; source examples are not customer evidence. |

Advisory tactics: six-part offer anatomy, bonus stacks, guarantees, scarcity, one-lever iterations, prohibiting all acquisition discounts, and preferred vocabulary are not universal business requirements. Do not fail an honest offer for having no countdown, no bonus, or no guarantee. Skill claims such as “10–40% lift,” “2–3x,” and “discount askers churn at ~2x” require original evidence before reuse as empirical promises.

## Pricing — 28 independent checks

Source: [pricing SKILL.md](skill://user/6ac92f6d067c8191b52695d83fd028ec/pricing/SKILL.md), version 2.1.3. Source sections: Three Pricing Axes; Value Metrics; Tier Structure; Pricing Research; Price Increase Rollout; Pricing Page Best Practices; Pricing Page Teardown. Key guidance: distinguish package, billing metric, and amount; state differentiators and terms; make claimed prices extractable; interpret willingness-to-pay research correctly. The main source names a ten-dimension teardown, but the detailed rubric was unavailable and is not reconstructed here.

Unavailable linked references: `references/pricing-models.md`, `references/tier-structure.md`, `references/research-methods.md`, `references/pricing-page-teardown.md`.

| ID | Independent defect statement | Applies / minimum evidence |
|---|---|---|
| CG-PRI-001 | The displayed amount differs from the approved price for the stated plan/cohort. | Public or in-product pricing; Text + Base price registry. |
| CG-PRI-002 | Currency is omitted or mislabeled where it materially changes the quoted amount. | Ambiguous/multiple-currency offer; Text + Base market/currency. |
| CG-PRI-003 | The price's billing period is wrong or ambiguous about the actual payment interval. | Recurring price; Text + Base billing period. |
| CG-PRI-004 | An annual amount is presented as a monthly payment without stating that annual payment is required. | Monthly-equivalent annual display; Text + Base charge schedule. |
| CG-PRI-005 | The monthly/annual selector's labels disagree with the displayed prices or active selection. | Selector changed; UI/Run + Base amounts. |
| CG-PRI-006 | An annual discount is arithmetically inconsistent with the comparable monthly and annual totals. | Discount shown; Text + Base comparable totals; distinguish percent from currency savings. |
| CG-PRI-007 | A required setup, base, minimum, or recurring add-on charge is omitted from an apparently complete price. | Mandatory charge exists; Text + Base fees. |
| CG-PRI-008 | A per-seat charge conceals a required minimum number of paid seats. | Seat billing/minimum exists; Text + Base. |
| CG-PRI-009 | The billing unit is undefined or differs from the approved metric. | Usage, seat, contact, credit, transaction, or outcome pricing; Text + Base unit. |
| CG-PRI-010 | Usage reset periods or included quotas are misstated. | Usage allowance shown; Text + Base allowance/reset terms. |
| CG-PRI-011 | Overage pricing is wrong or omitted while copy promises that the displayed fee covers all usage. | Overage exists and total-fee claim made; Text + Base. |
| CG-PRI-012 | “Unlimited” conceals an actual relevant cap or exclusion. | Unlimited claim; Text + Base limits and fair-use terms. |
| CG-PRI-013 | A feature is assigned to a plan that does not include it. | Tier feature statement; Text + Base entitlements. |
| CG-PRI-014 | A plan's support level or service commitment is overstated. | Support/SLA differentiator; Text + Base commitment. |
| CG-PRI-015 | A plan's stated target audience contradicts a mandatory eligibility restriction. | Audience or eligibility claim; Text + Base. |
| CG-PRI-016 | Identically named tiers are described with conflicting prices or inclusions on the same changed artifact. | Multiple plan representations; Text + matching tier/cohort context. |
| CG-PRI-017 | A “free” plan/trial requires an undisclosed payment or billing commitment. | Free/trial claim; Text + Base terms. |
| CG-PRI-018 | Trial duration or included access differs from approved trial terms. | Trial description; Text + Base. |
| CG-PRI-019 | The CTA's promised signup/purchase action actually opens a sales qualification step without disclosure. | Specific immediate-access promise; Text + Base/Run destination. |
| CG-PRI-020 | Cancellation, refund, or guarantee FAQ answers contradict the governing policy. | Terms/FAQ changed; Text + Base policy. |
| CG-PRI-021 | A public fixed price is published only inside an image where a text-extractability requirement applies. | Fixed prices + explicit AI-readability/accessibility scope; UI/source extraction evidence + Base scope. |
| CG-PRI-022 | A text/structured-data plan price conflicts with the visible plan price. | Both representations exist; Text/UI plus actual machine representation. |
| CG-PRI-023 | Per-tier feature differences are inaccessible to the extraction method claimed to support them. | Explicit extractability claim/requirement; actual extracted text/DOM evidence. |
| CG-PRI-024 | A one-agent paste test is described as proof that all AI agents can or cannot read the page. | AI-readiness report; Plan + exact test scope. |
| CG-PRI-025 | Van Westendorp's “optimal price” intersection is asserted to maximize actual revenue or profit. | Research interpretation; Plan/Data; the four survey questions do not prove this. |
| CG-PRI-026 | Willingness-to-pay survey answers alone are used as a measured conversion, churn, or demand forecast. | Research/forecast artifact; Plan + actual method/Data. |
| CG-PRI-027 | A price increase notice misstates the affected cohort, effective date, or grandfathering rule. | Each alleged term should yield its own finding; Text + Base rollout terms. |
| CG-PRI-028 | A pricing rollout is reported as validated despite missing the cohort, conversion, churn, or support evidence required by its own plan. | Rollout result/approval claim; Plan + Data for the claimed validation. |

Advisory tactics: three tiers, good/better/best, 2–3x premium spacing, $10/$100/$1,000 starting prices, round versus charm prices, annual discounts of 17–20%, prominent recommended tiers, monthly/annual toggles, customer logos, enterprise tiers, and Product/Offer schema are not unconditional failures. A legitimate sales-led “Contact us” price is not an error solely because a self-serve machine-readable number would be easier to compare. Schema checks need the separate schema skill's applicability rules.

## Signup — 24 independent checks

Source: [signup SKILL.md](skill://user/6ac92f6d06c88191b731160f2e93814a/signup/SKILL.md), version 2.0.1. Source sections: Core Principles; Field-by-Field Optimization; Multi-Step Best Practices; Trust and Friction Reduction; Mobile Signup; Post-Submit; Enrichment and Sales-Assisted Routing. Key guidance: only demand genuinely necessary data, disclose commitments, retain usable labels and entered values, give specific recoverable errors, and explain verification. No packaged linked reference; the external inbound-routing playbook was identified but not fetched.

| ID | Independent defect statement | Applies / minimum evidence |
|---|---|---|
| CG-SIG-001 | Signup copy misidentifies the account, trial, paid, or waitlist action being taken. | Signup flow; Text + Base flow type. |
| CG-SIG-002 | A required field is presented as optional, or an optional field is presented as required. | Form field semantics; Text/UI + Base or Run actual validation. |
| CG-SIG-003 | A new required field violates an explicit data-minimization or accepted field-set requirement. | Such requirement exists; UI + Base; no generic “every field hurts” failure. |
| CG-SIG-004 | An essential required phone field lacks the explanation promised by the approved flow. | Phone required and explanation part of task; Text/UI + Base. |
| CG-SIG-005 | Field labels disappear during entry and leave the field's purpose unidentified. | Placeholder-only field; UI/accessibility evidence showing absent usable label. |
| CG-SIG-006 | Password requirements are concealed until rejection despite the changed flow claiming they are shown upfront. | Password requirement/claim; Text/UI/Run + Base actual rules. |
| CG-SIG-007 | Displayed password requirements differ from the actual accepted password rules. | Password guidance; Text + Base or Run validation. |
| CG-SIG-008 | Password paste is blocked in the changed signup field. | Password field implementation; direct event evidence or Run. |
| CG-SIG-009 | A show-password control is mislabeled about its state or fails to perform its advertised action. | Toggle present; UI/Run state transition. |
| CG-SIG-010 | A social sign-in label represents signup to the wrong identity provider or account context. | Auth option changed; Text + Base provider or Run action. |
| CG-SIG-011 | Country-code or input formatting rejects a supported phone format while claiming broad support. | Phone support claim/requirement; Base supported locale + Run. |
| CG-SIG-012 | A multi-step progress indicator gives a false step count or completion state. | Indicator exists; UI/Run against actual required path. |
| CG-SIG-013 | The flow advertises reversible steps but back navigation loses entered values or cannot return. | Back/save promise or explicit requirement; Text + Run. |
| CG-SIG-014 | A declared saved signup state is lost on refresh or resume. | Save/resume promise or requirement; Text + Run same user/state. |
| CG-SIG-015 | Error text does not identify the actual invalid field or gives a correction that cannot resolve it. | Validation failure; Text + Run + Base validation rule. |
| CG-SIG-016 | Duplicate-account messaging supplies no usable recovery path despite an explicit recovery requirement. | Existing-account branch; UI/Run + Base requirement. |
| CG-SIG-017 | A failed submission clears valid entered values contrary to the accepted recovery behavior. | Error recovery changed; Run + Base requirement; do not infer from absence of client code alone. |
| CG-SIG-018 | A “no credit card required” statement is false. | Claim present; Text + Base/Run actual billing requirement. |
| CG-SIG-019 | A “free forever” or trial-duration statement conflicts with the actual access term. | Claim present; Text + Base. |
| CG-SIG-020 | A privacy assurance such as “never share” conflicts with the approved actual data use. | Privacy promise; Text + Base data-use policy. |
| CG-SIG-021 | Touch targets or input keyboards violate an explicit supported mobile/accessibility requirement. | Changed mobile fields/controls; UI or device evidence + Base standard; source's 44px is guidance unless adopted. |
| CG-SIG-022 | Success copy announces an account before the account creation action has actually succeeded. | Success state; Text + Run actual outcome. |
| CG-SIG-023 | Verification instructions direct users to a nonexistent or wrong resend, change-email, or continuation action. | Verification required; Text/UI + Base/Run supported actions. |
| CG-SIG-024 | Unknown/timed-out company enrichment is treated as implicit account rejection. | Enriched sales-assist flow; Base policy + Run or an explicit inaccurate statement. |

Advisory tactics: email-only forms, full-name rather than split-name, social auth prominence, passwordless auth, delayed verification, progress bars, single-column forms, sticky CTAs, prefilled inputs, and precise step counts are context-dependent. A security/compliance requirement can justify additional fields or verification. Do not remove it to satisfy generic conversion guidance.

## Onboarding — 20 independent checks

Source: [onboarding SKILL.md](skill://user/6ac92f6d06648191b89c264a0d981b73/onboarding/SKILL.md), version 2.0.1. Source sections: Core Principles; Onboarding Psychology; Toolkit; Defining Activation; Flow Design; Multi-Channel; Stalled Users; Measurement. Key guidance: minimum path to actual value, a clear first action, usable empty states, honest progress, dismissible optional tours, and behavior-coordinated messaging.

Unavailable linked references: `references/minimum-path-to-value.md`, `references/activation-models.md`, `references/experiments.md`.

| ID | Independent defect statement | Applies / minimum evidence |
|---|---|---|
| CG-ONB-001 | The stated activation event is different from the approved user-value milestone. | Onboarding plan/copy; Plan/Text + Base activation definition. |
| CG-ONB-002 | A retention/activation correlation is asserted without cohort evidence. | Empirical “aha moment” claim; Text/Plan + Data. |
| CG-ONB-003 | A first-run instruction directs a user to an unavailable feature or action. | New-user state; Text + UI/Run entitlement and state. |
| CG-ONB-004 | A mandatory setup step is described as optional, or vice versa. | Checklist/wizard step; Text + Base actual dependencies. |
| CG-ONB-005 | The onboarding path contradicts the product's actual free/trial/paid/consultation model. | Model-dependent flow; Text/Plan + Base access model. |
| CG-ONB-006 | A declared first-value result requires an undisclosed prerequisite. | “Get value now” claim; Text + Base prerequisite. |
| CG-ONB-007 | A checklist marks work complete that has not actually been completed. | Progress display; UI/Run + Base step definition; genuine precompleted work is allowed. |
| CG-ONB-008 | Completion percentages or item counts disagree with the required steps. | Quantified progress; UI/Run + Base denominator. |
| CG-ONB-009 | An empty-state explanation describes a different feature or data type from that screen. | Empty state; Text/UI + Base screen purpose. |
| CG-ONB-010 | An empty-state first-action CTA has no usable path to creating the promised first item. | First-item action; Text + UI/Run. |
| CG-ONB-011 | Example/demo data is represented as the user's actual data or actual achieved outcome. | Seeded content shown; UI/Text + Base provenance. |
| CG-ONB-012 | A tutorial labeled optional or skippable cannot be dismissed. | Tour/guide exists; Text + Run dismissal. |
| CG-ONB-013 | Dismissed onboarding guidance repeats contrary to an explicit remembered-dismissal requirement. | Persistence requirement exists; Base + Run returning state. |
| CG-ONB-014 | A “setup complete” celebration is emitted while a required setup action has failed. | Completion state; Text/UI + Run required action outcome. |
| CG-ONB-015 | A triggered reminder falsely tells users to complete an action they already completed. | Behavior-triggered message; Text + Base trigger + Run/Data user state. |
| CG-ONB-016 | An onboarding email CTA deep-links to the wrong step, inaccessible state, or wrong product context. | Email/in-app coordination; Text + Base/Run destination. |
| CG-ONB-017 | A reentry message promises continuation but routes the user to an unrecoverable or reset state. | Resume promise; Text + Run same user state. |
| CG-ONB-018 | Time-to-value or completion-rate results use a different event denominator from the declared activation definition. | Measurement/report artifact; Plan + Data. |
| CG-ONB-019 | Signup volume is reported as demonstrated activation or retention. | Success report; Text + Data definitions and follow-up window. |
| CG-ONB-020 | Generic progress/abandonment benchmarks are presented as measured product-specific effects. | Quantitative psychology/impact claim; Text + actual Data, not source anecdotes. |

Advisory tactics: one goal per session, 3–7 checklist items, 3–5 tour steps, demo data, celebration, calls, videos, and a particular email schedule are optional. Do not invent positive progress to imitate an endowed-progress effect. The source's “roughly +40% completion” and linked abandonment figures require original evidence before publication as empirical claims.

## Paywalls — 22 independent checks

Source: [paywalls SKILL.md](skill://user/6ac92f6d066c81919088c1b326b82a02/paywalls/SKILL.md), version 2.0.0. Source sections: Core Principles; Trigger Points; Screen Components; Specific Types; Timing/Frequency; Upgrade Flow; Anti-Patterns. Key guidance: explain the actual gate and paid value, provide transparent pricing and a clear alternative where free use remains available, respect dismissal, and confirm real access after purchase.

Unavailable linked reference: `references/experiments.md`.

| ID | Independent defect statement | Applies / minimum evidence |
|---|---|---|
| CG-PAY-001 | The upgrade screen identifies the wrong current plan. | Existing-user paywall; Text/UI + Base/Run account plan. |
| CG-PAY-002 | The stated gated feature is not actually restricted to the advertised plan. | Feature-lock explanation; Text + Base entitlement. |
| CG-PAY-003 | The paid feature preview promises capability not included in the offered upgrade. | Preview/value demonstration; Text/UI + Base capability. |
| CG-PAY-004 | The displayed usage-limit threshold differs from the actual allowance. | Limit prompt; Text/UI + Base quota. |
| CG-PAY-005 | The displayed usage count differs from the user's actual counted usage. | Personalized limit/progress display; Run/Data same state. |
| CG-PAY-006 | The proposed upgrade fails to resolve the limit or feature restriction it promises to resolve. | Unlock promise; Text + Base entitlement or Run. |
| CG-PAY-007 | A trial-expiration date or remaining-day count is wrong for that account. | Personalized trial notice; Text/UI + Base/Run trial clock. |
| CG-PAY-008 | The described post-expiration access differs from the real policy. | Expiration notice; Text + Base. |
| CG-PAY-009 | The screen falsely states that user data will be lost to pressure an upgrade. | Data-loss statement; Text + Base lifecycle. |
| CG-PAY-010 | A usage/value summary attributes actions or results to the user that did not occur. | Personalized accomplishments; UI/Text + Data. |
| CG-PAY-011 | The upgrade price differs from the selected plan's actual charge. | Purchase-facing amount; Text + Base/Run pricing. |
| CG-PAY-012 | Recurring period or annual prepayment is obscured by a misleading per-month amount. | Subscription upgrade; Text + Base billing. |
| CG-PAY-013 | The upgrade CTA promises an immediate unlock but instead adds an undisclosed approval/qualification step. | Immediate-access promise; Text + Base/Run flow. |
| CG-PAY-014 | A prompt obscures or disables its close control while free continuation is an available supported action. | Dismissible upgrade prompt; UI/Run + Base free path. |
| CG-PAY-015 | “Continue free,” “not now,” or downgrade control initiates purchase or a materially different action. | Alternative control exists; Text + Run action. |
| CG-PAY-016 | Decline wording shames or deceptively characterizes the user's choice. | Actual manipulative decline copy; Text; quote the wording, not inferred intent. |
| CG-PAY-017 | A paywall blocks a critical flow that the accepted access policy permits. | Critical permitted action; Base entitlement/flow + Run. |
| CG-PAY-018 | A prompt repeats immediately after dismissal despite an explicit cooldown rule. | Rule established; Base + Run same visitor/session. |
| CG-PAY-019 | Post-upgrade copy announces successful payment or access before the payment outcome is known. | Success state; Text + Run payment result. |
| CG-PAY-020 | A successful upgrade fails to grant the specific access promised as immediate. | Real successful payment; Base promise + Run entitlement state; mocks insufficient. |
| CG-PAY-021 | Confirmation or receipt text gives a different plan/charge than the completed transaction. | Receipt/confirmation artifact; Text + Base/Run transaction. |
| CG-PAY-022 | An experiment success claim ignores measured post-upgrade churn or revenue guardrails required by its own plan. | Upgrade analysis/report; Plan + Data guardrails. |

Advisory tactics: value-before-ask timing, previews, seven screen components, annual/monthly options, specific 7/3/1-day warnings, and multi-day cooldowns are optimization choices unless adopted. A hard paywall for a genuinely paid-only entitlement need not invent a free path. Respect-no checks apply to the actual access model and supported alternatives.

## Popups — 26 independent checks

Source: [popups SKILL.md](skill://user/6ac92f6d06748191a3384d8ca4875940/popups/SKILL.md), version 2.0.0. Source sections: Triggers; Popup Types; Design; Copy; Frequency/Rules; Compliance and Accessibility; Measurement. Key guidance: communicate a real value exchange, respect dismissals and consent, keep close controls available, support keyboard/screen-reader interactions, and avoid blocking mobile content. No linked packaged references.

| ID | Independent defect statement | Applies / minimum evidence |
|---|---|---|
| CG-POP-001 | The popup's offer conflicts with the page-specific offer it claims to extend. | Contextual offer; Text + Base page/campaign. |
| CG-POP-002 | Newsletter copy gives the wrong expected content or sending frequency. | Subscription popup; Text + Base program. |
| CG-POP-003 | A download popup promises a resource different from the delivered resource. | Lead-magnet popup; Text + Base asset. |
| CG-POP-004 | “Instant” delivery is asserted when the real flow requires undisclosed delay or manual handling. | Immediate-delivery promise; Text + Base/Run flow. |
| CG-POP-005 | A promotional percentage or amount disagrees with the actual eligible discount. | Promotion popup; Text + Base offer. |
| CG-POP-006 | A coupon is described as usable without the material eligibility restriction that makes it unavailable to the visitor. | Known restriction; Text + Base eligibility. |
| CG-POP-007 | The displayed promotion deadline is false or expired while copy presents the offer as current. | Time-bound promotion; Text + Base current campaign date. |
| CG-POP-008 | A coupon control fails to copy/apply the code while claiming it did so. | Copy/apply action; Text + Run outcome. |
| CG-POP-009 | The close control is absent, concealed, or unreachable in the rendered popup. | Dismissible conversion overlay; UI/Run affected viewport. |
| CG-POP-010 | A visible close or decline control performs conversion or navigation contrary to its label. | Control present; Text + Run. |
| CG-POP-011 | Decline copy uses guilt or humiliation to misrepresent the neutral choice. | Manipulative decline wording; exact Text. |
| CG-POP-012 | The overlay cannot be operated with the supported keyboard interaction. | Keyboard scope; UI/Run of Tab/Enter or actual relevant control. |
| CG-POP-013 | Escape does not dismiss a conversion dialog where that dismissal is required. | Conversion modal + adopted accessibility behavior; UI/Run + Base requirement. |
| CG-POP-014 | Focus escapes an open modal into obscured page controls. | Modal, not a nonmodal banner; UI/Run focus sequence. |
| CG-POP-015 | Dialog content or control purpose is unavailable to the screen reader. | Accessible dialog requirement; accessibility tree/UI evidence. |
| CG-POP-016 | Text/control contrast violates the specified accessibility standard. | Standard established; UI computed contrast + Base threshold. |
| CG-POP-017 | An essential state or instruction is communicated only by color. | Essential meaning lacks equivalent label/semantic signal; UI evidence. |
| CG-POP-018 | The mobile overlay obscures the close control or prevents reaching its form/CTA. | Supported mobile viewport; UI/Run. |
| CG-POP-019 | Marketing opt-in is prechecked despite a required affirmative-consent model. | Consent applies; UI/source + Base privacy requirement. |
| CG-POP-020 | Consent text describes a narrower or different use than the actual subscription/data exchange. | Data collection popup; Text + Base data use. |
| CG-POP-021 | The privacy-policy link resolves to the wrong policy or is inoperable. | Link supplied/required; UI/Run + Base intended policy. |
| CG-POP-022 | The popup repeats during the known suppression period after an actual dismissal. | Established frequency rule; Base + Run same visitor/session. |
| CG-POP-023 | Converted visitors are retargeted contrary to the explicitly configured exclusion. | Exclusion in scope; Base + Run visitor state. |
| CG-POP-024 | Two conversion overlays overlap despite a declared conflict rule preventing overlap. | Multiple popup strategy; Base + UI/Run. |
| CG-POP-025 | A popup interrupts an explicitly excluded checkout or conversion state. | Exclusion applies; Base route/state rules + Run. |
| CG-POP-026 | Popup conversion is overstated by counting attempts as successful submissions or by using the wrong impression denominator. | Measurement/report artifact; Data definitions and actual events. |

Advisory tactics: 30–60-second delays, 25–50% scroll triggers, exit intent, 400–600px widths, email-only capture, once-per-session caps, 7–30-day suppression, bottom slideups, first-person CTA copy, imagery, and precise trigger percentages are not universal requirements. The skill's popup conversion benchmarks are not proof of site performance. Do not claim an actual Google ranking penalty merely from an overlay's appearance; an intrusive design risk and a measured search effect are different claims.

## Lead magnets — 18 independent checks

Source: [lead-magnets SKILL.md](skill://user/6ac92f6d062c819182aac4bc0df136d6/lead-magnets/SKILL.md), version 2.1.0. Source sections: Principles; Types; Gating; Landing Page and Delivery; Promotion; Measuring Success. Key guidance: a specific usable resource, clear exchange and preview, truthful format/delivery promises, contextual distribution, and lead-quality measurement.

Unavailable linked references: `references/format-guide.md`, `references/content-to-skill.md`, `references/benchmarks.md`. The main document says the content-to-skill reference includes rights checks, an extraction pilot, source-backed lessons, and release; the detailed rights/release checklist was not inspected.

| ID | Independent defect statement | Applies / minimum evidence |
|---|---|---|
| CG-LEAD-001 | The named resource does not address the specific problem it promises to solve. | Promise has a concrete scope; Text + actual Base resource content. |
| CG-LEAD-002 | Landing-page takeaways describe material absent from the resource. | “What's inside” claims; Text + actual resource. |
| CG-LEAD-003 | The stated page count, item count, or content scope is false. | Quantified resource description; Text + Base asset. |
| CG-LEAD-004 | A preview or mockup implies content or functionality missing from the delivered asset. | Preview shown as actual resource; UI/Text + Base asset. |
| CG-LEAD-005 | The promised file/template format differs from the delivered one. | Format claim; Text + Base download. |
| CG-LEAD-006 | A “no special software” promise conceals required proprietary software or paid access. | Such promise; Text + Base actual requirements. |
| CG-LEAD-007 | A claimed mobile-usable resource is unusable on a supported mobile access path. | Explicit mobile promise/requirement; UI/Run actual resource. |
| CG-LEAD-008 | The resource is called free while requiring an undisclosed fee or paid subscription. | Free offer; Text + Base access terms. |
| CG-LEAD-009 | The gate's stated data exchange differs from the actual required fields or subscription consequence. | Capture form; Text + UI/Base actual exchange. |
| CG-LEAD-010 | The gate promises a full version but delivers only an undisclosed sample. | Full-version promise; Text + Base resource. |
| CG-LEAD-011 | A claimed instant-download path is absent or points to an unavailable asset. | Instant delivery; Text + UI/Run asset. |
| CG-LEAD-012 | “Check your inbox” claims delivery after a known required email-send failure. | Delivery status copy; Text + Run provider outcome. |
| CG-LEAD-013 | A drip-series description gives the wrong number or schedule of installments. | Series resource; Text + Base schedule. |
| CG-LEAD-014 | A thank-you page confirms a resource or next step different from the captured offer. | Post-capture state; Text + Base selected resource. |
| CG-LEAD-015 | A blog content upgrade promises relevance to the article but substitutes an unrelated generic asset. | Explicit content-upgrade promise; Text + Base article/asset. |
| CG-LEAD-016 | Download count, audience size, or user testimonial is fabricated or attributed to the wrong resource. | Resource proof; Text + Data/Base. |
| CG-LEAD-017 | A benchmark is reported as this campaign's measured performance without actual campaign data. | Performance report/copy; Text + Data cohort/source. |
| CG-LEAD-018 | Lead volume alone is used to assert qualified-lead or customer conversion success. | Success claim; Data lead qualification and progression definitions. |

Advisory tactics: a single format, under-10/30-minute consumption, one-stage buyer targeting, email-only forms, previews, six-section page structure, both thank-you page and email, content upgrades, paid distribution, and a product CTA are planning choices unless required. Do not propagate “every extra field reduces conversion by 5–10%” or “content upgrades convert 2–5x better” as a product-specific causal fact without evidence. No detailed content-to-skill rights rule is inferred from its unavailable reference.

## Free tools — 17 independent checks

Source: [free-tools SKILL.md](skill://user/6ac92f6d060c81918fc1b4b65ff1eb6f/free-tools/SKILL.md), version 2.0.1. Source sections: Core Principles; Tool Types; Ideation; Lead Capture; SEO; MVP; Evaluation; Common Pitfalls. Key guidance: solve one genuine audience problem, accurately promise inputs/outputs, make the exchange clear, keep the product connection relevant, and measure qualified outcomes and maintenance costs.

Unavailable linked references: `references/tool-types.md`, `references/tool-benchmarks.md`. Named historical cases and numbers in the main source are not independent verification of those cases.

| ID | Independent defect statement | Applies / minimum evidence |
|---|---|---|
| CG-FREE-001 | A calculator, generator, analyzer, or tester is advertised as performing a capability it does not implement. | Tool capability claim; Text + Base functionality/Run. |
| CG-FREE-002 | The tool's required input is mislabeled about the quantity, unit, time period, or data type expected. | Input label; Text + Base formula/validator. |
| CG-FREE-003 | The output label misstates the unit, time horizon, or meaning of the actual result. | Result presentation; Text + Base calculation. |
| CG-FREE-004 | A numeric result contradicts the documented formula for the supplied inputs. | Calculator result; Base formula + Run deterministic values. |
| CG-FREE-005 | An ROI/savings estimate is presented as guaranteed realized savings rather than a model with relevant assumptions. | Financial estimate; Text + Base model assumptions. |
| CG-FREE-006 | A tool claims a live audit or test while showing canned/demo output as actual measured results. | Analyzer/tester; Text/UI + Run provenance. |
| CG-FREE-007 | A “free” tool conceals a mandatory payment before the promised core output. | Free claim; Text + Base gating. |
| CG-FREE-008 | Gating copy promises access without signup/email but then requires that commitment. | Ungated claim; Text + Run actual route. |
| CG-FREE-009 | “Get full report” capture wording delivers only a different or partial output without disclosure. | Partial/full gating; Text + Base output. |
| CG-FREE-010 | A preview misrepresents the output that submitting the required data will provide. | Preview exists; UI/Text + Base actual output. |
| CG-FREE-011 | A claimed supported mobile tool cannot accept input or expose results at the supported viewport. | Mobile promise/requirement; UI/Run. |
| CG-FREE-012 | A lead-capture confirmation says data/report was saved or sent when the required destination operation failed. | Capture operation; Text + Run destination outcome. |
| CG-FREE-013 | A tool landing-page title/description identifies a different tool or use case from the one delivered. | SEO/marketing description; Text + Base tool function. |
| CG-FREE-014 | A CTA claims a natural product continuation that the actual paid product cannot provide. | Product handoff promise; Text + Base product capability. |
| CG-FREE-015 | A build-versus-return recommendation omits known maintenance cost while claiming a complete return calculation. | Investment analysis; Plan + Base/Data costs. |
| CG-FREE-016 | Search demand, lead qualification, or conversion forecasts are stated as observed facts without relevant research. | Strategy/result claim; Plan + Data. |
| CG-FREE-017 | Historical named-tool success numbers are reused as this proposed tool's expected measured result. | Case-based forecast; Text + actual comparable evidence and uncertainty. |

Advisory tactics: one-job tools, product adjacency, no accounts/saved results, email-only gating, a 25+ scorecard cutoff, custom/no-code/embed selection, and SEO-first positioning are strategy choices. Do not fail a requested complex tool or an ungated brand tool for lacking lead capture. Runtime calculation, delivery, reliability, and security claims require actual evidence; content review does not silently become a penetration test.

## A/B testing — 30 independent checks

Source: [ab-testing SKILL.md](skill://user/6ac92f6d05608191931e7369ea914646/ab-testing/SKILL.md), version 2.0.1. Source sections: Core Principles; Hypothesis; Sample Size; Metrics; Traffic Allocation; Running the Test; Analyzing Results; Documentation; Growth Experimentation Program. Key guidance: explicit hypothesis and metric, planned sample/stopping method, correct statistical interpretation, uncertainty and guardrails, and exploratory labels for unplanned segments.

Unavailable linked references: `references/sample-size-guide.md`, `references/test-templates.md`. The Evan Miller/Optimizely calculators and ASA statement links were identified, but this audit did not independently fetch them. Statistical definitions below are explicit in the main source, not inferred from those links.

| ID | Independent defect statement | Applies / minimum evidence |
|---|---|---|
| CG-AB-001 | A test plan claims a specific hypothesis but does not identify the change it proposes to test. | Experiment-plan completeness requirement; Plan. |
| CG-AB-002 | The claimed hypothesis lacks the audience to which the prediction applies. | Segmented/targeted experiment; Plan + Base target. |
| CG-AB-003 | The declared success metric differs from the metric used to call the winner. | Plan + Data analysis. |
| CG-AB-004 | A primary metric has no stated event/denominator sufficient to interpret the decision. | Test or report makes quantitative decision; Plan + Data definitions. |
| CG-AB-005 | A fixed-horizon test is described as fully designed without a sample-size/stopping commitment. | Explicit fixed-horizon design/completeness claim; Plan; sequential plans are different. |
| CG-AB-006 | The sample-size calculation uses a baseline different from the baseline it claims to model. | Calculation/report; Plan + Data inputs. |
| CG-AB-007 | Relative lift is confused with percentage-point change. | Effect/MDE claim; Text + Data arithmetic. |
| CG-AB-008 | A per-variant sample target is reported as the total sample, or vice versa. | Sample planning/report; Plan + Data counts. |
| CG-AB-009 | The duration estimate uses total traffic while claiming eligible assigned traffic. | Feasibility plan; Data eligibility/allocation + arithmetic. |
| CG-AB-010 | Several bundled changes are reported as causal evidence for one isolated component. | Component-level conclusion; Plan variants + Data. |
| CG-AB-011 | A variant's implementation differs from the treatment described in the report. | Experiment/report change; Plan + actual UI/Run variant. |
| CG-AB-012 | The report claims tracking was verified when the relevant success event was never exercised or known to fail. | Validation claim; Run/event evidence, not installed tooling. |
| CG-AB-013 | A user is described as consistently assigned despite evidence of uncontrolled switching between variants. | Consistent-assignment claim/requirement; Plan + Run/Data user assignment. |
| CG-AB-014 | A claimed balanced split ignores a known allocation or exposure imbalance. | Balance claim; Data assigned/exposed counts and timing. |
| CG-AB-015 | A fixed-horizon test is stopped early for significance and reported with its original fixed-horizon false-positive interpretation. | Plan stopping rule + actual Data stopping time. |
| CG-AB-016 | Treatments or audience sources changed mid-test but the result is presented as one unchanged experiment. | Stability claim; Plan/version/source history + Data. |
| CG-AB-017 | A p-value is described as the probability that the null hypothesis is true. | Statistical explanation; exact Text. |
| CG-AB-018 | A p-value is described as the probability that the result was random or will reproduce. | Statistical explanation; exact Text; separate findings for separate false assertions. |
| CG-AB-019 | A frequentist 95% confidence interval is described as a 95% posterior probability for this realized interval. | Statistical explanation; exact Text + stated methodology. |
| CG-AB-020 | A platform's Bayesian/sequential confidence score is interpreted as an ordinary fixed-horizon p-value. | Method interpretation; Plan + Base platform method. |
| CG-AB-021 | A winner claim omits an effect interval while claiming an uncertainty-complete statistical analysis. | Report completeness claim/requirement; Data effect and uncertainty. |
| CG-AB-022 | Statistical significance alone is claimed to establish meaningful business value. | Decision explanation; Text + Plan MDE/value + Data effect. |
| CG-AB-023 | An under-sampled result is labeled conclusive under the test's own required sample rule. | Planned sample and actual Data. |
| CG-AB-024 | Nonsignificance is interpreted as proof of no meaningful effect despite an interval allowing benefit/harm. | Result interpretation; Data interval + Plan practical threshold. |
| CG-AB-025 | A completed fixed-horizon test is extended until significant and represented as the original valid test. | Plan + Data timeline/stopping. |
| CG-AB-026 | An unplanned favorable segment is presented as confirmatory evidence. | Segment-level conclusion; Plan preregistered analyses + Data. |
| CG-AB-027 | A winner is declared while a required negative guardrail result is concealed. | Guardrail adopted; Plan + Data outcomes. |
| CG-AB-028 | The reported test result uses different sample counts or conversion totals from the cited dataset. | Test report; Data source and arithmetic. |
| CG-AB-029 | Cumulative lift adds overlapping relative percentages as though they were independent compounded gains. | Program-level growth claim; Data baselines, overlap, timing, and method. |
| CG-AB-030 | A generic win-rate, velocity, or sample-size benchmark is presented as a guaranteed operating target/result. | Program planning/report; Text + actual assumptions/Data. |

Advisory tactics: 50/50 allocation, single-variable tests, bold variants, fixed 2–4-week duration, ICE scoring, 4–8 experiments/month, 20–30% win rates, 20-item backlogs, and particular tooling are not universal mandates. A bundled redesign test is valid for the bundle; a valid sequential design need not use a fixed horizon. Stopping for technical failures or predefined harmful guardrails is compatible with the source. Planning sample tables are approximate starting points, not measurements of actual test power.

## Marketing psychology — 16 independent checks

Source: [marketing-psychology SKILL.md](skill://user/6ac92f6d06508191b403cc55c6af023c/marketing-psychology/SKILL.md), version 2.0.0. Source sections: How to Use; Foundational Thinking; Understanding Buyers; Influencing Behavior; Pricing Psychology; Design/Delivery; Growth/Scaling. Key guidance: apply an appropriate model to the audience, explain mechanisms without claiming certainty, and implement ethically. No linked reference files.

| ID | Independent defect statement | Applies / minimum evidence |
|---|---|---|
| CG-PSY-001 | A psychological heuristic is presented as a universal law or guaranteed conversion effect. | Causal/generalized psychology claim; Text + relevant evidence/qualification. |
| CG-PSY-002 | A customer motive is asserted as established research when it is only a proposed persona assumption. | Research-backed motive claim; Text + Base/Data research. |
| CG-PSY-003 | A mental-model explanation is applied to the wrong buyer job or desired outcome identified in trusted context. | Strategy/copy explanation; Plan/Text + Base job. |
| CG-PSY-004 | Social-proof numbers or popularity indicators assert events/customers that did not exist. | Proof tactic; Text/UI + Base/Data. |
| CG-PSY-005 | An authority cue implies an endorsement, certification, or affiliation absent from the approved source. | Authority tactic; Text/UI + Base. |
| CG-PSY-006 | A similarity/founder/community story fabricates real identity, experience, or membership. | Real-person/organization claim; Text + Base. |
| CG-PSY-007 | Scarcity/urgency is represented as genuine despite known false capacity or deadline facts. | Scarcity tactic; Text + Base. |
| CG-PSY-008 | A price anchor uses a false original, competitor, or enterprise comparison. | Anchoring claim; Text + Base comparable price and scope. |
| CG-PSY-009 | A discount frame misstates the arithmetic equivalence of the percentage and money savings. | Discount psychology; Text + Base arithmetic. |
| CG-PSY-010 | Daily/monthly cost framing conceals the actual billing commitment or uses an inconsistent conversion. | Mental accounting price frame; Text + Base schedule/arithmetic. |
| CG-PSY-011 | A positive/negative success-rate frame changes the denominator or population while claiming equivalence. | Framed outcome rate; Text + Data definitions. |
| CG-PSY-012 | A default option causes an undisclosed paid or marketing commitment. | Defaults used; UI/Run + Base actual consequence/consent requirement. |
| CG-PSY-013 | Progress or “almost done” wording invents completed work or conceals remaining required steps. | Goal-gradient/Zeigarnik tactic; UI/Text + Base/Run path. |
| CG-PSY-014 | Switching-cost messaging falsely claims data cannot be exported, deleted, or used elsewhere. | Retention/cost frame; Text + Base product/policy. |
| CG-PSY-015 | A before/after comparison changes measurement conditions while presenting a fair product effect. | Contrast demonstration; Text/UI + Base/Data comparable conditions. |
| CG-PSY-016 | Successful examples alone are presented as proof of a strategy's reliable success rate. | Evidence/forecast claim; Plan + Data denominator and failure coverage. |

Advisory tactics: anchors, decoys, default plans, three tiers, loss framing, free trials, round/charm prices, rule-of-100 presentation, one CTA, seven touches, and 80/20 allocations are options, not defects when absent. Ethical general guidance does not authorize a compliance claim. The source's generic “opt-out beats opt-in” recommendation cannot override an applicable affirmative-consent requirement. Broad approximate statements such as “losses feel twice as painful” need appropriate qualification and evidence when published as quantitative science.

## Site bootstrap — 20 independent checks

Source: [site-bootstrap-adm SKILL.md](skill://user/6ac5314b40a08191b208994ce42f7184/site-bootstrap-adm/SKILL.md). Source sections: Workflow 1–8; Completion; Common Failures. Key guidance: preserve target identity and requirements, independently track verified/pending/N/A, distinguish local build readiness from real CMS/contact/release operation, inspect output/accessibility, and prevent copied identities or trackers from leaking into clones.

Unavailable material linked references: `references/baseline.md`, `references/shared-setup.md`, `references/static-site.md`, `references/hybrid-site.md`, `references/lippincott-example.md`, `references/privacy-operations.md`, `references/data-lifecycle.md`, `references/testing.md`. Other linked deployment/source/template assets were indexed by the main source but not read; this audit does not invent their detailed metadata, canonical, privacy, or test rubrics.

These checks concern changed public content, metadata, and assertions about website readiness. They do not mandate Astro, TinaCMS, fast-check, a new CMS, or an automatic setup workflow for an existing site.

| ID | Independent defect statement | Applies / minimum evidence |
|---|---|---|
| CG-WEB-001 | Copied brand names or product identities remain in target public content contrary to the approved target identity. | Clone/new website; Text/UI + Base target identity. |
| CG-WEB-002 | A copied source-project domain appears as the target canonical or public destination without authorization. | Public URL/metadata; Text/source + Base target domain. |
| CG-WEB-003 | A contact CTA/form routes to the source project's recipient instead of the approved target recipient. | Copied contact details; Text/source + Base recipient; Run if delivery is alleged. |
| CG-WEB-004 | Metadata title/description describes the template instead of the approved target website. | Changed/generated metadata; Text/built output + Base target. |
| CG-WEB-005 | A declared canonical/content invariant is violated by generated output. | Exact invariant is in scope; Base independent invariant + built-output evidence; no invented canonical rubric. |
| CG-WEB-006 | CMS-authored content is reported as current while the actual build bypassed required generation. | Freshness/readiness claim; Base generation contract + Run/build evidence. |
| CG-WEB-007 | The published content differs from the approved generated content while the report claims they match. | CMS/generation/publication claim; Base artifact/version + built/deployed evidence. |
| CG-WEB-008 | Static-only hosting is described as executing a contact or other server endpoint. | Hosting capability claim; Text + Base deployment model/Run. |
| CG-WEB-009 | A contact form reports success after required provider delivery failed. | Delivery-dependent success; Text + Run actual provider result. |
| CG-WEB-010 | A delivery error is hidden behind copy asserting that a message reached its intended recipient. | Explicit receipt claim; Text + Run delivery evidence. |
| CG-WEB-011 | A form validation message accepts or rejects values contrary to the approved form invariant. | Form behavior/claim; Base invariant + UI/Run. |
| CG-WEB-012 | Mobile readiness is claimed without the affected responsive state working. | Readiness claim/requirement; UI/Run exact viewport; source code absence is not failure proof. |
| CG-WEB-013 | Keyboard accessibility is claimed while the required interaction is unreachable or inoperable. | Accessibility claim/requirement; UI/Run relevant interaction. |
| CG-WEB-014 | A form-error readiness claim conceals an unhandled observed error state. | Readiness report; Run actual failure + claimed coverage. |
| CG-WEB-015 | A copied analytics identifier sends target/preview traffic to the source project while copy claims isolated analytics. | Isolation claim/explicit rule; Base identifier/host + Run requests/config evidence. |
| CG-WEB-016 | Production-only analytics is claimed but marketing tracking activates on a clone or preview. | Default-off/host restriction applies; Base host rule + Run. |
| CG-WEB-017 | Public output exposes copied personal data or a credential contrary to the accepted publishing scope. | Public artifact changed; direct artifact evidence + Base classification; redact the finding. |
| CG-WEB-018 | A local reproducible build is represented as proof that the real CMS or contact provider is integrated. | Integration claim; Text + relevant actual provider evidence. |
| CG-WEB-019 | Passing local checks are represented as proof of production release. | Release claim; Text + actual selected host/version evidence. |
| CG-WEB-020 | A status document marks a requirement verified although its own required evidence remains pending or blocked. | Bootstrap/readiness documentation; Base requirement + actual recorded evidence. |

Advisory/workflow limits: a bare build command is evidence of what was run, not automatic proof of stale content. Missing adapter/provider/browser evidence produces an unverified claim issue only when an artifact claims success or the task explicitly requires that gate. Do not install tooling, execute full release checks, change frameworks, or publish from ContentGuard. Detailed SEO/accessibility thresholds were not available in linked references and cannot be attributed to them.

## App bootstrap — 18 independent checks

Source: [app-bootstrap-adm SKILL.md](skill://user/6ac532efa6688191954b8f80754d89b0/app-bootstrap-adm/SKILL.md). Source sections: Workflow; Completion; Common Failures. Key guidance: distinguish real server/auth/ownership/provider readiness from mocks or health checks, select only requested features, ground privacy/backup claims, and use the target's identity and instructions.

Unavailable linked material: `references/baseline.md`, `references/shared-setup.md`, `references/application.md`, `references/public-pages.md`, `references/privacy-operations.md`, `references/moderaty-example.md`. Other deployment/source/template assets were indexed but not read. Public-page SEO/accessibility detail is therefore a coverage gap.

These are checks on changed claims and in-scope app surfaces. ContentGuard should not turn a landing-copy edit into a general backend/security audit. A real authorization flaw with no changed-content connection belongs in the relevant software review workflow.

| ID | Independent defect statement | Applies / minimum evidence |
|---|---|---|
| CG-APP-001 | Public app content retains another project's product identity without approval. | Clone/template marketing route; Text/UI + Base target. |
| CG-APP-002 | A “secure server-only” claim is false because the changed public artifact directly exposes the claimed secret/configuration. | Specific secrecy claim; direct public artifact evidence; redact secret values. |
| CG-APP-003 | An ownership/isolation claim exceeds the demonstrated behavior of the actual owner-scoped operation. | Claim made; Base isolation requirement + Run relevant cross-owner case. |
| CG-APP-004 | A price/entitlement claim is contradicted by a trusted server-authoritative result. | Billing/access description; Base authoritative terms + Run. |
| CG-APP-005 | An outage is described as valid empty customer data when the actual data query failed. | User-facing empty/error state; Text + Run outage result. |
| CG-APP-006 | An outage is described as an intentional session expiration when the store failed. | Session error copy; Text + Run actual failure; avoid guessing from user symptoms. |
| CG-APP-007 | A repeated billing/webhook event is claimed harmless despite observed duplicate customer-facing effects. | Idempotency/readiness claim; Run same event/retry identity. |
| CG-APP-008 | Canceled access is described as final while an observed stale event restores it. | Cancellation/entitlement claim; Base event policy + Run chronological events. |
| CG-APP-009 | A provider integration is declared working based solely on a mock response or installed package. | Integration claim; Text + actual provider evidence. |
| CG-APP-010 | A CI configuration file is presented as proof that the referenced checks executed and passed. | Validation claim; Text + actual command/job results. |
| CG-APP-011 | A health-check 200 is presented as proof that the promised scheduled job completed. | Job-completion claim; Text + actual job/result evidence. |
| CG-APP-012 | Backup coverage is claimed for data/providers absent from the verified backup scope. | Backup claim; Text + Base inventory/backup evidence. |
| CG-APP-013 | Recoverability is claimed from backup existence without the restoration evidence required by the report's own gate. | Recovery claim/gate; Base + actual restore evidence. |
| CG-APP-014 | Privacy or deletion claims exceed the actual storage/provider data lifecycle. | Public privacy claim; Text + Base data inventory/verified lifecycle. |
| CG-APP-015 | Marketing analytics is described as default-off while it actually activates in an excluded state. | Default-off promise/rule; Base host/state policy + Run. |
| CG-APP-016 | A production-ready claim is based on local mocks while real provider checks remain explicitly pending. | Readiness claim; Text + Base gates + actual Run evidence. |
| CG-APP-017 | Release success is asserted for a different version or host than the requested release. | Release report; Text + Base expected version/host + actual evidence. |
| CG-APP-018 | A plan/status report treats unrequested accounts, billing, storage, jobs, or paid services as mandatory completed requirements. | Scope/status claim; Plan + Base user requirements; identify each unsupported addition separately. |

Advisory/workflow limits: SvelteKit, accounts, storage, billing, OAuth, workers, mutation tooling, and a particular test runner are not mandatory for every app or landing page. Health and mocks can support narrow statements about health/mocks; they do not establish provider, job, or recovery success. Unknown runtime behavior cannot be graded as an observed defect solely from missing evidence unless the changed content claims that behavior was verified.

## Sites — 14 independent checks

Sources: [sites SKILL.md](skill://plugin_connector_1p_689987207de08191979cf68eca2941c6/sites/SKILL.md) and accessible [Presentation-led sites](skill://plugin_connector_1p_689987207de08191979cf68eca2941c6/sites/references/design/presentation-led.md), both read completely. Main source sections: Implement; Design; Finish. Presentation guidance: sections add distinct substance, make the subject concrete, ground real claims, distinguish demos, preserve bounded edits, and avoid unrelated application features.

The workflow also links storage, identity, app integrations, preview, troubleshooting, MCP, recurring updates, and starter setup documents. They are capability/workflow references rather than a content/CRO rubric; this research did not execute them or treat them as required features.

| ID | Independent defect statement | Applies / minimum evidence |
|---|---|---|
| CG-SITE-001 | A new site's public title still identifies the starter instead of the requested subject. | Target identity supplied; Text/output + Base. |
| CG-SITE-002 | A new site's metadata description still describes the starter or another project. | Metadata changed/in scope; output + Base. |
| CG-SITE-003 | Temporary preview metadata is presented as final public content contrary to the explicit cleanup requirement. | Such metadata persists; direct final output/source evidence. |
| CG-SITE-004 | A bounded requested edit changes unrelated supplied content or structure without authorization. | Bounded task; diff + Base exact accepted scope. |
| CG-SITE-005 | Editing an existing site replaces established branding contrary to the accepted brief. | Branding preservation requirement; diff/UI + Base. |
| CG-SITE-006 | Explicit required content is omitted or materially altered from the accepted brief. | Content constraint; Text/diff + Base. |
| CG-SITE-007 | A real-person claim is invented rather than supplied or verified. | Real person represented; Text + Base fact provenance. |
| CG-SITE-008 | A real-organization claim is invented rather than supplied or verified. | Real organization represented; Text + Base. |
| CG-SITE-009 | Product capabilities are invented to fill a creative gap. | Real product promise; Text + Base. |
| CG-SITE-010 | A testimonial or customer is fabricated as real proof. | Proof content; Text + Base. |
| CG-SITE-011 | Statistics are invented or represented as sourced measurements without a source. | Real statistic; Text + Base/Data. |
| CG-SITE-012 | Illustrative/demo content is indistinguishable from actual factual results. | Demo/example content exists; Text/UI + Base provenance. |
| CG-SITE-013 | An explicit visitor task is blocked by unreadable, unresponsive, or inaccessible changed presentation. | Required task + affected state; UI/Run + Base requirement; name the specific failure. |
| CG-SITE-014 | Handoff claims deployment or behavior verification that the returned deployment or actual QA evidence does not establish. | Completion/handoff text; exact returned state or Run evidence. |

Advisory tactics: a particular narrative progression, section count, use of imagery, deeper presentation, buildless HTML, Vinext, or visual style are not mandatory unless requested. Repetition/filler can be an editorial issue when it actually obscures the task, but “generic feature cards” alone is not an objective failure. ContentGuard does not call create/register/deploy tools or add accounts, persistence, or integrations to make a presentation richer.

## Sites remix — 14 independent checks

Source: [sites-remix SKILL.md](skill://plugin_connector_1p_689987207de08191979cf68eca2941c6/sites-remix/SKILL.md), fully read. Source sections: definition; Inspect; Intake; Implementation Requirements; Setup; Final Handoff. Key guidance: copied source is not copied runtime data, preserve supplied decisions/design/features, adapt source-specific links and file dependencies, use real empty states, and report unverified/deferred setup honestly.

The main source links the Sites workflow (read in full above), storage, and identity/secrets references. Storage and secret configuration procedures are outside the present content-source audit; their detailed contents were not inspected.

| ID | Independent defect statement | Applies / minimum evidence |
|---|---|---|
| CG-REMIX-001 | The remix is described as having copied database records when only source was copied. | Remix description/data claim; Text + Base actual copy semantics. |
| CG-REMIX-002 | The remix is described as having copied stored files that were not copied. | File availability claim; Text + Base source/destination inventory. |
| CG-REMIX-003 | The remix is described as inheriting working runtime secrets/configuration without actual setup. | Runtime-readiness claim; Text + verified configuration presence/Run. |
| CG-REMIX-004 | Copied content is retained despite an explicit decision to clear/replace it. | Content treatment decided; diff/UI + Base decision. |
| CG-REMIX-005 | Copied content is cleared despite an explicit decision to retain it. | Retention decided; diff/UI + Base. |
| CG-REMIX-006 | Unspecified design is changed despite the preservation instruction. | Remix adaptation; diff/UI + Base design scope. |
| CG-REMIX-007 | An unspecified retained feature is removed or disabled without a supplied decision. | Feature preservation applies; diff/Run + Base. |
| CG-REMIX-008 | A confirmed removal disappears from the UI but its active behavior still runs. | Removal decision; Base + UI/Run affected behavior. |
| CG-REMIX-009 | Source-specific external links still direct destination visitors to the original content when adaptation/clearing was required. | Copied-content adaptation; Text/UI + Base treatment and URLs. |
| CG-REMIX-010 | A stored-file link points to an unavailable original dependency while copy presents the file as available. | Retained file dependency; Text + actual availability/Run. |
| CG-REMIX-011 | Missing/deferred records are replaced with fabricated real-looking samples without a request. | Empty destination data; UI/Text + Base no-sample decision/provenance. |
| CG-REMIX-012 | Empty-state copy advertises an add/upload action that the destination does not support. | Empty state; Text + UI/Run actual actions. |
| CG-REMIX-013 | A retained feature is claimed working despite missing required setup or unavailable verification. | Functionality claim; Base required setup + verified presence/Run; redaction is not absence. |
| CG-REMIX-014 | The handoff omits a known deferred feature/setup blocker while presenting the remix as fully complete. | Completion claim; Text + Base known blockers. |

Advisory/workflow limits: intake questions, optional future-content invitations, registration, schema recreation, secret entry, and deployment are workflow concerns. They do not authorize ContentGuard to remix a site, collect secrets, or make remote changes. An unavailable verification result is neither consent to disable a retained feature nor proof that the feature is broken.

## Recommended focused routing

Route the changed surface and semantic operation. Do not infer an entire conversion project merely because a file is HTML or a task mentions a website. A multi-surface change can have several focused tasks; each Haiku evaluation receives only its relevant skill/rule subset, trusted context, and changed spans. The content gate and Jev probability threshold still apply independently of this table.

| Changed surface or artifact | Primary focused skill | Additional routing only when the changed span actually needs it |
|---|---|---|
| General marketing landing, home, feature, about, or contextual blog CTA | cro | Offers for actual offer construction; pricing for amounts/tiers; independent writing/SEO skill for its own text/metadata defects. |
| Public pricing page, plan grid, billing explanation, pricing FAQ | pricing | cro for CTA/message-match issues; offers only for custom bonus/guarantee construction; schema/AI-search skill only for the changed markup/extractability objective. |
| Contact, demo, quote, newsletter, or ordinary lead form | cro | popups when the form is inside an overlay; lead-magnets when it exchanges an asset. Do not route to signup solely because it captures email. |
| Account creation, free-trial registration, waitlist account entry, email verification | signup | pricing for factual charge terms; onboarding only for the actual post-account path. |
| Post-signup wizard, first-run task, empty state, checklist, guided tour, triggered setup reminder | onboarding | paywalls for an actual upgrade gate; signup only if account creation is also changed. |
| In-product feature gate, usage limit, trial-expiration upgrade, paid-plan prompt | paywalls | pricing for actual plan/billing facts; popup rules only for real modal/accessibility behavior. Public pricing alone is not a paywall. |
| Conversion overlay, slide-in, announcement bar, exit-intent dialog | popups | cro/signup for the exact form type, lead-magnets for its offered resource, pricing/offers for actual promotion terms. |
| Downloadable guide/template/checklist, gated resource description, resource-delivery thank-you text | lead-magnets | cro for the capture form; popups for overlay behavior; actual writing/rights review only within its separate scoped task. |
| Free calculator, generator, grader, tester, tool landing page, or result explanation | free-tools | cro for its landing CTA; lead-magnets only for a separate downloadable resource; numeric correctness requires the trusted formula/output evidence. |
| Experiment hypothesis, variants, sample plan, test report, winner explanation | ab-testing | Surface-specific skill only for the corresponding variant's content. Do not demand an experiment for every copy change. |
| Explicit behavioral-science explanation or deliberate persuasion mechanism | marketing-psychology | Relevant surface skill for actual claim/consent/interaction defects. Never run a catalog of biases against ordinary prose. |
| Website clone metadata, CMS/contact/readiness claims, public bootstrap status | site-bootstrap-adm | Specific content/SEO/form skill for its changed output; no startup, host, test-installation, or release workflow. |
| App public-route content and app readiness/privacy/provider claims | app-bootstrap-adm | Specific signup/onboarding/paywall skill for changed user-facing state; no general app security audit from a text-only change. |
| Sites-specific bounded edit, starter metadata, supplied facts, demo labeling, handoff claim | sites:sites | Matching marketing surface skill if relevant. Site framework/publishing instructions do not become content checks. |
| Explicit Sites remix with copied-content/link/file/empty-state treatment | sites:sites-remix | sites:sites for shared content constraints; relevant destination surface skill for a changed offer/form. Never infer remix intent from a copied design alone. |

## Canonical consolidation without catchall findings

Keep the detailed source candidates as provenance. Implement the following exact-overlap aliases as shared atomic checks where useful; all unlisted source IDs remain distinct candidates. An alias applies only to the same fact, term, state, control, or operation in the same changed span. Similar marketing themes are insufficient grounds to merge. Do not aggregate an entire family into one clarity, factuality, accessibility, conversion, or intent score.

| Proposed shared ID | Atomic check to retain | Candidate aliases when they identify that same defect |
|---|---|---|
| CG-CAN-PRODUCT-IDENTITY | Public product/organization identity conflicts with the approved target. | CG-CRO-001, CG-WEB-001, CG-APP-001. |
| CG-CAN-CAPABILITY | A real product/tool capability is claimed but not supplied. | CG-OFF-002, CG-FREE-001, CG-SITE-009. |
| CG-CAN-RESOURCE-CONTENT | A specific promised resource component is absent from the actual resource. | CG-OFF-008, CG-POP-003, CG-LEAD-002; match the exact component, not the whole asset. |
| CG-CAN-RESOURCE-PREVIEW | Previewed real asset content differs from the delivered asset. | CG-LEAD-004, CG-FREE-010; CG-CRO-012 only when the mismatch is this preview. |
| CG-CAN-FULL-OUTPUT | A promised full resource/report is only an undisclosed partial result. | CG-LEAD-010, CG-FREE-009. |
| CG-CAN-DEMO-AS-REAL | Demo/example content is presented as actual customer/user evidence. | CG-CRO-012, CG-ONB-011, CG-FREE-006, CG-SITE-012, CG-REMIX-011 when the root defect is representation rather than an unauthorized sample decision. |
| CG-CAN-TESTIMONIAL | An attributed real testimonial is fabricated or materially changed. | CG-CRO-013, CG-SITE-010, CG-LEAD-016 for its testimonial component. |
| CG-CAN-CUSTOMER-RELATIONSHIP | A real customer or endorsement relationship is falsely asserted. | CG-CRO-014, CG-SITE-010, CG-PSY-005 for that same relationship. |
| CG-CAN-PROOF-COUNT | A stated customer/download/popularity count is false for the represented population. | CG-PSY-004, CG-LEAD-016, CG-SITE-011 if they identify the same count. |
| CG-CAN-CERTIFICATION | A certification/security badge overstates the actual certified scope. | CG-CRO-016, CG-PSY-005 for certification. |
| CG-CAN-FAKE-CAPACITY | Stock, enrollment, or capacity scarcity is false. | CG-OFF-015, CG-PSY-007 for capacity. |
| CG-CAN-FAKE-DEADLINE | An offer's represented deadline is untrue or nonexistent. | CG-OFF-016, CG-POP-007, CG-PSY-007 for that deadline. |
| CG-CAN-PRICE-AMOUNT | The quoted plan price differs from its authoritative amount. | CG-PRI-001, CG-PAY-011, CG-APP-004 for that same amount. |
| CG-CAN-BILLING-PERIOD | The recurring billing period is misrepresented. | CG-PRI-003, CG-PAY-012, CG-PSY-010 for the period. |
| CG-CAN-ANNUAL-PREPAYMENT | Monthly-equivalent copy conceals required annual prepayment. | CG-PRI-004, CG-PAY-012, CG-PSY-010 for prepayment. |
| CG-CAN-DISCOUNT-ARITHMETIC | The stated discount does not match the comparable amounts. | CG-PRI-006, CG-POP-005, CG-PSY-009. |
| CG-CAN-ZERO-PRICE | A free promise conceals a required monetary charge. | CG-PRI-017, CG-SIG-019, CG-LEAD-008, CG-FREE-007; a required card alone is a separate claim. |
| CG-CAN-TRIAL-DURATION | The trial's stated total duration differs from actual terms. | CG-PRI-018, CG-SIG-019 for duration; personalized end-date arithmetic in CG-PAY-007 remains distinct. |
| CG-CAN-PLAN-FEATURE | The named plan does not include the promised specific feature. | CG-PRI-013, CG-PAY-002, CG-PAY-003, CG-APP-004 when referring to that entitlement. |
| CG-CAN-UPGRADE-UNLOCK | The proposed upgrade does not remove the particular represented restriction. | CG-PAY-006, CG-PAY-020 only when the same restriction/claim fails; payment success and entitlement provisioning can be separate roots. |
| CG-CAN-QUOTA-THRESHOLD | The represented usage allowance differs from the actual quota. | CG-PRI-010, CG-PAY-004; actual used-count CG-PAY-005 is separate. |
| CG-CAN-CONTROL-ACTION | A control's label promises a different action from the one it performs. | CG-CRO-007, CG-PAY-015, CG-POP-010, CG-ONB-016, CG-SIG-010 if the exact control is implicated. |
| CG-CAN-HIDDEN-SALES-STEP | A promised immediate self-serve action hides a required sales/approval step. | CG-CRO-010, CG-PRI-019, CG-PAY-013. |
| CG-CAN-STEP-OPTIONALITY | A mandatory step/field is described as optional, or vice versa. | CG-SIG-002, CG-ONB-004; instantiate for the exact step/field. |
| CG-CAN-PROGRESS-COUNT | Displayed progress disagrees with the actual completed/required steps. | CG-SIG-012, CG-ONB-007, CG-ONB-008, CG-PSY-013 only when the same displayed value is wrong. |
| CG-CAN-EMPTY-CTA | An empty state's advertised first action is unsupported. | CG-ONB-010, CG-REMIX-012. |
| CG-CAN-CLOSE-UNAVAILABLE | A dismissible conversion overlay's close control is hidden or unreachable. | CG-POP-009, CG-POP-018, CG-PAY-014 for the same obstruction. |
| CG-CAN-SKIP-INEFFECTIVE | An explicitly skippable tour or optional prompt cannot be dismissed. | CG-ONB-012, CG-PAY-014 when the same skip interaction is affected; distinguish from absent close visibility. |
| CG-CAN-DISMISSAL-IGNORED | A remembered dismissal is ignored during its adopted suppression interval. | CG-POP-022, CG-PAY-018, CG-ONB-013. |
| CG-CAN-SHAMING-DECLINE | A neutral decline action is worded as guilt or humiliation. | CG-POP-011, CG-PAY-016. |
| CG-CAN-MARKETING-CONSENT | An applicable affirmative marketing consent is replaced by an undisclosed/preselected commitment. | CG-POP-019, CG-PSY-012 for the same consent. |
| CG-CAN-DATA-USE-PROMISE | A data-use assurance contradicts actual approved collection/sharing. | CG-SIG-020, CG-POP-020, CG-APP-014 when the exact promise concerns that use. |
| CG-CAN-DELIVERY-SUCCESS | Resource/contact delivery is asserted successful after the required delivery operation failed. | CG-LEAD-012, CG-FREE-012, CG-WEB-009, CG-WEB-010 for the same operation. |
| CG-CAN-INSTANT-DELIVERY | Promised instant delivery actually depends on undisclosed delay/manual handling. | CG-POP-004, CG-LEAD-011 when that is the defect; a missing/broken asset link remains its own defect. |
| CG-CAN-ENRICHMENT-REJECTION | A valid form/account action is rejected because enrichment is unavailable/unknown. | CG-CRO-019, CG-SIG-024 when the same submission is in scope. |
| CG-CAN-META-TITLE | Public title still identifies the template/wrong subject. | CG-WEB-004, CG-SITE-001, CG-FREE-013 for the title only. |
| CG-CAN-META-DESCRIPTION | Public description still describes the template/wrong subject. | CG-WEB-004, CG-SITE-002, CG-FREE-013 for the description only. |
| CG-CAN-SOURCE-LINK | A source-specific destination link contradicts the approved target/content treatment. | CG-WEB-002, CG-REMIX-009 when the same URL is the root defect; canonical and recipient semantics stay separately addressable. |
| CG-CAN-PROVIDER-VERIFICATION | Actual provider integration is claimed from only local/mock/package evidence. | CG-WEB-018, CG-APP-009, CG-APP-016 for that same provider assertion. |
| CG-CAN-DEPLOYMENT-VERIFICATION | A local result is represented as the requested deployed version's success. | CG-WEB-019, CG-APP-017, CG-SITE-014 for that deployment assertion. |
| CG-CAN-DEFAULT-OFF-ANALYTICS | Tracking activates in a state explicitly described as excluded/default-off. | CG-WEB-016, CG-APP-015. |
| CG-CAN-BENCHMARK-AS-RESULT | A generic external heuristic/benchmark is presented as this product's measured result. | CG-OFF-020, CG-ONB-020, CG-LEAD-017, CG-FREE-017, CG-AB-030 for the same stated result. |
| CG-CAN-LEADS-AS-CUSTOMERS | Raw signups/leads are used to establish activation, qualified leads, or customers without the corresponding evidence. | CG-ONB-019, CG-LEAD-018 for the same outcome claim. |
| CG-CAN-UNVERIFIED-COMPLETION | A specific requirement is marked verified while its necessary evidence is explicitly pending/blocked. | CG-WEB-020, CG-REMIX-014, CG-SITE-014 only for that report assertion; do not infer underlying functionality is broken. |

These 44 alias proposals are consolidation instructions, not a replacement checklist. Preserve local IDs for defects with distinct mechanisms: guarantee conditions/remedy/window, resettable timers, overage terms, card requirements, verification recovery, modal focus trap, keyboard support, contrast, color-only instructions, sample-size inputs, fixed-horizon stopping, p-value meaning, confidence-interval meaning, segment selection, and guardrails each need their own rule and evidence. When a candidate lists several possible field properties (for example units/time periods), instantiate the relevant property as its own finding; never issue one vague “terms inaccurate” finding.

## Implementation handoff and practical exclusions

- **Suitable for narrow static checks:** approved identity mismatches; quoted amounts/dates/counts; missing material qualifiers to an explicit promise; internal contradictory terms; mistranscribed supplied testimonials; known wrong destination labels; explicit hypothesis/statistical misinterpretations; source-template residue with trusted target identity. Static confidence still depends on Base and the exact changed span.
- **Requires rendering or behavioral evidence:** unreachable close controls, focus behavior, actual step order, user-state personalization, remembered dismissals, actual delivery, successful account/payment/access transitions, tool calculations, supported mobile behavior. Missing code or a screenshot is not blanket evidence of failure.
- **Requires real analysis evidence:** measured conversion/performance changes, experiment winners, activation/retention correlations, benchmark comparisons, qualified lead outcomes, real price rollout results. The model must not fabricate the evidence to make these checks decisive.
- **Advisory only absent a requirement:** adding page sections, adding/removing navigation, exact CTA count or location, adopting social auth, shortening forms, introducing tiers, adding guarantees or scarcity, changing billing models, setting popup timing, adding lead capture, or using a particular framework/tool/provider.
- **Not an automatic ContentGuard effect:** full-page redesign, new features, generating a replacement offer, analytics instrumentation, running unrelated tests, provisioning resources, schema migrations, collecting secrets, publishing, changing audiences, or remote writes. Return a bounded defect and correction within the authorized task.

Final audit inventory: all 15 assigned main skills covered; 307 source candidate rows; 44 canonical overlap proposals; 15 surface-routing entries; 1 accessible linked content rubric; 39 unavailable linked user-reference reads. Cloud skills became unavailable after the source snapshots were read; no additional availability is assumed.





