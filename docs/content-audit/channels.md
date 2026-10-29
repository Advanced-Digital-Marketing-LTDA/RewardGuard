# ContentGuard source audit: channels, campaigns, and visual content

> Historical source-audit record (2026-10-23). The candidate contracts and routing/evidence proposals below document the broader catalog design, not the current website runtime. In particular, the old Jev task-classifier and automatic evidence-discovery proposals are not active. Current behavior requires explicit trusted-base publications and bound evidence, deterministic supported artifact/rule selection, and mandatory exclusions. See [current review flow](../content-checks.md#review-flow) and [the publication API](../shared-ci-public-content.md).

Research date: 2026-10-23. Scope: twelve channel/content skills; no code, tests, sending, publication, account changes, or live campaign inspection.

This is a catalog of 119 proposed independent defect checks (11 shared and 108 channel-specific), not findings against a submitted marketing campaign. The available local artifacts were the ContentGuard design and implementation plan; no campaign, consent record, listing export, or rendered marketing asset was supplied for this audit. Examples below describe evidence a future review must actually observe.

## Source coverage and limits

Exact packages were discovered with all seven pages of `skills__list({authority:{kind:"cloud"}})`; all twelve complete `SKILL.md` resources were read, with no remaining source cursors. The main texts total 214,448 characters. All 56 attempted material reference reads failed with `failed to read skill resource`. A repeated exact-URI read of the email copy guidelines also failed, and no local reference copies were found. Do not claim that these linked references were audited or import rules supposedly contained in them.

| Key | Skill/version | Complete source URI |
|---|---|---|
| AD | ad-creative 2.10.0 | skill://user/6ac92f6d05708191839917ac4e4c7e2e/ad-creative/SKILL.md |
| ADS | ads 2.4.6 | skill://user/6ac92f6d05788191bb1b8f8d54b14963/ads/SKILL.md |
| EM | emails 2.1.3 | skill://user/6ac92f6d060081919dca24f9a7f1682a/emails/SKILL.md |
| OUT | cold-email 2.2.0 | skill://user/6ac92f6d05b88191969b0e6e18bd495b/cold-email/SKILL.md |
| SMS | sms 1.1.0 | skill://user/6ac92f6d06d88191b4db8366dd2a9848/sms/SKILL.md |
| SOC | social 2.3.3 | skill://user/6ac92f6d06dc819183254fe0d83e7224/social/SKILL.md |
| VID | video 2.2.1 | skill://user/6ac92f6d06e48191b91d6c16406597d3/video/SKILL.md |
| IMG | image 2.0.2 | skill://user/6ac92f6d061881919e52840dd5fdaf58/image/SKILL.md |
| PR | public-relations 1.2.0 | skill://user/6ac92f6d069c8191984eaa96a8725d69/public-relations/SKILL.md |
| ASO | aso 2.0.2 | skill://user/6ac92f6d05908191912a506bb94f6de2/aso/SKILL.md |
| INF | influencer-marketing 1.1.2 | skill://user/6ac92f6d061c8191981d2952b6d87589/influencer-marketing/SKILL.md |
| DIR | directory-submissions 2.1.1 | skill://user/6ac92f6d05f88191abfab38debb6e471/directory-submissions/SKILL.md |

Attempted reference URIs are formed by replacing each source's `/SKILL.md` with `/references/<name>.md`:

| Source | Unavailable material reference names |
|---|---|
| AD | platform-specs; static-ad-templates; creative-review-page; awareness-headlines; hook-system; imessage-video-ads; motion-video-ads; short-form-video-specs; meta-creative-formats; creative-roadmap |
| ADS | rsa-output-spec; audit-guardrails; ad-copy-templates; reading-google-ads-data; creative-research-automation |
| EM | sequence-templates; email-types; copy-guidelines |
| OUT | personalization; frameworks; subject-lines; follow-up-sequences; deliverability; linkedin-outreach; multichannel-cadence; outbound-plays; reply-handling |
| SMS | compliance; whatsapp; sequence-templates |
| SOC | platforms; platform-limits; x-algorithm; post-templates; carousel-frameworks; listening; reverse-engineering; short-form-video |
| VID | ai-video-prompting; edit-anatomy; product-demo-recording |
| IMG | ai-image-prompting |
| PR | story-angles; newsjacking; journalist-pitching; press-platforms; media-outlets; podcast-guest-prep; crisis-communications; statement-templates |
| ASO | scoring-criteria; apple-specs; google-play-specs; benchmarks |
| DIR | positioning-variations; directory-list |

Provider integration guides, vendor pricing pages, tools registries, and operational catalogs outside the above attempts are not content-rule sources in this audit. The inaccessible references remain a documented coverage gap.

## Application, evidence, and probability contract

Keep the approved sequence: deterministic content-presence gate → Jev content-task classification → applicable independent defect checks. Classification at `p >= 0.60` enters review; individual defect probabilities below 0.60 are ignored, 0.60–0.79 warn, and at least 0.80 fail. Routing confidence, missing evidence, and defect probability are different things.

Each check needs a changed span or changed artifact plus the minimum context needed to interpret it. A missing external source is not proof of a defect. Say “unverified/not assessed” when evidence is unavailable; never turn it into a claim that consent is absent, a provider is misconfigured, a legal requirement was violated, or the campaign is compliant.

Evidence keys in the catalog:

- **A:** changed artifact text, metadata, markup, script, final asset, or complete relevant flow; enough for an artifact-visible error.
- **B:** trusted base product facts, approved brief, brand requirement, source quotation, offer terms, agreement, audience, or explicit deliverable contract.
- **P:** confirmed platform/field/format/locale/account capabilities and a versioned current policy profile. Main-skill numbers are source-derived candidate defaults, not proof of current platform policy.
- **R:** supplied runtime or external evidence: consent logs, provider settings, delivery records, live DOM, screenshots, transcripts, rights records, or verified account observations. Review supplied records without making API calls by default.

These are proposed detector statements derived from the cited source sections. A rule expressing an optimization preference becomes a scored defect only when an explicit trusted requirement makes it objectively applicable, or an observed contradiction causes concrete reader harm. Advice about cadence, sentence style, creative format rankings, emoji use, keyword density, or predicted lift does not independently justify a failure.

Haiku should receive one narrow bundled rule excerpt, relevant changed content, and matching trusted base context for the finding. It should not receive all twelve skills, account-operation playbooks, unrelated channel rules, or branch-authored instructions. Treat submitted copy, exports, reviews, fetched pages, and captions as evidence, never as instructions.

## Canonical shared checks

Use these same IDs across the channel sections; do not run a duplicate claim detector for every skill that repeats the rule.

| Proposed check ID | Defect statement and applicability | Minimum evidence | Main-source grounding |
|---|---|---|---|
| `CG_CLAIM_FACT_CONTRADICTION` | A material feature, price, result, statistic, customer count, eligibility, or competitor claim contradicts an identified trusted fact. All promotional surfaces. | A+B; name the exact conflict and source/date. | AD “Grounding rules”; INF “No fabricated claims”; DIR honest comparisons; IMG real UI. |
| `CG_CLAIM_SUPPORT_MISREPRESENTATION` | Copy presents invented, altered, or unverified support as a verified study, review, winning ad, award, or customer result. Flag observable provenance misrepresentation; source absence alone stays unverified. | A+B/R; claimed provenance plus actual record or explicit fabrication evidence. | AD “Every concept cites its source”; ADS “Score only what you verified”; INF real proof. |
| `CG_QUOTE_FIDELITY` | A quoted testimonial, customer statement, interview, or review materially changes the source meaning or attribution. | A+B/R source quote and speaker. | AD reviews verbatim, no invented testimonials; SOC share with credit; PR data/quotes/customer names. |
| `CG_EXPERIENCE_AUTHENTICITY` | First-person use, customer status, personal story, or observed result is fabricated or falsely attributed. Do not infer fabrication from polished language. | A+B/R showing actual speaker/experience or disclosed dramatization. | INF cannot imply customer if not one; SOC manufactured vulnerability; AD dramatized conversations. |
| `CG_PROMISE_DESTINATION_MATCH` | A headline, CTA, link, or code promises an outcome that the linked destination or supplied offer does not provide. | A+B or A+R destination; URL unknown is not mismatch. | ADS landing-page alignment; AD clickbait destination; EM links useful/clear path; INF specific CTA. |
| `CG_PROMO_TERMS_CONSISTENCY` | Discount, deadline, availability, price, or “free” claim conflicts across the reviewed offer, ad, landing page, message, or code terms. | A+B; R when actual code/redemption state matters. | AD genuine urgency and offer constraints; SMS sequence offers; INF promo-code CTA; ASO price/IAP extraction. |
| `CG_METRIC_EVIDENCE_STATUS` | Published analysis labels an estimate, partial sample, unverified value, or incomparable metric as directly measured or complete. | A+B/R definitions, interval, coverage, source and calculation. | ADS audit guardrails and reporting; ASO note what cannot be assessed; DIR verified backlink procedure. |
| `CG_REQUIRED_DISCLOSURE` | A specifically required qualifier, disclaimer, or material limitation is missing or contradicts the claim in the changed artifact. No universal invented disclaimer. | A+B/P showing the precise applicable requirement. | AD “Constraints” mandatory elements; INF brief guardrails; SMS scoped disclosures. |
| `CG_BRIEF_SCOPE_CONFLICT` | Delivered content plainly contradicts an approved audience, product, channel, purpose, mandatory element, or prohibited promise. | A+B; explicit requirement and changed violation. | All twelve “Before Starting” context sections; AD/INF constraints. |
| `CG_FINAL_TOKEN_LEAK` | An artifact marked final/shippable exposes unresolved placeholders or missing-data substitutions as if they were real recipient/product facts. Template source with valid variables is not a defect. | A+B schema/final-state contract; R for rendered substitutions. | EM routing includes merge fields/dynamic content; EM output fields; OUT templated personalization. Derived implementation check. |
| `CG_STYLE_CONTRACT` | A clearly stated trusted editorial prohibition is violated in deliverable copy. Use a concrete rule, not “sounds AI.” | A+B explicit style contract and exact match/context. | AD/EM/OUT/SOC “No AI Tells”; channel source allows exceptions such as a real FAQ or one “No card required.” |

## 1. ad-creative

**Extracted guidance:** Ground scaled concepts in specific reviews, winning ads, or comments; never invent claims, statistics, or testimonials. Enforce actual field limits; RSA assets must work independently and in arbitrary combinations. Keep the landing-page promise deliverable and urgency genuine. The main text explicitly distinguishes recommended visible lengths from maximum lengths. Creative review pages must disclose what is grounded in real assets. Dramatized iOS/AI conversation formats have authenticity rules, but their detailed linked rules are unavailable.

Apply shared claim, quotation, experience, offer, disclosure, scope, and configured-style checks plus:

| Proposed check ID | Defect statement / applicability | Evidence |
|---|---|---|
| `CG_AD_RSA_HEADLINE_LIMIT` | A Google RSA headline exceeds its confirmed hard limit; main source says 30 characters. Count final rendered text with the platform's counting rules. | A+P; resolved dynamic text if used. |
| `CG_AD_RSA_DESCRIPTION_LIMIT` | A Google RSA description exceeds the confirmed hard limit; source says 90 characters. | A+P. |
| `CG_AD_RSA_PATH_LIMIT` | An RSA display-path component exceeds the confirmed hard limit; source says 15 characters per path. | A+P. |
| `CG_AD_RSA_ASSET_COUNT` | A submitted RSA exceeds supported asset/path counts; source says up to 15 headlines, four descriptions, two paths. Do not invent minimums from these maxima. | A+P complete ad record. |
| `CG_AD_RSA_COMBINATION_COHERENCE` | A permitted RSA combination creates a contradiction, incomplete referent, or unsupported composite promise; do not penalize aesthetic repetition alone. | A+P assembly/pinning rules; show a permitted bad combination. |
| `CG_AD_META_HARD_LIMIT` | A Meta field exceeds its confirmed maximum. The source's 125 visible primary-text characters and 40/30 recommended headline/description lengths are not hard rejection limits. | A+P exact placement and field; source lists 2,200 primary-text max. |
| `CG_AD_LINKEDIN_HARD_LIMIT` | A LinkedIn ad field exceeds the confirmed maximum. Source lists 600 intro/200 headline/300 description, distinct from recommended lengths. | A+P exact ad type. |
| `CG_AD_TIKTOK_HARD_LIMIT` | TikTok ad text/display name exceeds the confirmed maximum; source lists 100/40, with 80 text only recommended. | A+P. |
| `CG_AD_X_HARD_LIMIT` | X ad/card text exceeds supported limits for the selected account and format; source lists 280 tweet/70 headline/200 card description. | A+P; do not apply organic premium limits by assumption. |
| `CG_AD_BATCH_SOURCE_TRACE` | A scaled batch explicitly required to contain per-concept grounding lacks its trace, cites the wrong input, or marks an ungrounded concept grounded. Merely lacking a research corpus does not prove every claim false. | A+B accepted Mode 3 deliverable contract and inputs/index. |
| `CG_AD_DRAMATIZATION_MISREPRESENTED` | A scripted conversation or fabricated AI response is presented as an authentic conversation, independent recommendation, or real result. | A+B/R provenance and exact presentation. Detailed required-label rules need a supplied trusted policy because the reference is unavailable. |
| `CG_AD_REVIEW_GROUNDING_DISCLOSURE` | A requested stakeholder creative-review artifact omits its required real-assets/grounding disclosure or falsely labels invented assets real. | A+B accepted review-page contract and asset provenance. |

**Advisory only without an explicit brief:** 3–5 angles, template rotation, avoiding em dashes, pinning restraint, format S–F rankings, impression thresholds, changing one variable, refreshing inputs monthly, and “numbers perform better.” A performance hypothesis is not a factual promise.

## 2. ads

**Extracted guidance:** Align the actual ad promise and destination; distinguish goals and audience/funnel states. Audit only verified evidence. Do not invent negative keywords without a search-terms report, sum different attribution windows, or call branded cheap CPA incremental success absent an incrementality study. Pausing/scaling advice needs sample size, lag, and learning-state evidence. Main-text tactics that promise a minimum conversion lift are not validated causal guarantees.

Apply shared promise, offer, metric, disclosure, scope, and claim checks plus:

| Proposed check ID | Defect statement / applicability | Evidence |
|---|---|---|
| `CG_ADS_ATTRIBUTION_WINDOW_SUM` | A report sums conversions from overlapping/different platform attribution windows as a deduplicated total. | A+B/R exact windows, event definitions and deduplication. |
| `CG_ADS_BRAND_INCREMENTALITY_OVERCLAIM` | A report presents low brand CPA/high brand ROAS as newly created demand without the stated incrementality evidence. | A+B/R campaign/query classification and holdout evidence; ordinary descriptive brand metrics are valid. |
| `CG_ADS_AUDIT_UNKNOWN_AS_FAIL` | An audit labels an uninspected setup “broken,” or calls the audit complete after a required source failed. | A+B/R actual audit coverage and error/access records. |
| `CG_ADS_NEGATIVE_KEYWORD_INVENTION` | A client-facing recommendation represents negative-keyword candidates as report-derived despite no supporting search-term evidence. | A+B/R report; distinguish a hypothetical example from a claimed account finding. |
| `CG_ADS_KILL_RECOMMENDATION_UNQUALIFIED` | A report makes a categorical pause/kill decision from a CPA spike or tiny sample while suppressing known lag, learning state, or uncertainty. | A+B/R sample, lag, state, economics and recommendation text; absence of data means unassessed. |
| `CG_ADS_LIFT_GUARANTEE` | Copy turns a directional tactic/benchmark, including “headline mirroring,” into a guaranteed numerical lift for this campaign without evidence. | A+B/R claimed outcome and actual study/experiment scope. |
| `CG_ADS_AUDIENCE_OFFER_CONFLICT` | A changed ad explicitly targets an ineligible customer or describes a different offer/funnel state from the approved campaign. | A+B targeting/offer brief; R only if actual targeting delivery is asserted. |

**Requires operational evidence:** conversion tracking working, landing-page speed, pixel installation, exclusions, budget, bid strategy, learning phase, reach/fatigue and search-term coverage. Do not infer these from copy alone. Do not enforce 80/20 budget splits, three simultaneous tests, a 20% scaling increment, or native-vs-polished creative preferences as content failures.

## 3. emails

**Extracted guidance:** One primary job/action, useful clear destinations, sequence trigger/audience/goal and explicit exit conditions. Welcome/nurture messages should deliver promised value. Subjects should match the message; fake Re:/Fwd: is expressly prohibited. Coordinate onboarding with actual product state. Numbers for sequence length, timing, word count and subject length are recommendations.

Apply shared promise, offer, claim, token, scope and configured-style checks plus:

| Proposed check ID | Defect statement / applicability | Evidence |
|---|---|---|
| `CG_EMAIL_FAKE_THREAD_SUBJECT` | A first-touch or unrelated message falsely uses Re:/Fwd: to imply a prior thread or forwarded message. Applies to lifecycle and cold email. | A+B/R message/thread context; a real reply/forward is valid. |
| `CG_EMAIL_SUBJECT_PAYOFF_MISSING` | A subject/preview claims a ready resource, result, event, or offer that the body/destination does not provide. | A+B/R relevant body and destination. |
| `CG_EMAIL_PROMISED_RESOURCE_OMITTED` | A welcome/lead-magnet delivery email omits or misidentifies the asset explicitly promised at entry. | A+B entry promise and complete message/destination. |
| `CG_EMAIL_PRIMARY_ACTION_CONFLICT` | Mutually competing primary instructions make the intended task ambiguous or contradict one another. A normal footer/secondary link does not count. | A+B stated primary job and message. |
| `CG_EMAIL_LIFECYCLE_STATE_CONFLICT` | Email asserts the recipient has/has not completed an action or holds a plan when the supplied segment/trigger makes the assertion false. | A+B flow definition; R for actual recipient state. |
| `CG_EMAIL_TRIGGER_SCHEDULE_CONFLICT` | Stated trigger/delay or “immediate” promise conflicts with the delivered flow definition. | A+B flow/accepted promise; R to claim a real delayed send. |
| `CG_EMAIL_EXIT_STATE_CONFLICT` | The changed flow continues a reminder/upgrade/conversion sequence after its defined goal/exit state, causing contradictory messaging. | A+B flow and exit criteria; R for observed actual sends. |

**Evidence limits:** A standalone email cannot establish list consent, deliverability, suppression, actual send timing, or rendered personalization. Missing footer content is actionable only when the applicable program/policy requires it; this main skill is not a general email-law checklist.

## 4. cold-email

**Extracted guidance:** Research-based personalization must connect to the problem, one low-friction ask, each follow-up adds value, honor the breakup promise. Include plain-text opt-out and postal address. Verify lists, disable open/click tracking, prepare secondary domains, and stop all channels on a reply. Fake thread subjects are prohibited. No arbitrary word count or “interest CTA beats meeting” claim should become a default failure.

Reuse `CG_EMAIL_FAKE_THREAD_SUBJECT` and the shared claim/promise/scope checks plus:

| Proposed check ID | Defect statement / applicability | Evidence |
|---|---|---|
| `CG_OUTBOUND_OPTOUT_TEXT_MISSING` | A final B2B cold-email message lacks the required plain-text opt-out line under the selected program contract. | A+B/P full sendable body, not a cropped excerpt. Source “Before You Send” requires the line. |
| `CG_OUTBOUND_POSTAL_ADDRESS_MISSING` | A final cold-email message omits the postal address required by the program/applicable policy. | A+B/P full body/footer and scoped rule. |
| `CG_OUTBOUND_RESEARCH_SIGNAL_FALSE` | Personalization fabricates or materially distorts a funding, hiring, technology, post, or company-news signal. | A+B/R actual signal/source/date; absence of research alone is unverified. |
| `CG_OUTBOUND_BREAKUP_PROMISE_BROKEN` | A sequence promises its last touch then schedules another solicitation to the same recipient without a new permission/context. | A+B complete relevant cadence; R for actual sends. |
| `CG_OUTBOUND_REPLY_STOP_CONFLICT` | A reviewed cadence explicitly continues automated touches after a reply despite its required cross-channel stop rule. | A+B flow/contract; R for actual reply/queue behavior. A standalone draft cannot show this. |
| `CG_OUTBOUND_UNSUBSCRIBE_CONFLICT` | A suppression/opt-out instruction contradicts the reviewed flow or continues outreach to an observed opted-out recipient. | A+B/R suppression definition, opt-out and flow/send evidence. |
| `CG_OUTBOUND_TRACKING_CONFLICT` | A campaign promised/configured to disable open/click tracking contains tracking behavior that contradicts that requirement. | A+B configuration or A+R rendered tracking evidence; ordinary links are not tracking proof. |
| `CG_OUTBOUND_SETUP_STATUS_MISSTATED` | A handoff/report calls domains authenticated, warmed, addresses verified, or deliverability ready without supporting supplied observations, or against known failures. | A+B/R actual status records. Without records, report unverified setup, not a broken sender. |

**Runtime-only absent supplied configuration:** secondary domain selection; SPF/DKIM/DMARC; warmup; list validation; bounce/spam rates; a reply stopping every channel; provider opt-out handling. Do not certify these from message wording.

## 5. sms and WhatsApp

**Extracted guidance:** Consent and messaging scope are channel/jurisdiction specific. The main source gives program-name/frequency/STOP/HELP/rates/terms requirements at opt-in, explicit consent, no prechecked EU/UK controls, sender identity in each message, opt-out on confirmation, HELP content, local quiet hours, retention of consent records, and separation of marketing from transactional purpose. SMS encoding changes segment costs. WhatsApp needs the customer's last-message window, approved templates outside it, correct category, and a current country policy.

Do not reproduce the main text's legal scope or dated pricing as a universal compliance certification. The source has a nuanced footer statement: confirmation and periodic reminders are required in its program framing, whereas a footer on every promotional SMS is described as carrier-recommended. Do not silently elevate “every promotional footer” into an unconditional legal rule. Canadian implied-consent exceptions are also mentioned.

Apply shared claim, offer, promise and disclosure checks plus:

| Proposed check ID | Defect statement / applicability | Evidence |
|---|---|---|
| `CG_SMS_OPTIN_PROGRAM_ID_MISSING` | An SMS opt-in disclosure fails to identify the program/brand where required. | A+B/P actual complete opt-in surface. |
| `CG_SMS_OPTIN_MARKETING_SCOPE_MISSING` | Opt-in copy asks for a phone number or transactional updates while the defined use is marketing, without disclosing that marketing purpose/consent request. | A+B/P form wording and intended program. |
| `CG_SMS_OPTIN_FREQUENCY_MISSING` | The applicable opt-in disclosure omits its required message-frequency expectation. | A+B/P complete form. Do not invent a frequency. |
| `CG_SMS_OPTIN_STOP_HELP_MISSING` | The applicable opt-in disclosure omits required STOP or HELP instructions. | A+B/P complete disclosure. |
| `CG_SMS_OPTIN_RATES_MISSING` | The applicable opt-in disclosure omits required message/data-rate language. | A+B/P complete disclosure. |
| `CG_SMS_OPTIN_TERMS_LINK_MISSING` | A required opt-in terms link is absent, points to an unrelated document, or contradicts the program. | A+B/P link; R if live availability is asserted. |
| `CG_SMS_OPTIN_PRECHECKED` | The actual marketing-consent control is prechecked despite an applicable requirement for affirmative opt-in. | A+B/P markup/render and jurisdiction/program; do not infer checked state from a prose draft. |
| `CG_SMS_MESSAGE_SENDER_ID_MISSING` | A complete final SMS omits required brand/program identification, leaving the sender unclear. | A+B/P actual body and sender context. |
| `CG_SMS_CONFIRMATION_OPTOUT_MISSING` | A final opt-in confirmation omits required opt-out instructions or misstates how to stop. | A+B/P confirmation body and supported behavior. |
| `CG_SMS_HELP_RESPONSE_INCOMPLETE` | The supplied HELP response omits the required brand, STOP information, or support contact. | A+B/P response template. |
| `CG_SMS_STOP_SUPPRESSION_CONFLICT` | The reviewed flow contradicts promised STOP/UNSUBSCRIBE handling or demonstrably continues marketing after an opt-out. | A+B/R handler/flow or actual records; copy cannot prove handler success. |
| `CG_SMS_QUIET_HOURS_CONFLICT` | A specified schedule sends marketing outside the selected recipient-local policy, or claims compliance while using an incompatible timezone. | A+B/P schedule and timezone logic; R for actual send/locality. Federal/state/carrier rules need the scoped policy. |
| `CG_SMS_TRANSACTIONAL_MARKETING_CONFLICT` | A message categorized/consented as purely transactional contains a promotion whose program requires marketing scope. | A+B/P complete body, declared category, context and scoped rule. |
| `CG_SMS_CONSENT_USE_SCOPE_CONFLICT` | The campaign's stated audience/use contradicts supplied consent source, program, purpose, or withdrawal state. | A+B/P/R consent records. No log supplied means unverified, not absent consent. |
| `CG_SMS_A2P_SAMPLE_CONFLICT` | Actual/planned message purpose/content materially differs from the supplied registered campaign sample/use case. | A+B/P/R registration evidence and actual template; do not claim registration is missing just because it is not in the repo. |
| `CG_SMS_SEGMENT_COST_MISSTATED` | A campaign presents a final message as one SMS segment or quotes its cost using a demonstrably wrong encoding/segment count. | A+P encoding and segment rules; B for quoted cost. More than one segment is valid unless the brief forbids it. |
| `CG_SMS_FREQUENCY_PROMISE_BREACH` | The complete reviewed flow exceeds its own disclosed maximum frequency. | A+B full overlapping flows/campaign calendar; R for actual send counts. |
| `CG_WHATSAPP_WINDOW_TEMPLATE_CONFLICT` | A plan uses free-form WhatsApp outreach outside the supplied customer-response window without the approved-template route required by policy. | A+B/P/R window, last customer message, template state. Source says 24 hours; current policy must confirm. |
| `CG_WHATSAPP_CATEGORY_MISLABEL` | A promotional/cart-reminder template is labeled utility/authentication to evade the applicable marketing-category requirements. | A+B/P template content/category; approval status R if claimed. |
| `CG_WHATSAPP_RESTRICTED_DESTINATION` | A plan claims it can deliver marketing templates to a destination currently excluded by the provider. | A+P/R recipient country and current policy. Source flags US numbers; do not hardcode permanent geography policy from the dated skill. |

**Encoding caveat:** The source simplifies non-GSM text as “emojis, accented characters, or curly quotes.” Several accented characters are actually GSM-7. A future evaluator must use the actual encoding and extension-table rules, concatenation limits, and provider behavior, rather than declaring every accent UCS-2. Do not make “short link mandatory,” 160-character preference, daily frequency, initial discount timing, or one emoji an automatic content failure.

**Runtime-only without evidence:** registration state, every keyword variant working, seconds-to-suppression, actual HELP routing, consent retention, recipient-local enforcement, throttling, WhatsApp template approval/quality/limits and actual delivery. A good-looking consent sentence proves none of them.

## 6. social

**Extracted guidance:** Adapt each repurposed item to its platform and make it intelligible without the original episode/article. Credit others' content, preserve genuine stories, and avoid manufactured experience. Captions/subtitles should match speech; on-screen text should be readable and unobscured. Platform limits are reference-routed; the exact character/hashtag reference is unavailable.

Apply shared claim/quotation/experience/promise/scope/style checks plus:

| Proposed check ID | Defect statement / applicability | Evidence |
|---|---|---|
| `CG_SOCIAL_REPURPOSE_CONTEXT_LOSS` | A standalone clip/post removes context needed to interpret the quote, comparison, advice, or claim and materially changes its meaning. | A+B/R original content/transcript plus published excerpt. |
| `CG_SOCIAL_SOURCE_CREDIT_MISSING` | Repurposed third-party content omits credit required by the accepted use/context, or falsely claims original authorship. | A+B/R source and credit requirement; no universal invented attribution format. |
| `CG_SOCIAL_HOOK_PAYOFF_MISSING` | A hook promises a numbered list, demonstration, result, or answer that the complete post/clip does not supply. | A+B complete artifact and intent; curiosity alone is not deception. |
| `CG_SOCIAL_CAPTION_TRANSCRIPT_CONFLICT` | Captions omit, substitute, or mistime important words so the viewer receives a materially different claim/instruction. | A+R audio/transcript/timecodes or complete supplied render. |
| `CG_SOCIAL_TEXT_OBSCURED` | Important caption, disclaimer, or CTA is visibly clipped/covered or unreadable in the intended placement. | A+P/R final dimensions and rendered safe-zone/UI evidence. The source's 2-line/3–5-word recipe is not a universal hard limit. |
| `CG_SOCIAL_PLATFORM_LIMIT_CONFLICT` | Final post text, carousel, or metadata exceeds a confirmed supported field/format constraint. | A+P exact platform/account/post type; no numerical limits can be recovered from the unavailable reference. |

**Advisory:** posting frequency, content-pillar ratios, “link in comments,” first-three-second recipe, daily DMs, one fragment/list per post, emoji bullets, broetry, and ranking-algorithm claims. Real platform constraints or explicit trusted editorial rules can make specific deviations reviewable; generic engagement predictions cannot.

## 7. video

**Extracted guidance:** Product demos should show real product UI; overlays supply readable text. Add captions, match export dimensions to the intended placement, and use original assets when borrowing an edit style. The main skill says to copy editing grammar, never reference footage/script/music. An avatar is a production option, not evidence of a real unscripted founder/customer appearance.

Apply shared claim/quotation/experience/offer checks plus:

| Proposed check ID | Defect statement / applicability | Evidence |
|---|---|---|
| `CG_VIDEO_REQUIRED_CAPTIONS_MISSING` | A deliverable requiring captions for its audience/placement omits them, making required spoken information unavailable to that audience. | A+B/P/R full render/subtitle tracks and placement contract. A script alone does not prove missing captions. |
| `CG_VIDEO_DEMO_FUNCTIONALITY_CONFLICT` | Demo narration/steps/visuals show or promise product behavior contradicted by the approved product version. | A+B/R versioned product evidence and actual demo; ordinary illustrative B-roll is valid. |
| `CG_VIDEO_TEXT_CORRUPTION` | Generated on-screen text corrupts a material feature, amount, instruction, identity, or CTA. | A+R actual inspected frames/OCR plus intended text. Do not infer corruption merely because AI was used. |
| `CG_VIDEO_EXPORT_SPEC_CONFLICT` | The delivered video's actual dimensions, ratio, duration, or supported format conflicts with the confirmed delivery specification. | A+B/P/R media metadata and selected format; “optimal length” advice is not a hard constraint. |
| `CG_VIDEO_REFERENCE_ASSET_COPY` | A style-recreation deliverable uses reference footage/script/music outside the permitted asset scope. | A+B/R reference/source match and permissions/license. Similar edit rhythm alone is not evidence of copying. |
| `CG_VIDEO_PRESENTER_IDENTITY_MISREPRESENTED` | Generated or substituted presenter content is falsely represented as a real person's actual recorded statement/experience. | A+B/R provenance, permissions, and claim of authenticity. No blanket all-avatar disclosure rule is inferred. |

**External limits:** footage/music/voice rights, caption/audio synchronization, actual export quality, and real UI functionality need inspected media or supplied evidence. Tool/model preference, uncanny-valley taste, stock-vs-generated B-roll, and overproduction are recommendations.

## 8. image

**Extracted guidance:** Real screenshots are required when claiming to show actual product UI; models hallucinate interfaces. Match placement dimensions and brand assets; check text and cropping at actual display size. Alt text should describe the image without stuffing. OG/social metadata should identify a usable preview. Compression/size advice addresses delivery, not proof of content quality.

Apply shared fact/provenance/offer/scope checks plus:

| Proposed check ID | Defect statement / applicability | Evidence |
|---|---|---|
| `CG_IMAGE_PRODUCT_UI_MISREPRESENTED` | A fabricated/altered interface is represented as a real product screenshot, falsely demonstrating capability. | A+B/R inspected asset and versioned real UI/provenance. Clearly labeled concept art is different. |
| `CG_IMAGE_TEXT_CORRUPTION` | Final raster/vector text misspells or changes material brand, price, CTA, statistic, instruction, or legal qualifier. | A+R actual image plus B intended text/brand/offer. |
| `CG_IMAGE_PLACEMENT_SPEC_CONFLICT` | A delivered image violates a confirmed required dimension/ratio/file specification for its placement. | A+B/P/R actual media metadata; square vs portrait preference alone is insufficient. |
| `CG_IMAGE_CROP_MESSAGE_LOSS` | Placement cropping/avatar overlays remove essential copy, disclosure, product detail, or CTA. | A+P/R actual image and placement preview. |
| `CG_IMAGE_BRAND_ASSET_CONFLICT` | A final image uses a wrong logo, brand name, or mandatory brand element relative to an explicit trusted requirement. | A+B approved assets/rule; a different visual style alone is advisory. |
| `CG_IMAGE_ALT_CONTENT_CONFLICT` | Changed alt text describes a different image or omits essential information required for the image's actual content role. | A+B/R inspected image, usage context and alt. Decorative images may correctly use empty alt. |
| `CG_IMAGE_SOCIAL_PREVIEW_CONFLICT` | Changed preview metadata points to a missing/wrong asset, mismatches essential page identity, or claims dimensions contradicted by the actual asset. | A+B/P/R page/asset metadata; remote accessibility is unknown without evidence. |

**Do not fail by taste:** absence of WebP/JPEG fallback/CDN, image above 200KB, a particular generation model, seasonally unchanged banner, AI logo concepts, or a 4,000px source. A concrete delivery requirement, broken preview, observed content loss, or measured performance issue is needed. Image optimization runtime findings should route to the existing technical review when appropriate.

## 9. public-relations

**Extracted guidance:** Pitches need a real specific story, data/quotes/contacts, a clear ask and accurate journalist relevance. Press pages should supply usable company facts/assets/contact. Crisis communication requires fact confirmation, one spokesperson, a holding statement, next-update time and appropriate counsel review for the named high-risk incidents. The inaccessible templates cannot justify inventing mandatory wording.

Apply shared fact/quotation/provenance/metric/promise/scope checks plus:

| Proposed check ID | Defect statement / applicability | Evidence |
|---|---|---|
| `CG_PR_INCIDENT_ASSERTION_UNVERIFIED` | A public incident statement presents an explicitly unconfirmed cause, impact, breach scope, injury, or resolution as established fact. | A+B/R incident fact ledger and exact statement; no fact ledger means unverified, not necessarily false. |
| `CG_PR_INCIDENT_STATUS_CONFLICT` | Crisis messages contradict the supplied confirmed timeline/status, affected audience, spokesperson, or remedy. | A+B/R confirmed incident state and complete relevant statements. |
| `CG_PR_UPDATE_COMMITMENT_CONFLICT` | The statement gives inconsistent next-update times/contact instructions or conflicts with the approved communication schedule. | A+B schedule/contact; R to claim a real missed deadline. |
| `CG_PR_REQUIRED_REVIEW_SCOPE_CONFLICT` | A final statement is represented as approved despite a supplied policy requiring unfulfilled counsel/spokesperson review for the actual incident. | A+B/R incident classification, trusted approval requirement and status. No review record alone cannot prove approval was skipped. |
| `CG_PR_PITCH_RELEVANCE_MISREPRESENTED` | A pitch falsely claims a journalist covered a beat/article, or labels stale/unrelated material a new event. | A+B/R actual cited articles/event dates and message. Weak fit without a false claim is advice. |
| `CG_PR_PRESS_ASSET_FACT_CONFLICT` | Company bio, disclosed funding/founding/team facts, coverage list, named quote, or press asset contradicts verified approved information. | A+B/R exact facts/coverage/provenance. Existing shared claim ID can own a duplicate finding. |

**Do not enforce as default failures:** pitch under 150 words, HARO under 200, PR mix covering three modes, a fixed 24-hour contact promise, four-to-six-week program, branded vocabulary dislikes, or a one-hour newsjacking deadline. An actual promised response time/embargo/exclusive may be reviewed through shared promise/scope rules when documented.

## 10. aso

**Extracted guidance:** Separate Apple and Google fields and their hard limits; Apple keyword field is bytes, not characters. Google Play title content has stated restrictions. Fetching text is insufficient for screenshot/video evaluation; explicitly note missing data. Do not claim paid-tool ranking/volume knowledge without evidence. Distinguish indexed text fields by platform. Price/IAP transparency should match real availability.

Apply shared fact/price/provenance/metric/disclosure/scope checks plus:

| Proposed check ID | Defect statement / applicability | Evidence |
|---|---|---|
| `CG_ASO_TITLE_LIMIT` | Apple or Play app title exceeds the confirmed hard limit; source says 30 characters for either store. | A+P exact platform/locale and final field. |
| `CG_ASO_APPLE_SUBTITLE_LIMIT` | Apple subtitle exceeds the confirmed maximum; source says 30 characters. | A+P. |
| `CG_ASO_APPLE_PROMO_LIMIT` | Apple promotional text exceeds the confirmed maximum; source says 170 characters. | A+P. |
| `CG_ASO_APPLE_KEYWORD_BYTES` | Hidden Apple keyword field exceeds its confirmed byte budget; source says 100 bytes. | A+P actual encoding/field contents. Never infer this hidden field from title/subtitle alone. |
| `CG_ASO_PLAY_SHORT_DESCRIPTION_LIMIT` | Play short description exceeds its confirmed maximum; source says 80 characters. | A+P. |
| `CG_ASO_PLAY_FULL_DESCRIPTION_LIMIT` | Play full description exceeds its confirmed maximum; source says 4,000 characters. | A+P. |
| `CG_ASO_PLAY_TITLE_POLICY` | Final Play title contains a prohibited ranking/price/promotion/format element under a current applicable policy. Source lists emoji, all caps, “best/#1/free” and CTAs. | A+P current policy and exceptions; brand names/quoted examples need context. |
| `CG_ASO_SCREENSHOT_COUNT_CONFLICT` | A complete store submission violates confirmed screenshot count/device constraints; source says Play minimum two/max eight, Apple up to ten. | A+P complete per-device submission. Fewer than five is a source optimization preference, not the same rule. |
| `CG_ASO_FEATURE_GRAPHIC_SPEC_CONFLICT` | A required Play feature graphic is missing or violates the confirmed placement specification; source says 1024×500 for featured placements. | A+B/P/R required placement and actual asset. Do not universally require it from a cropped listing. |
| `CG_ASO_INDEXING_CLAIM_FALSE` | A submitted audit/strategy misstates which store fields are indexed and sells unsupported ranking effects from that premise. | A+P/R current documented indexing behavior; treat source claims about screenshot-caption indexing as unverified until confirmed. |
| `CG_ASO_VISUAL_ASSESSMENT_UNSUPPORTED` | An audit claims to have inspected screenshot copy, icon, video, or layout despite only having scraped text/incomplete visual evidence. | A+B/R actual evidence coverage and report claims. |
| `CG_ASO_SEARCH_METRIC_UNSUPPORTED` | Reported search volume/exact rank or competitor keyword ranking is presented as observed without supporting tool/data evidence. | A+B/R dated locale/store metrics; do not infer ranks from text keyword presence. |

**Reject arbitrary optimization as gate criteria:** below-4.0 rating; last update over three months; fewer than five screenshots; missing video; less than 1%/2–3% keyword density; repeated visible words used to infer a hidden keyword-field defect; category change solely to face weaker competition; language count; custom-page/event counts; and assumed conversion lifts. The source itself adjusts judgments for brand maturity and actual market. Runtime crashes/ANR, review-prompt quotas and exact ranking are outside a text-only check.

## 11. influencer-marketing

**Extracted guidance:** Any material connection in the actual campaign needs clear noticeable disclosure: payment, gift, commission, employee/family link or free trial. Source examples say #ad/#sponsored; #sp/#collab/#ambassador/“thanks” alone are insufficient. Disclosure should not be below the fold/buried in hashtags; audio/video needs spoken disclosure under this source's prescribed regime. Platform paid-partnership tools supplement written disclosure. Creators cannot invent results or imply customer use they did not have. Briefs/agreements need disclosure obligations and defined usage rights.

Apply shared claim/quote/experience/promise/disclosure/scope checks plus:

| Proposed check ID | Defect statement / applicability | Evidence |
|---|---|---|
| `CG_CREATOR_CONNECTION_UNDISCLOSED` | A sponsored/gifted/affiliate/employee campaign with a known material connection omits its applicable disclosure. | A+B/P relationship plus complete content; ordinary organic praise is not presumed sponsored. |
| `CG_CREATOR_DISCLOSURE_AMBIGUOUS` | The only supplied disclosure uses an insufficient label under the applicable regime, leaving the material connection unclear. | A+B/P actual label/relationship/regime; cite exact insufficiency rather than blanket “FTC compliant.” |
| `CG_CREATOR_DISCLOSURE_HIDDEN` | Required disclosure is buried below “more,” in a hashtag wall, or outside the content where the viewer encounters the endorsement. | A+P/R actual placement/render/length and required visibility. |
| `CG_CREATOR_AUDIO_DISCLOSURE_MISSING` | A relevant sponsored audio/video endorsement lacks the required spoken disclosure while relying only on a description or off-screen label. | A+B/P/R complete audio/transcript and scoped requirement. |
| `CG_CREATOR_PLATFORM_LABEL_MISSING` | A confirmed paid partnership omits the platform label additionally required for that placement. | A+B/P/R platform capabilities, relationship and actual publishing state; label status cannot be inferred from caption text alone. |
| `CG_CREATOR_FALSE_ENDORSEMENT` | Content claims creator use/customer status/results contradicted by known provenance or scripted claims. | A+B/R actual relationship/use; shared experience/claim IDs should own duplicate reports. |
| `CG_CREATOR_USAGE_RIGHTS_CONFLICT` | The planned ad reuse/whitelisting/channel/duration exceeds the supplied creator agreement or misstates permission. | A+B/R agreement and planned use; no agreement supplied means unverified rights. |
| `CG_CREATOR_BRIEF_DISCLOSURE_OMITTED` | A final creator brief/agreement required to specify disclosure omits it or instructs concealment. | A+B/P complete accepted deliverable and campaign relationship. |

**Limits:** Do not infer fake followers from follower count alone, require creators to follow an exact script, or flag rate-card/range differences as factual defects. Jurisdiction, regulated category, actual paid-partnership setting, rights and shipped visibility require evidence. Source “route to legal” does not mean every creator draft needs a new approval flow.

## 12. directory-submissions

**Extracted guidance:** Match actual product capability to the directory category, describe competitors honestly, use real screenshots, point to a real destination, and ask for honest feedback rather than Product Hunt upvotes. Verify the specific product anchor in HTML/rendered DOM, its destination/redirects and rel tokens; HTTP headers are not backlink verification. Without qualifiers record “unqualified link observed,” not guaranteed dofollow/ranking credit. Missing/blocked inspection stays unverified. Cross-posted technical content should point canonical metadata to the original.

Apply shared fact/provenance/promise/metric/scope and image authenticity checks plus:

| Proposed check ID | Defect statement / applicability | Evidence |
|---|---|---|
| `CG_DIRECTORY_CATEGORY_CAPABILITY_FALSE` | Listing claims an AI/MCP/no-code/integration capability or category fit contradicted by the actual approved product. | A+B exact capability/product evidence. Different truthful emphasis per directory is valid. |
| `CG_DIRECTORY_DESTINATION_MISSING` | A final listing's selected CTA/destination is demonstrably absent, unrelated, or unavailable to the intended audience. | A+B route/offer or A+R actual destination; missing evidence of indexing is not broken availability. |
| `CG_DIRECTORY_UPVOTE_SOLICITATION` | Product Hunt outreach explicitly solicits upvotes despite the selected launch policy requiring feedback and prohibiting manipulation. | A+B/P actual platform/campaign policy. Ordinary request for honest feedback is valid. |
| `CG_DIRECTORY_BACKLINK_VERIFICATION_METHOD` | A report claims backlink destination/rel verification from HTTP headers, an unrelated anchor, or a canonical tag. | A+B/R evidence/method and exact claim. |
| `CG_DIRECTORY_BACKLINK_QUALIFICATION_FALSE` | A report calls a product link unqualified despite observed nofollow/sponsored/ugc, or calls an absent/uninspectable link verified. | A+R inspected product anchor/redirects/rel tokens, timestamp and access limits. |
| `CG_DIRECTORY_BACKLINK_BENEFIT_GUARANTEE` | Copy guarantees indexing, ranking credit, dofollow status, traffic or leads from a listing without supporting observations/terms. | A+B/P/R exact guarantee and evidence; anchor lacking rel is not proof of ranking benefit. |
| `CG_DIRECTORY_BADGE_STATUS_FALSE` | An awarded/free/paid review badge or listing is represented as earned/current when supplied eligibility/account status contradicts it. | A+B/P/R actual platform rules/account/award; source's badge pricing/counts are dated, not automatic truth. |
| `CG_DIRECTORY_FORM_SPEC_CONFLICT` | Submitted listing text/assets violate confirmed target-directory field/category/asset constraints. | A+P actual target form spec. Source preparation targets (60-character short copy/150 words) are not every directory's limits. |
| `CG_DIRECTORY_CANONICAL_TARGET_CONFLICT` | A reviewed cross-post claims canonical credit to the original but points canonical metadata elsewhere or to a nonexistent source. | A+B/R actual origin and cross-post metadata. |

**Do not import the main source's unsupported SEO rules as failures:** universal mandatory FAQ schema; automatic AI duplicate-content penalty; one H1 causing 2.8× citations; 6–27× AI traffic conversion; directory DR minimums; three alternatives/three use cases/twenty templates before any listing; fixed day-30/day-90 KPI targets; 2.7× video upvotes; first-two-hour supporter thresholds; “directories always pass dofollow”; exact report cutoffs; or “all cross-posts produce dofollow.” These are unsupported, contextual, or policy-sensitive propositions in this source. A submitted artifact repeating them as proven facts can trigger shared claim/evidence checks; they should not become reviewer axioms.

## Canonical routing recommendation

Route by changed artifact type and known destination, not a filename keyword alone. A JSON or TypeScript file may contain ad copy, localizations, subtitles, consent text or a campaign definition; a Markdown file may only document a hypothetical example. Never treat quoted “bad examples” inside policy documentation as actual campaign copy.

| Changed content / routing evidence | Candidate family | Narrow explainer source/context |
|---|---|---|
| Any public promotional promise, quote, offer, statistic or product claim | Only applicable canonical shared checks | One claim/provenance/offer excerpt; trusted product facts or cited source |
| Google RSA export, selected platform ad field, paid-ad creative | AD hard-field/assembly rules, shared promise/claim checks | AD Platform Specs or Grounding rules; exact platform field profile |
| Paid-media report, audit or campaign recommendation | ADS evidence/attribution/recommendation rules | ADS Audit Guardrails/reporting excerpt; supplied data definitions/coverage |
| Lifecycle email/sequence/entry promise | EM; shared offer/claim/token checks | EM sequence/subject/action excerpt; actual trigger/segment/exit flow |
| Explicit B2B cold-outreach sequence/cadence | OUT plus real/fake-thread subject rule | OUT Before You Send/followup/cross-channel excerpt; actual full message/flow |
| SMS opt-in surface/confirmation/HELP/message/schedule | Only matching SMS subtype checks | SMS compliance/structure paragraph; scoped program/jurisdiction profile |
| WhatsApp template, category or window plan | Only three WhatsApp checks plus shared content rules | SMS WhatsApp paragraph; supplied current window/category/country evidence |
| Organic social post/carousel/repurposed clip | SOC; shared quote/experience/claim checks | SOC standalone repurposing/caption guidance; selected platform/format |
| Video script/captions/deliverable and provenance | VID; relevant SOC or AD placement check if known | VID demo/captions/edit-asset excerpt; inspected transcript/frames/metadata |
| Product screenshot/banner/alt/OG/image delivery | IMG; matching shared claim and placement check | IMG real UI/placement/alt/preview excerpt; actual image and trusted assets |
| Incident statement/newsroom/pitch/press brief | PR; relevant shared fact/promise/quote checks | PR crisis/pitch/newsroom excerpt; approved fact ledger or stated story source |
| Apple/Play listing export/ASO report | ASO; shared price/claim checks | ASO exact field/evidence-limits excerpt; confirmed store/locale/policy |
| Sponsored/affiliate/gifted creator caption, brief or reuse plan | INF plus relevant platform/media checks | INF disclosure/rights/claims excerpt; actual relationship and placement |
| Directory entry/review badge/backlink report/Product Hunt outreach | DIR plus image/shared claim checks as relevant | DIR exact listing/backlink/PH excerpt; selected directory and supplied DOM/policy |

A creator video does not automatically run all video, social, ad, SMS, directory and ASO checks. Select applicable media integrity checks, the actual platform limits, sponsorship disclosure checks supported by a known connection, and any concrete changed claims. Collapse overlapping findings by changed span and underlying defect; retain source provenance without multiplying the failure count.

## Required evidence boundaries for implementation planning

1. **Artifact-visible, generally reviewable now:** final text exceeds a confirmed field cap; fake first-touch Re:; an opt-in disclosure visibly misses a known required term; misleading CTA/offer; quote differs from supplied source; disclaimer cropped in an inspected render; a consent checkbox is visibly prechecked under a confirmed rule; a report describes header-only backlink checking as anchor inspection.
2. **Needs trusted factual or contractual context:** product claims, actual customer experience, approved offer, creator relationship, rights window, required brand elements, definitive final-vs-template status, registration sample, approved incident fact ledger.
3. **Needs current provider/channel evidence:** ad/store field limits and counting; allowed title elements; exact WhatsApp country/template/window restrictions; platform disclosure controls; relevant consent rules; directory badge/field policy.
4. **Needs runtime evidence:** consent actually recorded; opt-out every keyword works; recipient-local sends; authenticated/warmed email domains; verified recipients; current rankings; live link rel; actual pixel/conversion events; uploaded partnership labels; actual media encoding/caption sync and delivered rendering.
5. **Unavailable evidence is a coverage note:** it is not a finding probability of 1.0, nor a pass. Where content itself claims “verified,” “approved,” “compliant,” “one segment,” “dofollow,” “currently ranked,” or “guaranteed,” assess that specific assertion using the supplied evidence and calibrated uncertainty.

No outward action is needed to implement these review distinctions. The judge job can evaluate trusted supplied snapshots without executing branch code, fetching arbitrary URLs from the diff, sending messages, or touching accounts.

