"""The example workflows are copied into every protected project, so their safety properties are
pinned here: branch code never runs next to the secrets, and the check job reads the PR head."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
HEAD_SHA = "${{ github.event.pull_request.head.sha }}"
SECRETS = {
    "typesafe-api-key": "${{ secrets.TYPESAFE_API_KEY }}",
    "claude-code-oauth-token": "${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}",
}


def _load(rel: str) -> dict:
    return yaml.safe_load((ROOT / rel).read_text())


def _triggers(wf: dict) -> dict:
    # YAML 1.1 reads the bare key `on` as the boolean True
    return wf.get("on", wf.get(True)) or {}


def _step(job: dict, uses: str) -> dict:
    steps = [s for s in job["steps"] if uses in s.get("uses", "")]
    assert len(steps) == 1, f"expected one step using {uses}"
    return steps[0]


def test_no_tests_workflow():
    wf = _load("examples/rewardguard-no-tests.yml")
    assert "pull_request" in _triggers(wf)
    assert list(wf["jobs"]) == ["rewardguard"]
    job = wf["jobs"]["rewardguard"]
    assert job["permissions"] == {"contents": "read", "pull-requests": "write"}

    checkout = _step(job, "actions/checkout")["with"]
    assert checkout["ref"] == HEAD_SHA and checkout["fetch-depth"] == 0

    guard = _step(job, "reward-hacking-checker")["with"]
    assert guard["mode"] == "check"
    assert guard["tests"] == "false"
    assert {k: guard[k] for k in SECRETS} == SECRETS


def test_two_job_workflow_keeps_secrets_away_from_branch_code():
    wf = _load("examples/rewardguard.yml")
    assert "pull_request" in _triggers(wf)
    tests_job, check_job = wf["jobs"]["rewardguard-tests"], wf["jobs"]["rewardguard"]

    # tests job runs branch code: no secrets, read-only token, no saved git credentials
    assert tests_job["permissions"] == {"contents": "read"}
    assert "secrets." not in yaml.safe_dump(tests_job)
    checkout = _step(tests_job, "actions/checkout")["with"]
    assert checkout["ref"] == HEAD_SHA and checkout["persist-credentials"] is False
    assert _step(tests_job, "reward-hacking-checker")["with"]["mode"] == "tests"

    # check job holds the secrets and must still report when the tests job fails
    assert check_job["needs"] == "rewardguard-tests"
    assert "!cancelled()" in check_job["if"]
    assert check_job["permissions"] == {"contents": "read", "pull-requests": "write"}
    assert _step(check_job, "actions/checkout")["with"]["ref"] == HEAD_SHA
    guard = _step(check_job, "reward-hacking-checker")["with"]
    assert guard["mode"] == "check"
    assert {k: guard[k] for k in SECRETS} == SECRETS


@pytest.mark.parametrize("rel", ["examples/rewardguard.yml", "examples/rewardguard-no-tests.yml"])
def test_examples_only_use_declared_action_inputs(rel):
    declared = set(_load("action.yml")["inputs"])
    assert {"mode", "tests", *SECRETS} <= declared
    for job in _load(rel)["jobs"].values():
        used = set(_step(job, "reward-hacking-checker")["with"])
        assert used <= declared, used - declared
