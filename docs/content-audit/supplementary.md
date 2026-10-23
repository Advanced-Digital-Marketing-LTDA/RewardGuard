# Supplementary writing and evidence audit

Reviewed on 2026-10-23. These four main guides were read in full in addition to the 76 guides assigned to the six audit families.

| Skill | Source | Contribution |
|---|---|---|
| data-analytics:validate-data | `skill://Plugin_fc9843a6fb34819195d6c7802398a8a7/validate-data/SKILL.md` | Consequential calculations; populations, units, periods and denominators; caveats; distinction between arithmetic contribution and causal explanation; distinguish unavailable verification from demonstrated error. |
| data-analytics:visualize-data | `skill://Plugin_fc9843a6fb34819195d6c7802398a8a7/visualize-data/SKILL.md` | Truthful chart encodings, comparable scales and units, meaningful uncertainty, distinguish missing observations from zero, source/visual/text agreement, readable accessible labels. |
| pages:maintain-space | `skill://plugin_connector_1p_4a72ddeef4c481918f92d8e8df18fb2c/maintain-space/SKILL.md` | Reconcile updated facts instead of accumulating contradictory copies; preserve distinct facts and dated records; mark task completion only against actual criteria; keep parent summaries and media consistent. |
| google-drive:google-drive-comments | `skill://plugin_connector_1p_ab21a553bfbc81919ea8fd1858e3ffa7/google-drive-comments/SKILL.md` | Evidence anchoring for feedback: exact quotation, location, and concrete problem; avoid vague “this sentence” comments unsupported by the source. |

## Candidate checks

| Candidate | Concrete defect | Applicability / evidence |
|---|---|---|
| REPORT_CALCULATION_CONFLICT | A changed consequential number or rate conflicts with its supplied inputs, formula, denominator, unit, or comparison period. | Reports, case studies, KPI readouts; require inspectable inputs or a demonstrable internal contradiction. Absence of source data is unverified, not proof the number is false. |
| REPORT_SCOPE_MISMATCH | A changed conclusion describes a different population, period, filter, or unit from the cited evidence. | Reports and quantitative copy with supplied source evidence. |
| UNSUPPORTED_CAUSAL_CLAIM | A changed statement presents correlation, temporal coincidence, or an arithmetic contribution as an established causal mechanism without supporting evidence. | Quantitative or research writing; identify the actual leap and material implication. |
| MISLEADING_VISUAL_ENCODING | A changed chart specification misrepresents supplied data through an inappropriate scale, aggregation, geometry, or label. | Chart source/spec/data available; screenshots or rendered evidence needed for clipping/layout findings. House palette and renderer choices are not universal defects. |
| VISUAL_TEXT_CONTRADICTION | A changed figure, title, annotation, or adjacent prose conflicts with the values, scope, or uncertainty in supplied chart evidence. | Quantitative content; cite both sides. |
| UPDATE_FACT_CONFLICT | A content update creates conflicting current facts, claims completion not supported by known criteria, or leaves a dependent current summary materially inconsistent. | Updates with trusted prior/current evidence; preserve historical dated records and intentional time-specific differences. |
| REVIEW_FEEDBACK_UNANCHORED | A submitted review artifact criticizes a quote, range, or location that is absent or materially different in its supplied target. | Review/report artifacts with target text. This also informs ContentGuard's own output contract. |

## Exclusions and resource gaps

Provider-specific renderer, publishing, sharing, scheduling and document API mechanics do not become universal content requirements. No Google Drive or Pages writes were performed.

The linked shared Data analysis-quality resource returned `failed to read skill resource`. Its unseen details were not used. The main guides contain the criteria described above.

