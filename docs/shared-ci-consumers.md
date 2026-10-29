# Shared CI consumer inventory

Read-only snapshot taken 2026-10-28 from the 13 repositories exposed by the connected GitHub inventory. This is the accessible inventory, not proof of organization-wide completeness. Each link is pinned to the inspected repository head. No consumer files, permissions, secrets or branch protections were changed.

| Repository / inspected commit | Shared workflow reference | Existing read/check/comment declarations | Test settings agree | Publication mappings | Event overlap |
| --- | --- | --- | --- | --- | --- |
| [SEO-Research @ f14638afd1f8](https://github.com/Advanced-Digital-Marketing-LTDA/SEO-Research/blob/f14638afd1f8cf9a4689963121a0e58e2ffc6bfc/.github/workflows/rewardguard.yml) | `v0` | present | yes (`false`) | 0 (new schema not deployed) | possible feature push + PR |
| [the-lippincott-team @ bad5308d3cef](https://github.com/Advanced-Digital-Marketing-LTDA/the-lippincott-team/blob/bad5308d3cef6ba40dbe8d7c5d4ffb58fcfe8482/.github/workflows/rewardguard.yml) | `v0` | present | yes (`false`) | 0 (new schema not deployed) | possible feature push + PR |
| [Moderaty @ 5ad1c92024de](https://github.com/Advanced-Digital-Marketing-LTDA/Moderaty/blob/5ad1c92024de7e9af51e31efac4285f6d75a8071/.github/workflows/rewardguard.yml) | `v0` | present | yes (`false`) | 0 (new schema not deployed) | possible feature push + PR |
| [Advanced-Digital-Marketing-LTDA @ 25a4d7bcae70](https://github.com/Advanced-Digital-Marketing-LTDA/Advanced-Digital-Marketing-LTDA/blob/25a4d7bcae70f3be84018df9a48224034ab8e7dd/.github/workflows/rewardguard.yml) | `v0` | present | yes (`false`) | 0 (new schema not deployed) | possible feature push + PR |
| [Top-Realtors-Cypress-TX @ 27e22c9b3246](https://github.com/Advanced-Digital-Marketing-LTDA/Top-Realtors-Cypress-TX/blob/27e22c9b32460b30c37ed36b289eb3d0a225365d/.github/workflows/rewardguard.yml) | `v0` | present | yes (`false`) | 0 (new schema not deployed) | branch-filtered |
| [Site-Bootstrap-ADM @ 747418e9a27f](https://github.com/Advanced-Digital-Marketing-LTDA/Site-Bootstrap-ADM/blob/747418e9a27fce292e2e3a9886f4f4b41f3f7635/.github/workflows/rewardguard.yml) | `v0` | present | yes (`false`) | 0 (new schema not deployed) | possible feature push + PR |
| [App-Bootstrap-ADM @ 01ccb499fa25](https://github.com/Advanced-Digital-Marketing-LTDA/App-Bootstrap-ADM/blob/01ccb499fa25cd04b3e7e8a14a8ce2341f0e5902/.github/workflows/rewardguard.yml) | `v0` | present | yes (`false`) | 0 (new schema not deployed) | possible feature push + PR |
| [Langlo @ 7b188c73625a](https://github.com/Advanced-Digital-Marketing-LTDA/Langlo/blob/7b188c73625a866a32a35e537d214f657e9a48ac/.github/workflows/rewardguard.yml) | `v0` | present | yes (`false`) | 0 (new schema not deployed) | possible feature push + PR |
| [AI-Comment-Moderation @ 1253ed23b44b](https://github.com/Advanced-Digital-Marketing-LTDA/AI-Comment-Moderation/blob/1253ed23b44b3eab18a9745efd7257bedb1519aa/.github/workflows/rewardguard.yml) | `v0` | present | yes (`false`) | 0 (new schema not deployed) | possible feature push + PR |
| [tina-cms-mcp @ 2662635ca51e](https://github.com/Advanced-Digital-Marketing-LTDA/tina-cms-mcp/blob/2662635ca51ea900f6339e049763e50af85c8343/.github/workflows/rewardguard.yml) | `v0` | present | yes (`false`) | 0 (new schema not deployed) | possible feature push + PR |
| [coolify-mcp @ 5ca0ae5ceb12](https://github.com/Advanced-Digital-Marketing-LTDA/coolify-mcp/blob/5ca0ae5ceb123a52134380cba71a6fde490ae125/.github/workflows/rewardguard.yml) | `v0` | present | yes (`false`) | 0 (new schema not deployed) | possible feature push + PR |
| [workflows @ 98644db90cb6](https://github.com/Advanced-Digital-Marketing-LTDA/workflows/blob/98644db90cb691013e4a93d1539dc3de5c01e1d4/.github/workflows/rewardguard-check.yml) | `v0` | present | yes (`false`) | 0 (new schema not deployed) | possible feature push + PR |
| [RewardGuard @ 958ef58b8869](https://github.com/Advanced-Digital-Marketing-LTDA/RewardGuard/blob/958ef58b886910c5370536c63252a0a81f30fe8d/.github/workflows/rewardguard.yml) | `v0` | present | yes (`false`) | 0 (new schema not deployed) | branch-filtered |

## Release gates

- All observed callers use the maintained `v0` channel; no older immutable caller pin was observed in this accessible set. Their currently resolved channel/action revisions still require runtime inspection.
- Migrate actual public sources in trusted-base configuration before expecting content coverage. Existing caller configurations have no publication mappings for the new contract.
- Reduce duplicate feature-push/PR events in each caller; do not silently drop default-branch push coverage.
- Validate candidate shared-workflow revision before promotion. Both action uses must match the same published tested release SHA.
- A real public-content consumer must prove initial evaluation, restored clean/warning/failure/explanation reuse, exact action SHA and explicit cache misses. No such run has been performed for this implementation.
- Keep named-secret delivery, read/check/comment permissions and run-tests agreement. Fork/Dependabot credentials and organization settings remain separately verified release prerequisites.
- Durable cross-run storage and concurrent coordination remain REWARD-1. Budget work is excluded. Local hook installations do not follow the shared channel.

The forthcoming authenticated optional-test-artifact integration may require explicit `actions: read` in callers. That permission is not established by the baseline column above; migration and runtime verification must precede promotion.
