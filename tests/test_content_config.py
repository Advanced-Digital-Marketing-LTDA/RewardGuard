from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from rewardguard import config, globs
from rewardguard.models import RewardGuardError


def test_content_defaults_are_enabled_with_trusted_context():
    content = config.parse("run_tests = false\n").content

    assert content.enabled is True
    assert content.packs == []
    assert content.context == {
        "B": [".rewardguard/content-context.md"],
        "P": [".rewardguard/content-policy.md", ".rewardguard/content-policy.json"],
        "I": [".rewardguard/content-inventory.md", ".rewardguard/content-inventory.json"],
        "S": [".rewardguard/content-sources.md", ".rewardguard/content-sources.json"],
        "R": [".rewardguard/content-rendered.md", ".rewardguard/content-rendered.json"],
        "M": [".rewardguard/content-measurements.md", ".rewardguard/content-measurements.json"],
        "H": [".rewardguard/content-history.md", ".rewardguard/content-history.json"],
    }


@pytest.mark.parametrize("path", [
    "README.md", "guides/intro.mdx", "public/index.html", "src/pages/index.astro",
    "src/Page.vue", "src/Page.svelte", "src/Page.jsx", "src/Page.tsx",
    "content/home.json", "src/locales/pt-BR.json", "src/i18n/en.yaml",
    "src/translations/es.yml", "src/messages/en.json", "content/intro.txt",
    "src/content/intro.text", "public/robots.txt", "app/robots.ts",
    "public/sitemap.xml", "public/sitemap_index.xml", "app/sitemap.ts",
    "src/metadata.ts", "src/seo.json", "src/seo/defaults.ts", "_redirects",
    "public/_redirects", "config/redirects.json",
])
def test_default_include_covers_content_and_seo_controls(path):
    assert globs.match(path, config.parse("run_tests = false\n").content.include)


@pytest.mark.parametrize("path", ["src/copy.js", "src/copy.ts", "lib/copy.mjs", "lib/copy.cts"])
def test_ambiguous_source_strings_have_a_separate_include(path):
    content = config.parse("run_tests = false\n").content

    assert globs.match(path, content.source_include)
    assert not globs.match(path, content.include)


@pytest.mark.parametrize("path", [
    "node_modules/package/README.md", "vendor/page.html", "dist/index.html",
    "build/index.html", "coverage/index.html", ".next/server/page.html",
    ".svelte-kit/output/page.html", "tests/page.md", "__tests__/copy.ts",
    "src/page.test.tsx", "e2e/page.ts", "package-lock.json", "pnpm-lock.yaml",
    "yarn.lock", "bun.lock", "uv.lock",
])
def test_default_exclude_keeps_generated_vendor_test_and_lock_paths_out(path):
    assert globs.match(path, config.parse("run_tests = false\n").content.exclude)


def test_content_overrides_replace_lists_and_merge_context_codes():
    content = config.parse('''run_tests = false
[content]
enabled = false
include = ["articles/**/*.md"]
source_include = ["src/copy/**/*.ts"]
exclude = ["articles/drafts/**"]
packs = ["writing", "pricing"]
[content.context]
B = ["docs/product.md"]
P = []
''').content

    assert content.enabled is False
    assert content.include == ["articles/**/*.md"]
    assert content.source_include == ["src/copy/**/*.ts"]
    assert content.exclude == ["articles/drafts/**"]
    assert content.packs == ["writing", "pricing"]
    assert content.context["B"] == ["docs/product.md"]
    assert content.context["P"] == []
    assert content.context["I"] == [
        ".rewardguard/content-inventory.md", ".rewardguard/content-inventory.json",
    ]


def test_explicit_empty_content_lists_are_not_replaced_with_defaults():
    content = config.parse('''run_tests = false
[content]
include = []
source_include = []
exclude = []
packs = []
''').content

    assert content.include == []
    assert content.source_include == []
    assert content.exclude == []
    assert content.packs == []


def test_content_defaults_are_independent_between_configurations():
    first = config.Config(install=None, suites=[]).content
    second = config.Config(install=None, suites=[]).content
    parsed = config.parse("run_tests = false\n").content
    untouched = config.parse("run_tests = false\n").content
    for content in (first, parsed):
        content.include.clear()
        content.source_include.clear()
        content.exclude.clear()
        content.packs.append("pricing")
        content.context["B"].clear()

    for content in (second, untouched):
        assert globs.match("README.md", content.include)
        assert globs.match("src/copy.ts", content.source_include)
        assert globs.match("dist/index.html", content.exclude)
        assert content.packs == []
        assert content.context["B"] == [
            ".rewardguard/content-context.md",
        ]


