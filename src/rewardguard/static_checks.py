"""Deterministic checks: counting and pattern matching. Clear-cut findings (models.CLEAR_CUT) keep the
severity set here; every other finding is graded by Jev afterwards (judge.confirm)."""
from __future__ import annotations

import base64
import binascii
import json
import re
from dataclasses import dataclass

from . import gitops
from .config import CONFIG_FILE, Config
from .globs import match
from .models import FAIL, WARN, Finding

TEST, CONFIG, CHECKER, SNAPSHOT, SOURCE, OTHER, EXCLUDED = (
    "test", "config", "checker", "snapshot", "source", "other", "excluded",
)

_LINE_COMMENT = re.compile(r"(?<![:\"'`\\])//.*$")
_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)

TEST_DECL = re.compile(
    r"(?<![\w.$])(?:it|test|fit|xit|xtest)"
    r"(?:\.(?:only|skip|todo|fixme|fails?|concurrent|sequential|slow|skipIf\([^)]*\)|runIf\([^)]*\)|each\s*\([^)]*\)))*"
    r"\s*\("
)
ASSERTION = re.compile(r"(?<![\w.$])(?:expect(?:\.soft|\.poll)?|assert(?:\.\w+)?)\s*\(")

SKIP = re.compile(
    r"(?<![\w$])(?:it|test|describe|suite|bench)(?:\.\w+)*\.(?:skip|todo|fixme|skipIf|fails?)\b"
    r"|(?<![\w.$])x(?:it|test|describe)\s*\("
)
ONLY = re.compile(r"(?<![\w$])(?:it|test|describe|suite)(?:\.\w+)*\.only\s*\(|(?<![\w.$])f(?:it|describe)\s*\(")
_LITERAL = r"(?:true|false|null|undefined|-?\d+(?:\.\d+)?|'[^']*'|\"[^\"]*\")"
TAUTOLOGY = re.compile(
    # a literal compared with a literal, or checked with an argument-free matcher; both sides are constant
    rf"expect\(\s*{_LITERAL}\s*\)\s*\.\s*(?:not\s*\.\s*)?"
    rf"(?:(?:toBe|toEqual|toStrictEqual)\(\s*{_LITERAL}\s*\)"
    r"|(?:toBeTruthy|toBeFalsy|toBeDefined|toBeUndefined|toBeNull)\(\s*\))"
    r"|expect\(\s*([\w.$\[\]'\"]+)\s*\)\s*\.\s*(?:toBe|toEqual|toStrictEqual)\(\s*\1\s*\)"
    r"|assert(?:\.ok)?\(\s*true\s*\)"
    r"|assert\.(?:equal|strictEqual|deepEqual|deepStrictEqual)\(\s*([\w.$]+)\s*,\s*\2\s*\)"
)
EARLY_EXIT = re.compile(r"process\.exit\(\s*0?\s*\)")
DEAD_BRANCH = re.compile(r"\bif\s*\(\s*(?:false|0|!1)\s*\)")
PASS_NO_TESTS = re.compile(r"passWithNoTests|--pass-with-no-tests")
TYPE_ESCAPE = re.compile(r"@ts-ignore|@ts-nocheck|@ts-expect-error|eslint-disable|\bas\s+any\b|\bas\s+unknown\s+as\b")
EMPTY_CATCH = re.compile(
    r"catch\s*(?:\([^)]*\))?\s*\{\s*\}"
    r"|\.catch\(\s*(?:\(\s*\w*\s*\)|\w+)\s*=>\s*(?:\{\s*\}|undefined|null|\[\]|\{\s*\}\s*)\s*\)"
)
TEST_ENV = re.compile(
    r"process\.env\.(?:NODE_ENV|VITEST\w*|JEST_WORKER_ID|PLAYWRIGHT\w*|CI)\b"
    r"|process\.env\[\s*['\"](?:NODE_ENV|VITEST|JEST_WORKER_ID|CI)['\"]\s*\]"
    r"|import\.meta\.env\.(?:MODE|VITEST|TEST)\b"
    r"|typeof\s+(?:jest|vi|describe|it)\s*!==?\s*['\"]undefined['\"]"
)
MOCK_IN_SOURCE = re.compile(
    r"(?:from|require\()\s*['\"][^'\"]*(?:__mocks__|/mocks?/|/mock|fixtures?|\.mock)[^'\"]*['\"]"
    r"|\b(?:mock|fake|dummy|sample|demo|placeholder)(?:Data|Response|Result|User|Users)\b",
    re.I,
)
COVERAGE_IGNORE = re.compile(r"(?:istanbul|c8|v8)\s+ignore\b")
LOG_SILENCED = re.compile(
    r"console\.(?:error|warn)\s*=(?!=)"
    r"|spyOn\(\s*console\s*,\s*['\"](?:error|warn)['\"]\s*\)\s*\.\s*mockImplementation"
)
TIMEOUT_RAISED = re.compile(
    r"(?:jest|test)\.setTimeout\(|vi\.setConfig\(|\b(?:testTimeout|hookTimeout)\s*:|\{\s*timeout\s*:\s*\d"
)
FIXED_WAIT = re.compile(r"waitForTimeout\(|new\s+Promise\(\s*\(?\s*\w+\s*\)?\s*=>\s*setTimeout\(")
REVIEWER_NOTE = re.compile(
    r"\b(?:reviewer|review bot|grader|checker|rewardguard|reward guard|jev|llm|ai model|language model|"
    r"claude|gpt|copilot|codex|ai reviewer|automated review)\b[^\n]{0,80}?\b(?:ignore|approve|safe|fine|correct|"
    r"pass|skip|allow|not (?:a |an )?(?:issue|problem|hack|bug|cheat))"
    r"|ignore (?:all |any )?(?:previous|prior|above|earlier) instructions"
    r"|(?:note|message|instruction)s? (?:to|for) (?:the )?(?:ai|reviewer|grader|checker|model)",
    re.I,
)


