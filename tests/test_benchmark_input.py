import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts import benchmark_content_payload as benchmark


def git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


@pytest.fixture
def benchmark_repo(tmp_path):
    repo = tmp_path / 'repo'
    repo.mkdir()
    git(repo, 'init', '-q', '-b', 'main')
    git(repo, 'config', 'user.name', 'Test')
    git(repo, 'config', 'user.email', 'test@example.test')
    (repo / '.rewardguard.toml').write_text('run_tests = false\n[content]\npacks = ["writing"]\n')
    (repo / 'page.md').write_text('# Old\nPrevious public copy.\n')
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'base')
    base = git(repo, 'rev-parse', 'HEAD')
    (repo / 'page.md').write_text('# New\nChanged public copy.\n')
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'change')
    return repo, base, git(repo, 'rev-parse', 'HEAD')


def run_benchmark(repo, base, head, *args, stdin=b''):
    script = Path(__file__).parents[1] / 'scripts' / 'benchmark_content_payload.py'
    return subprocess.run([sys.executable, str(script), str(repo), base, head, *args],
                          input=stdin, capture_output=True, timeout=20)


def test_stdin_is_explicit_bounded_and_utf8():
    assert benchmark.read_description(io.BytesIO(b'x' * 256_000)) == 'x' * 256_000
    assert benchmark.read_description(io.BytesIO('é'.encode() * 128_000)) == 'é' * 128_000
    with pytest.raises(SystemExit, match='exceeds'):
        benchmark.read_description(io.BytesIO(b'x' * 256_001))
    with pytest.raises(SystemExit, match='UTF-8'):
        benchmark.read_description(io.BytesIO(b'\xff'))


def test_default_does_not_read_stdin(monkeypatch, capsys):
    class NoInput:
        @property
        def buffer(self):
            raise AssertionError('stdin read without explicit opt-in')

    result = ({'serialized_body_bytes': 0}, {'coverage': []}, {})
    monkeypatch.setattr(benchmark.sys, 'argv', ['benchmark', '.', 'base', 'head'])
    monkeypatch.setattr(benchmark.sys, 'stdin', NoInput())
    monkeypatch.setattr(benchmark, 'exercise', lambda *_: result)
    benchmark.main()
    assert json.loads(capsys.readouterr().out)['offline_questions_equal']


def test_explicit_stdin_accepts_operator_selected_context(benchmark_repo, tmp_path):
    repo, base, head = benchmark_repo
    outside = tmp_path / 'outside-context.txt'
    outside.write_text('Private context stays in the local benchmark.\n')
    link = repo / 'operator-selected-link'
    link.symlink_to(outside)
    result = run_benchmark(repo, base, head, '--description-stdin', stdin=link.read_bytes())
    assert result.returncode == 0, result.stderr.decode()
    output = json.loads(result.stdout)
    assert output['offline_questions_equal'] and output['offline_coverage_provenance_omissions_equal']
    assert b'Private context' not in result.stdout + result.stderr


def test_legacy_paths_traversal_and_symlinks_are_not_opened(benchmark_repo, tmp_path):
    repo, base, head = benchmark_repo
    outside = tmp_path / 'secret.txt'
    outside.write_text('never display this file')
    link = repo / 'context-link'
    link.symlink_to(outside)
    for argument in (str(outside), str(link), '../secret.txt'):
        result = run_benchmark(repo, base, head, argument)
        assert result.returncode != 0
        assert b'never display this file' not in result.stdout + result.stderr
        assert b'--description-stdin' in result.stderr
