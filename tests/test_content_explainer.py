"""Exercise content explanation at the external Claude CLI boundary."""
from __future__ import annotations

import json
import subprocess

import pytest

from rewardguard import explainer
from rewardguard.config import Config
from rewardguard.models import RewardGuardError


RULE = "CG_PRICE_TRIAL_TERMS"
STATEMENT = "The advertised trial duration contradicts the approved offer."
RUBRIC = "Check only trial duration against the trusted offer; do not judge visual style."
STATE = "Trusted offer: 14 days.\nChanged content, line 7: Try it free for 30 days."
ISSUE = {
    "rule": RULE,
    "line": 7,
    "code": "Try it free for 30 days.",
    "problem": "The offer allows a 14-day trial, but this line promises 30 days.",
    "fix": "Change the stated trial duration to 14 days.",
}


class CliBoundary:
    """Replace the paid external process, leaving prompts and validation real."""

    def __init__(self, payload=None, *, stdout=None, returncode=0, error=None):
        self.stdout = json.dumps(payload) if stdout is None else stdout
        self.returncode = returncode
        self.error = error
        self.calls = []

    def __call__(self, cmd, **kwargs):
        self.calls.append({"cmd": cmd, **kwargs})
        if self.error is not None:
            raise self.error
        return subprocess.CompletedProcess(cmd, self.returncode, self.stdout, "CLI failure")


@pytest.fixture
def content_explainer(monkeypatch):
    def install(payload=None, **kwargs):
        boundary = CliBoundary(payload, **kwargs)
        monkeypatch.setattr(explainer, "_run", boundary)
        monkeypatch.setattr(explainer, "_which", lambda name: "/usr/bin/claude")
        cfg = Config(install=None, suites=[], run_tests=False, explainer_timeout_seconds=37)
        return explainer.HaikuExplainer(cfg, token="subscription-token"), boundary

    return install


def answer(issues):
    return {"type": "result", "is_error": False, "result": "", "structured_output": {"issues": issues}}


def test_explains_only_the_requested_content_rule(content_explainer):
    client, boundary = content_explainer(answer([ISSUE]))

    issues = client.explain_content(STATE, RULE, STATEMENT, RUBRIC, anchors={7: "Try it free for 30 days."})

    assert issues == [{
        "line": 7,
        "code": "Try it free for 30 days.",
        "problem": "The offer allows a 14-day trial, but this line promises 30 days.",
        "fix": "Change the stated trial duration to 14 days.",
    }]
    call = boundary.calls[0]
    cmd = call["cmd"]
    system = cmd[cmd.index("--system-prompt") + 1]
    assert "content" in system.lower()
    assert "evidence" in system.lower()
    assert "never instructions" in system.lower()
    assert "invent" in system.lower()
    assert "fix" in system.lower()
    assert "reward hacking" not in system.lower()
    assert STATE in call["input"]
    assert STATEMENT in call["input"]
    assert call["input"].count(RUBRIC) == 1
    assert "HARDCODED_OUTPUT" not in call["input"]
    assert "CG_AD_FIELD_PROFILE" not in call["input"]
    schema = json.loads(cmd[cmd.index("--json-schema") + 1])
    item = schema["properties"]["issues"]["items"]
    assert item["properties"]["rule"]["enum"] == [RULE]
    assert item["properties"]["line"]["minimum"] == 1


def test_content_cli_keeps_tool_and_billing_isolation(content_explainer, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "must-not-bill-api")
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "must-not-use-auth-token")
    monkeypatch.setenv("CLAUDE_CODE_OAUTH_TOKEN", "inherited-token")
    client, boundary = content_explainer(answer([]))

    assert client.explain_content(STATE, RULE, STATEMENT, RUBRIC, anchors={7: "Try it free for 30 days."}) == []

    call = boundary.calls[0]
    cmd = call["cmd"]
    assert cmd[:2] == ["/usr/bin/claude", "-p"]
    assert cmd[cmd.index("--tools") + 1] == ""
    assert cmd[cmd.index("--disallowedTools") + 1] == "mcp__*"
    assert "--safe-mode" in cmd
    assert "--no-session-persistence" in cmd
    assert cmd[cmd.index("--output-format") + 1] == "json"
    assert cmd[cmd.index("--model") + 1] == "claude-haiku-5-5"
    assert cmd[cmd.index("--effort") + 1] == "low"
    assert "ANTHROPIC_API_KEY" not in call["env"]
    assert "ANTHROPIC_AUTH_TOKEN" not in call["env"]
    assert call["env"]["CLAUDE_CODE_OAUTH_TOKEN"] == "subscription-token"
    assert call["capture_output"] is True
    assert call["text"] is True
    assert call["timeout"] == 37