# Credentials in a known token format, a private key, or a URL with an inline password
SECRET = re.compile(
    r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"
    r"|\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"
    r"|\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36}\b|\bgithub_pat_[A-Za-z0-9_]{60,}"
    r"|\bsk-ant-[A-Za-z0-9_-]{20,}|\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}"
    r"|\bxox[abposr]-[A-Za-z0-9-]{10,}"
    r"|\bAIza[0-9A-Za-z_-]{35}\b"
    r"|\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqps?)://[^\s:/@'\"`]+:(?![^@\s]*\$\{)[^@\s/'\"`]{3,}@(?!(?:localhost|127\.0\.0\.1|0\.0\.0\.0)\b)"
)
CREDENTIAL_URL = re.compile(r"://[^/\s@]+@")  # user or token embedded in a URL
_B64_BLOB = re.compile(r"[A-Za-z0-9+/]{40,}={0,2}")

# Agent instruction and harness files: an edit changes what every later agent session is told to do
AGENT_FILES = re.compile(
    r"(?:^|/)(?:AGENTS|CLAUDE|GEMINI)\.md$|(?:^|/)SKILL\.md$|^\.github/copilot-instructions\.md$"
    r"|^\.(?:claude|cursor|gemini|codex|agents|windsurf)/|^\.(?:cursorrules|windsurfrules)$"
)
# Commit hooks, lint and type-check configuration
GATE_FILES = re.compile(
    r"^\.husky/|(?:^|/)\.lintstagedrc|(?:^|/)lint-staged\.config\.|(?:^|/)\.eslintrc|(?:^|/)eslint\.config\."
    r"|(?:^|/)tsconfig[\w.-]*\.json$|(?:^|/)\.pre-commit-config\.yaml$"
)
GATE_BYPASS = re.compile(
    r"\bHUSKY\s*=\s*['\"]?0\b|--no-verify\b|\bcore\.hooksPath\b|\bcontinue-on-error\s*:\s*true\b"
)
# Only meaningful in GATE_FILES: application code has its own options called `strict`
STRICT_OFF = re.compile(r"['\"]?(?:strict|noImplicitAny|strictNullChecks|noEmitOnError)['\"]?\s*:\s*false\b")
DOC_FILE = re.compile(r"\.(?:md|mdx|txt|rst)$", re.I)
ESLINT_RULE_OFF = re.compile(r"['\"][\w@/-]+['\"]\s*:\s*(?:['\"]off['\"]|0)\s*(?:,|$)")

