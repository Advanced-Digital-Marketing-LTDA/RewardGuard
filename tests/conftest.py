from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

FIXTURE = Path(__file__).parent / "fixtures" / "sample"


def sh(cwd, *cmd):
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True).stdout


@pytest.fixture(scope="session")
def node_modules(tmp_path_factory) -> Path:
    """Install the sample project's dependencies once; every checkout symlinks to them."""
    d = tmp_path_factory.mktemp("deps")
    shutil.copy(FIXTURE / "package.json", d)
    shutil.copy(FIXTURE / "package-lock.json", d)
    sh(d, "npm", "ci", "--no-audit", "--no-fund")
    return d / "node_modules"


class SampleRepo:
    def __init__(self, path: Path, node_modules: Path):
        self.path = path
        shutil.copytree(FIXTURE, path, ignore=shutil.ignore_patterns("node_modules"))
        (path / ".rewardguard.toml").write_text(
            f'install = "ln -s {node_modules} node_modules"\n\n'
            "[[suites]]\n"
            'name = "unit"\n'
            'command = "./node_modules/.bin/vitest run --reporter=json --outputFile={report}"\n\n'
            "[judge]\nconcurrency = 2\n"
        )
        (path / ".gitignore").write_text("node_modules\n")
        sh(path, "git", "init", "-q", "-b", "main")
        sh(path, "git", "config", "user.email", "t@example.com")
        sh(path, "git", "config", "user.name", "t")
        sh(path, "git", "add", "-A")
        sh(path, "git", "commit", "-qm", "base")

    def branch(self, name: str, files: dict[str, str | None]) -> None:
        sh(self.path, "git", "checkout", "-q", "-B", name, "main")
        for rel, content in files.items():
            p = self.path / rel
            if content is None:
                p.unlink()
            else:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(content)
        sh(self.path, "git", "add", "-A")
        sh(self.path, "git", "commit", "-qm", name)

    def read(self, rel: str) -> str:
        return (self.path / rel).read_text()


@pytest.fixture
def sample_repo(tmp_path, node_modules) -> SampleRepo:
    return SampleRepo(tmp_path / "repo", node_modules)


class FakeJev:
    """Stands in for the Jev HTTP API. `rules` maps (question_key, substring_in_state) -> probability."""

    def __init__(self, rules=None, status=200, raw=None):
        self.rules = rules or {}
        self.status = status
        self.raw = raw
        self.calls: list[dict] = []

    def __call__(self, req, timeout=None):
        import io
        import urllib.error

        body = json.loads(req.data.decode())
        self.calls.append(body)
        if self.status != 200:
            raise urllib.error.HTTPError(req.full_url, self.status, "err", {}, io.BytesIO(b'{"error":"x"}'))
        if self.raw is not None:
            payload = self.raw
        else:
            answers = {}
            for key in body["questions"]:
                p = 0.02
                for (k, needle), prob in self.rules.items():
                    if k == key and needle in body["state"]:
                        p = max(p, prob)
                answers[key] = {"type": "noul", "noul": p}
            payload = {"model": "jev-1.13.0", "answers": answers, "usage": {"input_tokens": 1, "output_tokens": 0}}

        class Resp(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        return Resp(json.dumps(payload).encode())


class FakeHaiku:
    """Stands in for `claude -p` (replaces rewardguard.explainer._run). By default returns one issue per
    flagged statement. `payload` replaces the CLI's JSON output; `returncode` simulates a CLI failure."""

    def __init__(self, payload=None, returncode=0, stdout=None):
        self.payload = payload
        self.returncode = returncode
        self.stdout = stdout
        self.calls: list[dict] = []

    def __call__(self, cmd, input=None, env=None, **kwargs):
        import subprocess

        self.calls.append({"cmd": cmd, "input": input, "env": env})
        if self.stdout is not None:
            out = self.stdout
        elif self.payload is not None:
            out = json.dumps(self.payload)
        else:
            flagged = re.findall(r"^- ([A-Z_]+):", input, re.M)
            out = json.dumps({"type": "result", "is_error": False, "result": "", "structured_output": {"issues": [
                {"rule": r, "line": 3, "code": "x", "problem": f"{r} problem", "fix": "fix it"} for r in flagged
            ]}})
        return subprocess.CompletedProcess(cmd, self.returncode, out, "cli failed" if self.returncode else "")


@pytest.fixture
def fake_haiku(monkeypatch):
    monkeypatch.setenv("CLAUDE_CODE_OAUTH_TOKEN", "test-token")
    monkeypatch.setattr("rewardguard.explainer._which", lambda name: "/usr/bin/claude")

    def install(**kwargs) -> FakeHaiku:
        fh = FakeHaiku(**kwargs)
        monkeypatch.setattr("rewardguard.explainer._run", fh)
        return fh

    return install


@pytest.fixture
def fake_jev(monkeypatch, fake_haiku):
    """Fakes Jev, and Haiku with its default answers (call fake_haiku again to change them)."""
    monkeypatch.setenv("TYPESAFE_API_KEY", "test-key")
    fake_haiku()

    def install(**kwargs) -> FakeJev:
        fj = FakeJev(**kwargs)
        monkeypatch.setattr("rewardguard.judge.urllib.request.urlopen", fj)
        return fj

    return install
