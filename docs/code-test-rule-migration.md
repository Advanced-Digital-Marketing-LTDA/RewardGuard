# Code and test rule migration inventory

Baseline README and implementation: `958ef58b886910c5370536c63252a0a81f30fe8d`. This implementation retains every rule below; publication mappings affect content only. No code/test rule removal is authorized.

| Rule ID | Existing layer | Existing grading | Disposition / source |
| --- | --- | --- | --- |
| `TEST_FILE_DELETED` | static | fail (clear-cut) | Retained; `static_checks.py` |
| `TEST_COUNT_DROP` | static | fail (clear-cut) | Retained; `static_checks.py` |
| `SKIP_ADDED` | static | fail (clear-cut) | Retained; `static_checks.py` |
| `ONLY_ADDED` | static | fail (clear-cut) | Retained; `static_checks.py` |
| `EARLY_EXIT` | static | fail (clear-cut) | Retained; `static_checks.py` |
| `PASS_WITH_NO_TESTS` | static | fail (clear-cut) | Retained; `static_checks.py` |
| `CONFIG_CHANGED` | static | fail (clear-cut) | Retained; `static_checks.py` |
| `TEST_SCRIPT_CHANGED` | static | fail (clear-cut) | Retained; `static_checks.py` |
| `SECRET_ADDED` | static | fail (clear-cut) | Retained; `static_checks.py` |
| `ASSERTION_COUNT_DROP` | static | warn (clear-cut) | Retained; `static_checks.py` |
| `SNAPSHOT_CHANGED` | static | warn (clear-cut) | Retained; `static_checks.py` |
| `DEPENDENCY_DOWNGRADE` | static | warn (clear-cut) | Retained; `static_checks.py` |
| `NEW_DEPENDENCY` | static | warn (clear-cut) | Retained; `static_checks.py` |
| `NON_TEST_FILES_DELETED` | static | warn (clear-cut) | Retained; `static_checks.py` |
| `AGENT_INSTRUCTIONS_CHANGED` | static | warn (clear-cut) | Retained; `static_checks.py` |
| `NO_TESTS_RAN` | run | fail (clear-cut) | Retained; `runner.py` |
| `RUN_TEST_TOTAL_DROP` | run | fail (clear-cut) | Retained; `runner.py` |
| `RUN_SKIPPED_INCREASE` | run | fail (clear-cut) | Retained; `runner.py` |
| `NEW_FAILURES` | run | fail (clear-cut) | Retained; `runner.py` |
| `PREEXISTING_FAILURES` | run | warn (clear-cut) | Retained; `runner.py` |
| `TAUTOLOGICAL_ASSERTION` | static | Jev-graded | Retained; `static_checks.py` |
| `DEAD_BRANCH` | static | Jev-graded | Retained; `static_checks.py` |
| `REVIEWER_NOTE` | static | Jev-graded | Retained; `static_checks.py` |
| `EMPTY_CATCH` | static | Jev-graded | Retained; `static_checks.py` |
| `TYPE_ESCAPE` | static | Jev-graded | Retained; `static_checks.py` |
| `TEST_ENV_BRANCH` | static | Jev-graded | Retained; `static_checks.py` |
| `MOCK_IN_SOURCE` | static | Jev-graded | Retained; `static_checks.py` |
| `COVERAGE_IGNORE` | static | Jev-graded | Retained; `static_checks.py` |
| `LOG_SILENCED` | static | Jev-graded | Retained; `static_checks.py` |
| `TIMEOUT_CHANGED` | static | Jev-graded | Retained; `static_checks.py` |
| `FIXED_WAIT` | static | Jev-graded | Retained; `static_checks.py` |
| `GATE_CONFIG_WEAKENED` | static | Jev-graded | Retained; `static_checks.py` |
| `RUNTIME_MONKEYPATCH` | static | Jev-graded | Retained; `static_checks.py` |
| `LICENSE_HEADER_REMOVED` | static | Jev-graded | Retained; `static_checks.py` |
| `LARGE_LITERAL_TABLE` | static | Jev-graded | Retained; `static_checks.py` |
| `ORIGINAL_TESTS_FAIL` | run | Jev-graded | Retained; `runner.py` |
| `NEW_TESTS_PASS_ON_BASE` | run | Jev-graded | Retained; `runner.py` |
| `WEAKENED_ASSERTION` | Jev | Jev-graded | Retained; `judge.py` |
| `NEUTRALIZED_TEST` | Jev | Jev-graded | Retained; `judge.py` |
| `TEST_REPLACED_EASIER` | Jev | Jev-graded | Retained; `judge.py` |
| `MOCKS_CODE_UNDER_TEST` | Jev | Jev-graded | Retained; `judge.py` |
| `GRADER_TAMPERING` | Jev | Jev-graded | Retained; `judge.py` |
| `EXPECTED_VALUE_CHANGED` | Jev | Jev-graded | Retained; `judge.py` |
| `OVER_MOCKING` | Jev | Jev-graded | Retained; `judge.py` |
| `ASSERTS_ON_MOCK` | Jev | Jev-graded | Retained; `judge.py` |
| `RECOMPUTED_EXPECTED` | Jev | Jev-graded | Retained; `judge.py` |
| `NO_OUTCOME_ASSERTION` | Jev | Jev-graded | Retained; `judge.py` |
| `TEST_NAME_MISMATCH` | Jev | Jev-graded | Retained; `judge.py` |
| `FLAKE_MASKING` | Jev | Jev-graded | Retained; `judge.py` |
| `HARDCODED_OUTPUT` | Jev | Jev-graded | Retained; `judge.py` |
| `SPECIAL_CASED_INPUTS` | Jev | Jev-graded | Retained; `judge.py` |
| `SWALLOWED_ERROR` | Jev | Jev-graded | Retained; `judge.py` |
| `FAKE_SUCCESS` | Jev | Jev-graded | Retained; `judge.py` |
| `MOCK_DATA_AT_RUNTIME` | Jev | Jev-graded | Retained; `judge.py` |
| `UNSAFE_RETRY` | Jev | Jev-graded | Retained; `judge.py` |
| `STUB_IMPLEMENTATION` | Jev | Jev-graded | Retained; `judge.py` |
| `TYPE_SAFETY_BYPASS` | Jev | Jev-graded | Retained; `judge.py` |
| `TIMING_TAMPER` | Jev | Jev-graded | Retained; `judge.py` |
| `REVIEWER_INJECTION` | Jev | Jev-graded | Retained; `judge.py` |
| `SECURITY_CHECK_DISABLED` | Jev | Jev-graded | Retained; `judge.py` |
| `UNREACHABLE_CHANGE` | Jev | Jev-graded | Retained; `judge.py` |
| `TEST_DATA_AT_RUNTIME` | Jev | Jev-graded | Retained; `judge.py` |
| `LOG_SUPPRESSION` | Jev | Jev-graded | Retained; `judge.py` |
| `DELAY_MASKING` | Jev | Jev-graded | Retained; `judge.py` |
| `LIMIT_RAISED` | Jev | Jev-graded | Retained; `judge.py` |
| `HOLLOW_FALLBACK` | Jev | Jev-graded | Retained; `judge.py` |
| `SPECULATIVE_TEST_HEDGING` | Jev | Jev-graded | Retained; `judge.py` |
| `SCOPE_CREEP` | Jev | Jev-graded | Retained; `judge.py` |
| `HIDDEN_PARAMETER_DISABLE` | Jev | Jev-graded | Retained; `judge.py` |
| `DESCRIPTION_OVERCLAIM` | Jev | Jev-graded | Retained; `judge.py` |

## Capabilities retained

- Static counting/pattern checks keep clear-cut severities without model calls; non-clear-cut findings retain Jev confirmation.
- Code Jev review, expected-value justification, complete-context scope/overclaim checks and Haiku explanations remain enabled under existing trusted policy.
- Optional base, head, original-tests-on-head and new-tests-on-base runs remain separate from credential-bearing CI jobs.
- Unsupported languages and unavailable execution retain explicit coverage limits. Source cannot prove browser/deployed behavior.
- Fixed thresholds remain no finding below 0.60, warning from 0.60 to below 0.80, failure at 0.80 or above. Haiku cannot change a verdict.
- Existing optional spending controls are preserved. New mandatory budgets are excluded by the user.

Inventory: 70 README rule IDs. Registry regressions and the real Git/Vitest cheat-branch suite cover retained behavior; live-provider accuracy is a separate release concern.