# Reassigning built-ins, test globals or built-in prototypes, or reading the call stack, from application code
MONKEYPATCH = re.compile(
    r"(?<![\w.$])(?:Math|JSON|Date|Number|String|Array|Object|Promise|Reflect|Intl|performance)\.\w+\s*=(?!=)"
    r"|(?<![\w.$])(?:Array|Object|String|Number|Function|Promise|Date|Map|Set|RegExp|Error)\.prototype\.\w+\s*=(?!=)"
    r"|(?<![\w.$])(?:globalThis|global|window)\.(?:Math|JSON|Date|expect|describe|it|test|vi|jest|assert)\s*=(?!=)"
    r"|(?<![\w.$])(?:Date|Math|JSON)\s*=(?!=)"
    r"|Object\.defineProperty\(\s*(?:Math|JSON|Date"
    r"|(?:Array|Object|String|Number|Function|Promise|Date|Map|Set|RegExp|Error)\.prototype)\s*,"
    r"|Object\.defineProperty\(\s*(?:globalThis|global|window)\s*,\s*['\"]"
    r"(?:Math|JSON|Date|expect|describe|it|test|vi|jest|assert)['\"]"
    r"|\bError\.prepareStackTrace\s*=(?!=)"
    r"|\binspect\.stack\(|\bsys\._getframe\(|\bsetattr\(\s*(?:np|numpy|math|builtins|torch|sklearn)\b"
)
# One entry of a literal lookup table: `key: literal,` or a row of literals
_LIT = r"(?:-?\d+(?:\.\d+)?(?:e-?\d+)?|'[^']*'|\"[^\"]*\"|`[^`$]*`|true|false|null)"
TABLE_ROW = re.compile(
    rf"^\s*(?:(?:[\w$]+|'[^']*'|\"[^\"]*\"|\[{_LIT}\])\s*:\s*{_LIT}"
    rf"|\[\s*{_LIT}(?:\s*,\s*{_LIT})*\s*\]|{_LIT}(?:\s*,\s*{_LIT})+)\s*,?\s*$"
)
LITERAL_TABLE_MIN_ROWS = 100
LICENSE_LINE = re.compile(r"\bcopyright\b|SPDX-License-Identifier|\blicensed under\b|\ball rights reserved\b", re.I)
DEP_SECTIONS = ("dependencies", "devDependencies", "optionalDependencies", "peerDependencies")


def find_secret(text: str) -> str | None:
    """'plain' or 'base64' when the text holds a credential, else None. Never returns the credential."""
    if SECRET.search(text):
        return "plain"
    for blob in _B64_BLOB.findall(text):
        try:
            decoded = base64.b64decode(blob + "=" * (-len(blob) % 4), validate=True).decode("utf-8")
        except (binascii.Error, UnicodeDecodeError):
            continue
        if SECRET.search(decoded):
            return "base64"
    return None


def strip_comments(text: str) -> str:
    text = _BLOCK_COMMENT.sub("", text)
    return "\n".join(_LINE_COMMENT.sub("", l) for l in text.splitlines())


def count(pattern: re.Pattern[str], text: str | None) -> int:
    return len(pattern.findall(strip_comments(text))) if text else 0


def classify(path: str, cfg: Config) -> str:
    if match(path, cfg.exclude):
        return EXCLUDED
    if path == CONFIG_FILE or path.startswith(".github/"):
        return CHECKER
    if match(path, cfg.snapshot_globs):
        return SNAPSHOT
    if match(path, cfg.config_globs):
        return CONFIG
    if match(path, cfg.test_globs):
        return TEST
    if match(path, cfg.judge_include):
        return SOURCE
    return OTHER


@dataclass
class StaticContext:
    repo: str
    base: str
    head: str
    cfg: Config


def _f(ctx: StaticContext, rule: str, default: str, message: str, file=None, line=None, evidence=None):
    sev = ctx.cfg.severity(rule, default)
    if sev == "off":
        return None
    return Finding(rule, sev, message, file=file, line=line, source="static",
                   evidence=(evidence.strip()[:200] if evidence else None))


def _package_json_findings(ctx: StaticContext, path: str) -> list[Finding]:
    def load(commit):
        text = gitops.show_file(ctx.repo, commit, path)
        if text is None:
            return {}
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"__invalid__": True}

    old, new = load(ctx.base), load(ctx.head)
    out = []
    old_s, new_s = old.get("scripts", {}) or {}, new.get("scripts", {}) or {}
    for key in sorted(set(old_s) | set(new_s)):
        if re.search(r"test|e2e|spec|vitest|jest|playwright|^ci$|check", key) and old_s.get(key) != new_s.get(key):
            out.append(_f(ctx, "TEST_SCRIPT_CHANGED", FAIL,
                          f"package.json script '{key}' changed: {old_s.get(key)!r} -> {new_s.get(key)!r}", file=path))
    for key in ("jest", "vitest"):
        if old.get(key) != new.get(key):
            out.append(_f(ctx, "CONFIG_CHANGED", FAIL, f"package.json '{key}' config block changed", file=path))
    for section in ("dependencies", "devDependencies"):
        old_d, new_d = old.get(section, {}) or {}, new.get(section, {}) or {}
        for name in sorted(set(old_d) & set(new_d)):
            old_v, new_v = _version(old_d[name]), _version(new_d[name])
            if old_v and new_v and new_v < old_v:
                out.append(_f(ctx, "DEPENDENCY_DOWNGRADE", WARN,
                              f"{section} '{name}' downgraded: {old_d[name]} -> {new_d[name]}", file=path))
    for section in DEP_SECTIONS:
        old_d, new_d = old.get(section, {}) or {}, new.get(section, {}) or {}
        known = set().union(*((old.get(s, {}) or {}) for s in DEP_SECTIONS))
        for name in sorted(set(new_d) - set(old_d) - known):
            spec = str(new_d[name])
            shown = "spec redacted: it holds a credential" if find_secret(spec) or CREDENTIAL_URL.search(spec) else spec
            out.append(_f(ctx, "NEW_DEPENDENCY", WARN,
                          f"{section} '{name}' added ({shown}); check the name is the package you meant",
                          file=path))
    return [f for f in out if f]


