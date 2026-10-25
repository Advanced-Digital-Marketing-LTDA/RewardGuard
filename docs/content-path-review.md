# Content path review: internal material and publication content

## Finding

The earlier exclusion applied to **grading targets**, while repository evidence
used a separate discovery path. Explicit `[content.context]` files under `docs/`
were still read. Installed skill discovery could treat a developer guide named
`writing-tests.md` as editorial policy. The presence of a file in P provenance
means it was supplied as policy evidence; it does not mean it was itself graded.

Both entry points now have default exclusions. Evidence filtering runs before
blob reads, configured evidence admission, automatic discovery, Markdown-reference
following, static import/related-source admission and inventory selection.
Known internal paths are not supplied to Jev or Haiku as repository evidence.

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

## Content retained

Public website pages, marketing/landing pages, blog and article sources,
templates/components containing user-visible copy, CMS content, translations,
SEO/schema metadata, robots/sitemaps and publication controls remain eligible
outside excluded locations. Neither all Markdown nor all JSON/source files are
disabled. A source match still requires Jev's task classification before review.
Ambiguous files elsewhere remain subject to classification; filename heuristics
cannot prove whether every repository file is published.

Focused reviewer skills packaged with RewardGuard remain available. Installed
repository development skills are not automatically loaded as content policy.
Code/integrity checks have their own scope and remain unchanged.

## Deliberate evidence and published-docs exceptions

Use `.rewardguard/content-context.md`, `content-policy.md`, `content-inventory`,
`content-sources`, `content-rendered`, `content-measurements` and `content-history`
files for intentional, scoped trusted evidence. These dedicated artifacts are
not content grading targets. Do not copy unrelated engineering instructions into
them. The implicit `.agents/product-marketing.md` default has been removed.

`content.exclude` controls targets. `content.evidence_exclude` independently
controls all evidence, including explicitly configured sources. Both lists are
read from trusted-base configuration. Merely adding a path to `include` or
`context` does not override an exclusion. Projects genuinely publishing from
`docs/`, examples or another excluded directory must deliberately replace both
exclusion lists, admitting only their published subtree and retaining other
internal/generated/test exclusions. An override in a PR cannot affect that PR's
own trusted configuration. Private/credential path safety remains non-overridable.

Filtered configured references produce explicit omission records. Missing policy
or source evidence remains a coverage gap (`not_evaluated` where required), not
a clean verdict or an invented content defect. Jev's rules, probabilities,
warning/failure thresholds and Haiku's explanation-only role are unchanged.

## Release boundary

The filter is effective when an installation runs this RewardGuard revision.
ADM's shared `@v0` channel still pins a published RewardGuard release SHA. After
this fix is reviewed, merged and released, the central dependency upgrade and
successful promotion will deliver it to channel callers. Local pre-commit/Codex
installations must also upgrade. A PR or a moving shared channel alone does not
change the pinned action source.
