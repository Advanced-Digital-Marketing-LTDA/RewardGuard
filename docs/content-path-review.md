# Content path review: internal material and publication content

## Finding

The earlier exclusion applied to **grading targets**, while repository evidence
used a separate discovery path. Explicit `[content.context]` files under `docs/`
were still read. Installed skill discovery could treat a developer guide named
`writing-tests.md` as editorial policy. The presence of a file in P provenance
means it was supplied as policy evidence; it does not mean it was itself graded.

Both targets and evidence require explicit trusted-base declarations. Mandatory safety filters run before blob reads. No automatic discovery, reference/import following or Git inventories admit additional material. A declaration or context path cannot opt internal/private/credential sources into the website reviewer.

## Reviewed locations

Exclusions apply at any depth and are case-insensitive. The authoritative patterns
are `DEFAULT_CONTENT_INTERNAL_EXCLUDE` and `DEFAULT_CONTENT_EVIDENCE_EXCLUDE`
in `src/rewardguard/config.py`.

| Repository material | Default locations and names excluded |
| --- | --- |
| Agent/editor/tool instructions | `.agents`, `.agent`, `.claude`, `.codex`, `.cursor`, `.superpowers`, `.windsurf`, `.opencode`, `.serena`, `.gstack`, `.warp`, `.aider`, `.vscode`, `.idea`; AGENTS/CLAUDE/GEMINI/SKILL files and variants |
| Internal documentation | `docs`, `doc`, `documentation`, ADRs, RFCs, specs, plans, runbooks, playbooks, decisions, notes, tickets, tasks, issues |
| Research and verification records | `research`, `notebooks`, `reports`, `audits`, `evidence`, benchmarks |
| Project administration | README, CONTRIBUTING, DEVELOPMENT, ARCHITECTURE, CODE_OF_CONDUCT, MAINTAINERS, TODO, SECURITY, LICENSE, COPYING, NOTICE, CHANGELOG, CODEOWNERS and related variants |
| Root and nested engineering contracts | CONTEXT, ROADMAP, PLAN, DESIGN, SPEC, REQUIREMENTS, TASKS, TESTING, OPERATIONS, DEPLOYMENT, MIGRATION, RUNBOOK, EVIDENCE and variants |
| CI and developer automation | `.github`, `.gitlab`, `.circleci`, `.buildkite`, `.devcontainer`, `.husky`, `.changeset(s)`, `ci`, `scripts`, `tools`, `tooling` |
| Installed repository skills and demos | `skills`, `skills-src`, `examples`, `samples` |
| Tests, fixtures and snapshots | `test`, `tests`, `e2e`, `__tests__`, fixtures/mocks, snapshots, test-results, playwright-report; test/spec/story filename suffixes |
| Storybook and type declarations | `.storybook`, storybook-static, `*.stories.*`, `*.story.*`, `*.d.ts`, `*.d.mts`, `*.d.cts` |
| Infrastructure and deployment | `infra`, `infrastructure`, terraform, deploy/deployment(s), docker, containers, migrations |
| Backend-only sources | backend/server trees; API/server subtrees under src/app/pages/routes; db/database under src/app/lib |
| Build/test configuration | tsconfig/jsconfig JSON; Jest/Vitest/Playwright/ESLint/Prettier/Stylelint/Commitlint/PostCSS/Tailwind/Vite/Webpack/Rollup/Babel configuration and matching rc files |
| Dependencies, output, caches and locks | Existing vendor/node_modules/build/dist/coverage exclusions, framework outputs, virtual environments, Python caches, tool caches, deployment output, snapshots and lockfiles |

This removes the reported Langlo `docs/content-maintenance.md`,
`docs/curriculum-import-contract.md`, `docs/scoring-policy.md`, and every
`.agents/skills/e2e/references/writing-tests.md` section from evidence under
the defaults, even when listed in `[content.context]`.

## Explicit public sources and evidence

Public sources are eligible only when trusted-base `[[content.publications]]` maps their path, artifact type and route. The default empty mapping does not grade arbitrary Markdown, JSON or JavaScript strings. `include` and `source_include` only narrow those declarations. Declared static templates, selected JSON fields, Markdown/HTML reader units and metadata retain explicit extraction limits; there is no whole-source fallback. Runtime output and external facts require supplied evidence.

Mandatory exclusions cannot be undone with `exclude=[]`, mappings or context. Sites whose content currently lives under excluded internal directories need a supported public source layout; do not bypass safety by treating all docs as public. Product/policy/source/measurement files under `.rewardguard/content-*` can provide explicitly bound trusted evidence; they are not grading targets. Installed repository development skills never become editorial policy automatically.

Filtered references and missing required evidence produce explicit omissions/coverage. An unchanged semantic unit without an authenticated completed record is `unchanged`, not a clean finding or missing-evidence error. Missing evidence is `not_evaluated`; an unadopted policy is locally `not_applicable`. Code/test checks and fixed defect thresholds remain intact. See [the publication API](shared-ci-public-content.md) and [configuration](content-checks.md#configure-content-review).

## Release boundary

The filter is effective when an installation runs this RewardGuard revision.
ADM's shared `@v0` channel still pins a published RewardGuard release SHA. After
this fix is reviewed, merged and released, the central dependency upgrade and
successful promotion will deliver it to channel callers. Local pre-commit/Codex
installations must also upgrade. A PR or a moving shared channel alone does not
change the pinned action source.