def _version(spec: str) -> tuple[int, ...]:
    m = re.search(r"\d+(?:\.\d+)*", str(spec))
    return tuple(int(x) for x in m.group(0).split(".")) if m else ()


def run(ctx: StaticContext, changed: list[gitops.ChangedFile]) -> tuple[list[Finding], dict[str, str]]:
    """Returns findings and a map of path -> classification (for the judge)."""
    findings: list[Finding] = []
    kinds: dict[str, str] = {}
    tests_before = tests_after = asserts_before = asserts_after = 0

    deleted: list[str] = []

    def add(f):
        if f:
            findings.append(f)

    for cf in changed:
        kind = classify(cf.path, ctx.cfg)
        kinds[cf.path] = kind
        if kind == EXCLUDED:
            continue

        if AGENT_FILES.search(cf.path):
            add(_f(ctx, "AGENT_INSTRUCTIONS_CHANGED", WARN,
                   "Agent instruction or harness file changed; later agent sessions follow it", file=cf.path))
        if GATE_FILES.search(cf.path):
            add(_f(ctx, "GATE_CONFIG_WEAKENED", WARN, "Commit hook, lint or type-check configuration changed",
                   file=cf.path))
        if cf.status == "D" and kind in (SOURCE, OTHER, CHECKER):
            deleted.append(cf.path)

        if kind == TEST:
            old_text = None if cf.status == "A" else gitops.show_file(ctx.repo, ctx.base, cf.old_path or cf.path)
            new_text = None if cf.status == "D" else gitops.show_file(ctx.repo, ctx.head, cf.path)
            tests_before += count(TEST_DECL, old_text)
            tests_after += count(TEST_DECL, new_text)
            asserts_before += count(ASSERTION, old_text)
            asserts_after += count(ASSERTION, new_text)
            if cf.status == "D":
                add(_f(ctx, "TEST_FILE_DELETED", FAIL,
                       f"Test file deleted ({count(TEST_DECL, old_text)} tests removed)", file=cf.path))
                continue

        # CI workflows and .rewardguard.toml (kind CHECKER) are not flagged: CI sometimes has to change,
        # and the config is read from base, so a branch's edits to it only apply once merged
        if kind == CONFIG:
            add(_f(ctx, "CONFIG_CHANGED", FAIL, "Test runner configuration changed", file=cf.path))
        elif kind == SNAPSHOT and cf.status in ("M", "D"):
            add(_f(ctx, "SNAPSHOT_CHANGED", WARN,
                   "Snapshot updated or deleted; expected output changed", file=cf.path))

        if cf.path.endswith("package.json"):
            findings.extend(_package_json_findings(ctx, cf.path))

        if cf.status == "D":
            continue

        table_rows, table_line = 0, None
        for hunk in gitops.file_hunks(ctx.repo, ctx.base, ctx.head, cf.path, 0, cf.old_path):
            for lineno, raw in hunk.added:
                code = strip_comments(raw)
                secret = find_secret(raw)
                # the report must not repeat a credential, whichever rule matches its line
                loc = dict(file=cf.path, line=lineno, evidence=None if secret else raw)
                if secret:
                    add(_f(ctx, "SECRET_ADDED", FAIL, f"Credential added to the repository ({secret})", **loc))
                gate_file = GATE_FILES.search(cf.path)
                if (GATE_BYPASS.search(code) and not DOC_FILE.search(cf.path)) or (gate_file and (
                        STRICT_OFF.search(code) or ("eslint" in cf.path and ESLINT_RULE_OFF.search(code)))):
                    add(_f(ctx, "GATE_CONFIG_WEAKENED", FAIL,
                           "Commit hook, CI step, lint rule or type-check strictness turned off", **loc))
                if kind == SOURCE and MONKEYPATCH.search(code):
                    add(_f(ctx, "RUNTIME_MONKEYPATCH", FAIL,
                           "Built-in, test global or call stack reached into from application code", **loc))
                if kind == SOURCE and TABLE_ROW.match(code):
                    table_rows += 1
                    table_line = table_line or lineno
                if REVIEWER_NOTE.search(raw):
                    add(_f(ctx, "REVIEWER_NOTE", FAIL, "Text addressed to a reviewer/grader/AI", **loc))
                if PASS_NO_TESTS.search(code):
                    add(_f(ctx, "PASS_WITH_NO_TESTS", FAIL, "Allows a run with zero tests to pass", **loc))
                if kind in (TEST, CONFIG):
                    if SKIP.search(code):
                        add(_f(ctx, "SKIP_ADDED", FAIL, "Test skipped, marked todo/fixme, or expected to fail", **loc))
                    if ONLY.search(code):
                        add(_f(ctx, "ONLY_ADDED", FAIL, ".only/fit added; other tests stop running", **loc))
                    if TAUTOLOGY.search(code):
                        add(_f(ctx, "TAUTOLOGICAL_ASSERTION", FAIL, "Assertion that cannot fail", **loc))
                    if EARLY_EXIT.search(code):
                        add(_f(ctx, "EARLY_EXIT", FAIL, "process.exit added to test code", **loc))
                    if DEAD_BRANCH.search(code):
                        add(_f(ctx, "DEAD_BRANCH", FAIL, "Unreachable branch in test code", **loc))
                if kind == SOURCE:
                    if DEAD_BRANCH.search(code):
                        add(_f(ctx, "DEAD_BRANCH", WARN, "Unreachable branch added", **loc))
                    if TEST_ENV.search(code):
                        add(_f(ctx, "TEST_ENV_BRANCH", WARN, "Source code checks whether tests are running", **loc))
                    if MOCK_IN_SOURCE.search(code):
                        add(_f(ctx, "MOCK_IN_SOURCE", WARN, "Mock/demo/fixture data referenced from non-test code", **loc))
                if kind in (SOURCE, TEST) and TYPE_ESCAPE.search(raw):
                    add(_f(ctx, "TYPE_ESCAPE", WARN, "Type checker or linter silenced", **loc))
                if kind in (SOURCE, TEST) and COVERAGE_IGNORE.search(raw):
                    add(_f(ctx, "COVERAGE_IGNORE", WARN, "Coverage ignore comment added", **loc))
                if kind in (SOURCE, TEST, CONFIG) and LOG_SILENCED.search(code):
                    add(_f(ctx, "LOG_SILENCED", WARN, "console.error/warn replaced or silenced", **loc))
                if kind in (TEST, CONFIG) and TIMEOUT_RAISED.search(code):
                    add(_f(ctx, "TIMEOUT_CHANGED", WARN, "Test timeout set or raised", **loc))
                if kind == TEST and FIXED_WAIT.search(code):
                    add(_f(ctx, "FIXED_WAIT", WARN, "Fixed wait added to a test", **loc))
            added_code = strip_comments("\n".join(t for _, t in hunk.added))
            if kind in (SOURCE, TEST) and EMPTY_CATCH.search(added_code):
                add(_f(ctx, "EMPTY_CATCH", WARN, "Error caught and discarded", file=cf.path,
                       line=hunk.added[0][0] if hunk.added else None))
            added_text = {t.strip() for _, t in hunk.added}
            for gone in hunk.removed:
                if LICENSE_LINE.search(gone) and gone.strip() not in added_text:
                    add(_f(ctx, "LICENSE_HEADER_REMOVED", WARN, "Copyright or licence notice removed",
                           file=cf.path, evidence=None if find_secret(gone) else gone))
                    break
        if table_rows >= LITERAL_TABLE_MIN_ROWS:
            add(_f(ctx, "LARGE_LITERAL_TABLE", WARN,
                   f"{table_rows} lines of literal lookup data added to application code", file=cf.path,
                   line=table_line))

    if deleted:
        shown = ", ".join(deleted[:5]) + (f" and {len(deleted) - 5} more" if len(deleted) > 5 else "")
        add(_f(ctx, "NON_TEST_FILES_DELETED", WARN, f"{len(deleted)} non-test file(s) deleted: {shown}"))
    if tests_after < tests_before:
        add(_f(ctx, "TEST_COUNT_DROP", FAIL,
               f"Net test count across changed test files dropped {tests_before} -> {tests_after}"))
    if asserts_after < asserts_before:
        add(_f(ctx, "ASSERTION_COUNT_DROP", WARN,
               f"Net assertion count across changed test files dropped {asserts_before} -> {asserts_after}"))
    return findings, kinds
