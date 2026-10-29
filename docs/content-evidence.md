# Repository evidence for public-content review

`rewardguard.content_evidence.collect(repo, trusted_base, head, path, cfg, max_chars=18000)` returns `EvidenceBundle` with `text`, `by_code`, `available`, `provenance`, `omissions`, `source_observations` and `budgeted_characters`. It reads only context codes explicitly bound by the source's trusted-base publication declaration. The [publication manifest](shared-ci-public-content.md) separately resolves public reader units and transitive declared dependencies.

## Explicit sources

Each declaration's `evidence` selects configured `[content.context]` codes; only those trusted-base paths are attempted. Each whole nonempty file must fit the remaining allowance. Oversized, absent, excluded or empty files produce omissions without inventing clipped completeness. Availability describes supplied material, not universal readiness for every rule. Evidence remains a repository assertion, with `independently_verified: false`.

The collector does not discover documents or skills, follow Markdown links or imports, scan repository inventories, or collect Git history. It does not execute project code, builds, browser automation, scripts or package installation, and does not fetch URLs or query external accounts. Actual source observations cannot prove a live route, rendering, measurement, claim accuracy or publication state.

## Safety and bounds

Reads use committed Git objects from the trusted policy revision. Mandatory path exclusions apply before blob reads, including explicitly configured context. Private/credential/environment/export/log/generated/dependency paths, internal engineering documents, tests, tooling, CI and backend-only material cannot be opted in by clearing configured lists. Symlinks/submodules and nonregular objects are never followed. Blobs larger than 160000 bytes, binary or undecodable blobs are omitted.

Use dedicated `.rewardguard/content-*` files for intentional product facts, adopted policy or supplied external observations. They are evidence, not grading targets. Keep unrelated engineering instructions out of editorial policy. `content.evidence_exclude` can narrow evidence independently of `content.exclude` for targets; `include`, declarations and context cannot bypass mandatory safety.

Provenance retains real path/commit/source coordinates outside model state. Evidence text is bound to the relevant rule/unit only; paths, Git labels and repository inventories do not become independent-reader state. Public source credential redaction and trusted evidence boundaries are defensive controls, not proof that arbitrary prose has no private information. Source review remains necessary before provider-bearing canaries.

## Coverage

Missing adopted P makes policy-specific rules locally not applicable. Other missing necessary facts/render/measurement evidence is `not_evaluated`, with explicit scope. Selected JSON fields and literal HTML attributes never establish an entire record. C is contract-specific: complete authored Markdown/HTML reader extraction and complete declared dependencies can support only the two authored-text completeness rules described in the API contract.

An unchanged unit without a reusable authenticated completed record is `unchanged`, not missing required evidence or a clean verdict. Completed records preserve coverage, probabilities and findings; stale explanations are explicitly unavailable while their original Jev grades remain. Provider/configuration failures remain errors. CI requires complete coverage through `--require-complete`; local legacy exit behavior remains distinct. See [content configuration](content-checks.md) and [release verification](shared-ci-release-verification.md).