@pytest.mark.parametrize("fragment", [
    'content = false', 'content = "enabled"', 'content = []',
    '[content]\nenabled = "false"', '[content]\nenabled = 0',
    '[content]\ninclude = "docs/**"', '[content]\ninclude = [1]',
    '[content]\nsource_include = false', '[content]\nsource_include = [true]',
    '[content]\nexclude = {}', '[content]\nexclude = [1]',
    '[content]\npacks = "writing"', '[content]\npacks = [true]',
    '[content]\ncontext = false', '[content]\ncontext = []',
    '[content.context]\nB = "docs/product.md"', '[content.context]\nB = [1]',
    '[content.context]\nX = []', '[content.context]\nb = []',
    '[content]\nenabeld = false', '[content]\nwarn_at = 0.1',
    '[content.thresholds]\nfail = 0.1',
])
def test_malformed_content_settings_raise_config_errors(fragment):
    with pytest.raises(RewardGuardError, match="content"):
        config.parse("run_tests = false\n" + fragment + "\n")


@pytest.mark.parametrize("setting", ["include", "source_include", "exclude", "context"])
@pytest.mark.parametrize("path", [
    "", " ", "/tmp/proof.md", "../proof.md", "docs/../proof.md",
    "C:/proof.md", "C:proof.md", r"C:\proof.md", r"\\server\proof.md",
    r"docs\..\proof.md", "**/{..,docs}/**", "docs/\0proof.md",
])
def test_content_paths_cannot_escape_the_repository(setting, path):
    if setting == "context":
        fragment = "[content.context]\nB"
    else:
        fragment = f"[content]\n{setting}"
    text = "run_tests = false\n" + fragment + " = [" + json.dumps(path) + "]\n"

    with pytest.raises(RewardGuardError, match="content"):
        config.parse(text)


def test_relative_paths_can_contain_spaces_dots_and_glob_alternatives():
    content = config.parse('''run_tests = false
[content]
include = ["./docs/**/*.md", "content/**/*.{json,yaml}", "release..md"]
[content.context]
S = ["docs/source files/evidence.md"]
''').content

    assert content.include == ["./docs/**/*.md", "content/**/*.{json,yaml}", "release..md"]
    assert content.context["S"] == ["docs/source files/evidence.md"]


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True,
    ).stdout.strip()


@pytest.fixture
def content_repo(tmp_path):
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "config", "user.name", "Config test")
    _git(tmp_path, "config", "user.email", "config@example.test")
    (tmp_path / "README.md").write_text("base\n")
    _git(tmp_path, "add", "README.md")
    _git(tmp_path, "commit", "-qm", "base")
    return tmp_path


def test_missing_project_config_gets_content_defaults(content_repo):
    base = _git(content_repo, "rev-parse", "HEAD")

    cfg = config.load_from_commit(str(content_repo), base, allow_missing=True)

    assert cfg.content.enabled is True
    assert cfg.content.context["B"] == [
        ".rewardguard/content-context.md",
    ]
    assert cfg.run_tests is False


def test_content_policy_is_loaded_from_the_requested_base_commit(content_repo):
    path = content_repo / ".rewardguard.toml"
    path.write_text('''run_tests = false
[content]
enabled = true
packs = ["pricing"]
[content.context]
B = ["docs/trusted-product.md"]
''')
    _git(content_repo, "add", ".rewardguard.toml")
    _git(content_repo, "commit", "-qm", "trusted config")
    base = _git(content_repo, "rev-parse", "HEAD")
    path.write_text('''run_tests = false
[content]
enabled = false
packs = []
[content.context]
B = ["../untrusted.md"]
''')

    cfg = config.load_from_commit(str(content_repo), base)

    assert cfg.content.enabled is True
    assert cfg.content.packs == ["pricing"]
    assert cfg.content.context["B"] == ["docs/trusted-product.md"]


def test_content_configuration_cannot_change_probability_thresholds():
    with pytest.raises(RewardGuardError, match=r"\[thresholds\] is no longer configurable"):
        config.parse("run_tests = false\n[content]\nenabled = false\n[thresholds]\nwarn = 0.1\n")
