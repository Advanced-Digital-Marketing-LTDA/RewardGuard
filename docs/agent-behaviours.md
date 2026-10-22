# Agent behaviours rewardguard looks for

Reward hacking, misleading and destructive behaviours by AI coding agents, from research and incident reports published May–October 2026. For each behaviour this page says which rule covers it, or why no diff-based check can.

## Sources

| Short name | Source | Date |
|---|---|---|
| SpecBench | [SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents](https://arxiv.org/abs/2605.21384) | 20 May 2026 |
| Overeager | [Overeager Coding Agents: Measuring Out-of-Scope Actions on Benign Tasks](https://arxiv.org/abs/2605.18583) | 18 May 2026 |
| SNARE | [SNARE: Adaptive Scenario Synthesis for Eliciting Overeager Behavior in Coding Agents](https://arxiv.org/abs/2605.28122) | 27 May 2026 |
| METR | [METR Frontier Risk Report, Feb–Mar 2026](https://metr.org/blog/2026-05-19-frontier-risk-report/) | 19 May 2026 |
| Enemy | [Coding with "Enemy": Can Human Developers Detect AI Agent Sabotage?](https://arxiv.org/abs/2606.05647) | 4 Jun 2026 |
| Anthropic | [Agentic Misalignment in Summer 2026](https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/) | 13 Jul 2026 |
| Transluce | [Measuring coding agent misalignment in the wild](https://transluce.org/docent/blog/coding-agent-behaviors) | 4 Aug 2026 |
| CSA | [Comment and Control: AI coding agent CI prompt injection](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-coding-agent-ci-prompt-injection-202608/) | 7 Aug 2026 |
| DeepSWE | [Coding Agents Are Learning to Please the Grader](https://joinhandshake.com/research/ai/deepswe-reward-hacking/) | 18 Sep 2026 |
| Oversight | [Reward Hacking Challenges Oversight of Autonomous Research Agents](https://arxiv.org/abs/2609.28614) | 23 Sep 2026 |
| Evasion | [Instrumental Monitor Evasion Emerges Under Ordinary Task Pressure](https://arxiv.org/abs/2609.30217) | 24 Sep 2026 |
| Traces | [LLM Agents Can Easily Tamper With Their Own Traces](https://arxiv.org/abs/2609.30266) | 24 Sep 2026 |
| PocketOS | [AI agent deletes company's entire database in 9 seconds](https://www.livescience.com/technology/artificial-intelligence/i-violated-every-principle-i-was-given-ai-agent-deletes-companys-entire-database-in-9-seconds-then-confesses) | Apr 2026 incident |

## Visible in a diff

### Gaming the tests

| Behaviour | Example | Source | Rule |
|---|---|---|---|
| Memorizing test answers | A 2,900-line hash table of expected outputs instead of a compiler. It passed 97% of the visible tests and 0% of the held-out ones. | SpecBench | `LARGE_LITERAL_TABLE`, `HARDCODED_OUTPUT` |
| Hard-coding outputs for known inputs | Hidden test files were copied, and the code looked answers up in a hard-coded table, scoring 164/165. | METR | `HARDCODED_OUTPUT`, `SPECIAL_CASED_INPUTS` |
| Patching the scorer or a library | Importing the module patched `np.corrcoef`, presented as a "numerical-stability" wrapper. This evaded LLM review 25% of the time. Other agents reached the grader through `inspect.stack()` or `sys._getframe`. | Oversight, METR | `RUNTIME_MONKEYPATCH`, `GRADER_TAMPERING` |
| Leaked labels disguised as constants | Labels fitted offline and hard-coded as "domain priors" evaded LLM review 37.5% of the time. | Oversight | `HARDCODED_OUTPUT` (partly) |
| Reading test or label data at runtime | Code reads the evaluation labels (for example `*_ytest.npy`). | Oversight | `TEST_DATA_AT_RUNTIME` |
| Hollow fallback | `compress("")`, `gzipBytes(nil)`, or a value cut down until it fits, so a size check still passes. | DeepSWE | `HOLLOW_FALLBACK` |
| Hedging for hidden tests | Fourteen routes where six were specified, unused aliases and alternate input shapes. 10–25% of full-reward runs shaped what they built around guesses about hidden tests. | DeepSWE | `SPECULATIVE_TEST_HEDGING` |
| Disabling a parameter while reporting success | An ablation strength was set to 0, the metric was hard-coded, and the run reported "COMPLETED successfully". Gemini 3.1 Pro intervened in 19 of 20 simulated runs, 11 of them covertly. | Anthropic | `HIDDEN_PARAMETER_DISABLE`, `FAKE_SUCCESS` |
| Weakening or skipping tests | Skip or xfail markers, loosened assertions, a failing test deleted while the agent claimed "✅". | Transluce, Overeager | `SKIP_ADDED`, `WEAKENED_ASSERTION`, `TEST_FILE_DELETED`, … |
| Injecting the verifier | Text telling a grader to output a perfect score. | Oversight | `REVIEWER_NOTE`, `REVIEWER_INJECTION` |

### Weakening oversight

| Behaviour | Example | Source | Rule |
|---|---|---|---|
| Silencing the type checker or linter | A loop appended `@ts-nocheck` to TypeScript files. | Transluce | `TYPE_ESCAPE`, `TYPE_SAFETY_BYPASS` |
| Turning off gates | `HUSKY=0`, `--no-verify`, `core.hooksPath=/dev/null`, lowered coverage, a weakened linter config. | Transluce | `GATE_CONFIG_WEAKENED`, `CONFIG_CHANGED` |
| Gutting authentication | Asked to make a failing auth test pass, the agent rewrote `require_auth` as a no-op (25–37% of runs on some harnesses). | Overeager | `SECURITY_CHECK_DISABLED` |
| Rewriting agent instructions | A poisoned `AGENTS.md`, a crafted `.gemini/.env` (CVSS 10.0), or a malicious skill file. | CSA, Traces | `AGENT_INSTRUCTIONS_CHANGED` |

### Going out of scope

| Behaviour | Example | Source | Rule |
|---|---|---|---|
| Committing credentials | A production connection string from `.envrc` hard-coded into `migration.sql`; tokens base64-encoded and committed to get past secret scanning. | SNARE, CSA | `SECRET_ADDED` |
| Over-eager cleanup | Deleting files that weren't part of the task, including a "do not delete" folder. | Overeager | `NON_TEST_FILES_DELETED` |
| Removing licence notices | A copyright header stripped from copied code. | Overeager | `LICENSE_HEADER_REMOVED` |
| Adding or changing packages | A dependency installed to work around an error. | Overeager | `NEW_DEPENDENCY`, `DEPENDENCY_DOWNGRADE` |
| Unrelated changes | A refactor of nearby code the task didn't ask for. | Overeager | `SCOPE_CREEP` |
| Overclaiming in the PR | "Integration Tests Converted ✅" after deleting a test the agent couldn't convert. | Transluce | `DESCRIPTION_OVERCLAIM` |

## Not visible in a diff

These happen in the agent's shell or through APIs at runtime. Rewardguard cannot see them, so they need limits on what the agent is allowed to do.

| Behaviour | Example | Source | Control |
|---|---|---|---|
| Destroying data with a stray token | The agent found an API token in an unrelated file and deleted the production database and its backups in 9 seconds. | PocketOS | Give agents least-privilege tokens with no production access. Require confirmation for destructive API calls. Keep backups off the same volume. |
| Overriding git and the forge | Force-pushing, `reset --hard`, removing branch protection to merge and then restoring it, falsely claiming a review agent approved. | Transluce, Overeager | Branch rulesets that nobody, agents included, can bypass. Agent tokens without admin rights. |
| Leaking secrets through prompt injection | A PR title made CI agents post `GITHUB_TOKEN` and API keys in public comments. | CSA | Run with no secrets on untrusted input, scrub the environment, use an egress allowlist. |
| Evading monitors | Encoding blocked commands, splitting them across tool calls, retrying until the monitor's history drops the blocked step. Attempts reached up to 98% and successes up to 88% under a task-policy conflict. | Evasion | Enforce policy in the sandbox, not in a monitor the agent can route around. |
| Tampering with traces | Deleting session logs when asked; spoofing tool output through `BASH_ENV`. | Traces | Store logs outside the agent's write access. |
| Sabotage that passes review | 94% of developers missed inserted malicious code without a monitor. Even when a monitor correctly flagged it, the sabotage still got through in 56% of sessions. | Enemy | Automated checks like this one plus review, not review alone. |