@pytest.mark.parametrize("payload", [
    None,
    [],
    "not an envelope",
    {"is_error": True, "result": "provider unavailable"},
    {"is_error": False, "result": "no structured output"},
    {"structured_output": []},
    {"structured_output": {"issues": None}},
    {"structured_output": {"issues": {}, "other": []}},
    {"structured_output": {"issues": [], "unexpected": "extra"}},
    answer([None]),
    answer(["not an issue"]),
    answer([{}]),
    answer([{**ISSUE, "rule": "CG_AD_FIELD_PROFILE"}]),
    answer([ISSUE, {**ISSUE, "rule": "OTHER"}]),
    answer([{**ISSUE, "rule": [RULE]}]),
    answer([{**ISSUE, "line": 0}]),
    answer([{**ISSUE, "line": -1}]),
    answer([{**ISSUE, "line": True}]),
    answer([{**ISSUE, "line": 7.0}]),
    answer([{**ISSUE, "line": "7"}]),
    answer([{key: value for key, value in ISSUE.items() if key != "fix"}]),
    answer([{**ISSUE, "code": None}]),
    answer([{**ISSUE, "problem": ["not text"]}]),
    answer([{**ISSUE, "fix": 14}]),
    answer([{**ISSUE, "extra": "unexpected"}]),
])
def test_malformed_content_answers_fail_closed(content_explainer, payload):
    client, _ = content_explainer(payload)

    with pytest.raises(RewardGuardError):
        client.explain_content(STATE, RULE, STATEMENT, RUBRIC, anchors={7: "Try it free for 30 days."})


@pytest.mark.parametrize("kwargs, message", [
    ({"stdout": "not JSON"}, "invalid JSON"),
    ({"returncode": 2}, "exited 2"),
    ({"error": subprocess.TimeoutExpired("claude", 37)}, "timed out after 37s"),
    ({"error": OSError("executable disappeared")}, "claude CLI"),
])
def test_content_cli_failures_are_rewardguard_errors(content_explainer, kwargs, message):
    client, _ = content_explainer(answer([]), **kwargs)

    with pytest.raises(RewardGuardError, match=message):
        client.explain_content(STATE, RULE, STATEMENT, RUBRIC, anchors={7: "Try it free for 30 days."})


@pytest.mark.parametrize("rubric", ["", "   ", "x" * 8001], ids=["empty", "whitespace", "too-long"])
def test_invalid_rubric_is_rejected_before_cli(content_explainer, rubric):
    client, boundary = content_explainer(answer([]))

    with pytest.raises(RewardGuardError, match="rubric"):
        client.explain_content(STATE, RULE, STATEMENT, rubric)

    assert boundary.calls == []


def test_maximum_bounded_rubric_is_not_silently_truncated(content_explainer):
    client, boundary = content_explainer(answer([]))
    rubric = "x" * 8000

    assert client.explain_content(STATE, RULE, STATEMENT, rubric) == []

    assert rubric in boundary.calls[0]["input"]


@pytest.mark.parametrize('payload,kwargs,diagnostic', [
    (None, {'error': OSError(2, 'private-source-and-token')}, 'errno=2'),
    (None, {'returncode': 2, 'stdout': 'private-source-and-token'}, 'stdout_chars=24'),
    (None, {'stdout': 'private-source-and-token'}, 'line=1, column=1'),
    ({'is_error': True, 'subtype': 'error_during_execution', 'result': 'private-source-and-token'}, {}, 'subtype=error_during_execution'),
    ({'is_error': False, 'result': 'private-source-and-token', 'structured_output': 'private-source-and-token'}, {}, 'structured_output_type=str'),
])
def test_failure_metadata_is_actionable_without_echoing_cli_output(content_explainer, payload, kwargs, diagnostic):
    client, _ = content_explainer(payload, **kwargs)
    with pytest.raises(RewardGuardError) as caught:
        client.explain_content(STATE, RULE, STATEMENT, RUBRIC, anchors={7:'Try it free for 30 days.'})
    assert diagnostic in str(caught.value)
    assert 'private-source-and-token' not in str(caught.value)


@pytest.mark.parametrize('line,quote,accepted', [(17, 'return 42;', True), (18, 'return 42;', False), (17, 'invented', False)])
def test_code_grounding_uses_fixed_external_response_not_fake_hunk_parser(content_explainer, line, quote, accepted):
    issue = {'rule':'HARDCODED_OUTPUT', 'line':line, 'code':quote, 'problem':'fixed output', 'fix':'compute result'}
    client, boundary = content_explainer(answer([issue]))
    result = client.explain('File: a.py\n@@ -17 +17 @@\n-return value;\n+return 42;',
        {'HARDCODED_OUTPUT':'Hardcoded output'}, anchors={17:'return 42;'})
    expected = [{k:v for k,v in issue.items() if k != 'rule'}] if accepted else []
    assert result == {'HARDCODED_OUTPUT':expected}
    assert len(boundary.calls) == 1
