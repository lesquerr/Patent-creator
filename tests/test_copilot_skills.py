"""Contract tests for the native GitHub Copilot skill migration."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SKILLS = ROOT / "skills"
COPILOT_SKILLS = ROOT / ".github" / "skills"
EXPECTED_SKILLS = {
    "bigquery-patent-search",
    "development-assistant",
    "epc-search",
    "epo-patent-analyzer",
    "epo-patent-search",
    "index-manager",
    "mpep-search",
    "patent-application-creator",
    "patent-claims-analyzer",
    "patent-diagram-generator",
    "patent-reviewer",
    "patent-search",
    "pct-application",
    "prior-art-search",
    "setup-assistant",
    "testing-assistant",
    "troubleshooting-assistant",
}
EXPECTED_RESOURCES = {
    "bigquery-patent-search": {"SKILL.md"},
    "development-assistant": {"SKILL.md"},
    "epc-search": {"SKILL.md"},
    "epo-patent-analyzer": {"SKILL.md"},
    "epo-patent-search": {"SKILL.md"},
    "index-manager": {"SKILL.md"},
    "mpep-search": {"SKILL.md", "mpep_search.py"},
    "patent-application-creator": {"SKILL.md"},
    "patent-claims-analyzer": {"SKILL.md"},
    "patent-diagram-generator": {"SKILL.md"},
    "patent-reviewer": {"SKILL.md"},
    "patent-search": {"SKILL.md"},
    "pct-application": {"SKILL.md"},
    "prior-art-search": {"SKILL.md", "prior_art_types.py"},
    "setup-assistant": {"SKILL.md", "filing-reference.md"},
    "testing-assistant": {"SKILL.md"},
    "troubleshooting-assistant": {"SKILL.md"},
}


def _read_frontmatter(path: Path) -> tuple[str, str]:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", content, re.DOTALL)
    assert match, f"{path} must start with YAML frontmatter"
    fields = {}
    for line in match.group(1).splitlines():
        field = re.fullmatch(r"(name|description): (.+)", line)
        assert field, f"Unsupported or missing frontmatter field in {path}: {line}"
        fields[field.group(1)] = field.group(2)
    assert set(fields) == {"name", "description"}
    assert fields["description"].startswith('"') and fields["description"].endswith('"')
    return fields["name"], json.loads(fields["description"])


def test_all_original_skills_and_resources_are_migrated():
    assert {path.name for path in SOURCE_SKILLS.iterdir() if path.is_dir()} == EXPECTED_SKILLS

    for skill_name in EXPECTED_SKILLS:
        source = SOURCE_SKILLS / skill_name
        target = COPILOT_SKILLS / skill_name
        assert target.is_dir(), f"Missing Copilot skill: {skill_name}"
        source_resources = {
            path.relative_to(source) for path in source.rglob("*") if path.is_file()
        }
        target_resources = {
            path.relative_to(target) for path in target.rglob("*") if path.is_file()
        }
        assert {path.as_posix() for path in source_resources} == EXPECTED_RESOURCES[skill_name]
        assert source_resources == target_resources, f"Resource inventory changed for {skill_name}"
        assert Path("SKILL.md") in target_resources


def test_copilot_skill_frontmatter_is_valid_and_unique():
    assert COPILOT_SKILLS.is_dir(), "Copilot skill directory has not been migrated"
    names = []
    for skill_name in EXPECTED_SKILLS:
        skill_dir = COPILOT_SKILLS / skill_name
        skill_path = skill_dir / "SKILL.md"
        name, description = _read_frontmatter(skill_path)
        assert name == skill_dir.name
        assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
        assert description.strip()
        names.append(name)
    assert len(names) == len(set(names))


def test_migrated_skills_do_not_depend_on_claude_only_or_unix_conventions():
    forbidden = re.compile(
        r"CLAUDE_PLUGIN_ROOT|claude mcp\s+(?:add|remove|list)|"
        r"```bash|source venv/bin|sudo apt|brew install|"
        r"\bTask\s*\(",
        re.IGNORECASE,
    )
    for skill_name in EXPECTED_SKILLS:
        for path in (COPILOT_SKILLS / skill_name).rglob("*"):
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                assert not forbidden.search(text), f"Legacy platform assumption in {path}"


def test_migrated_skills_use_the_attached_mcp_server():
    assert COPILOT_SKILLS.is_dir(), "Copilot skill directory has not been migrated"
    forbidden = re.compile(
        r"native_tools|--skip-mcp\b|--describe\b|--list\b|"
        r"mcp__[A-Za-z0-9_]+|transport[- ]free runner|"
        r"(?:search_mpep|TOOL)\s+--input",
        re.IGNORECASE,
    )
    required_guidance = (
        "patent-creator",
        "/mcp",
        "restart copilot",
        "named arguments",
        "schema",
        "aliases vary",
    )
    for skill_name in EXPECTED_SKILLS:
        for path in (COPILOT_SKILLS / skill_name).rglob("*"):
            if not path.is_file():
                continue
            content = path.read_text(encoding="utf-8")
            assert not forbidden.search(content), f"Obsolete MCP execution path in {path}"

        content = (COPILOT_SKILLS / skill_name / "SKILL.md").read_text(encoding="utf-8").lower()
        for phrase in required_guidance:
            assert phrase in content, f"Missing attached MCP guidance ({phrase}) in {skill_name}"
        assert "mcp__" not in content, f"Do not hard-code runtime MCP aliases in {skill_name}"

    mpep_skill = (COPILOT_SKILLS / "mpep-search" / "SKILL.md").read_text(encoding="utf-8")
    assert "mpep://index/stats" in mpep_skill
    helper = (COPILOT_SKILLS / "mpep-search" / "mpep_search.py").read_text(encoding="utf-8")
    assert "Implementation reference" in helper
    assert "attached MCP" in helper


def test_setup_guidance_preserves_python_setup_and_explains_index_prerequisites():
    content = (COPILOT_SKILLS / "setup-assistant" / "SKILL.md").read_text(encoding="utf-8")
    assert ".venv\\Scripts\\python.exe -m mcp_server.cli download-all" in content
    assert ".venv\\Scripts\\python.exe -m mcp_server.cli rebuild-index" in content
    assert ".venv\\Scripts\\python.exe -m mcp_server.cli health" in content
    assert "35 USC" in content and "37 CFR" in content
    assert "subsequent updates" in content and "EPO/PCT" in content
    assert "do not also run `download-mpep`" in content
    assert "Claude" in content and "registration" in content
    assert "restart Copilot" in content
    assert "`/mcp`" in content
    assert "PDF" in content and "index" in content
    assert "only starts when" in content


def test_index_manager_uses_cli_download_and_never_builds_via_server_loop():
    content = (COPILOT_SKILLS / "index-manager" / "SKILL.md").read_text(encoding="utf-8")
    assert ".venv\\Scripts\\python.exe -m mcp_server.cli download-all" in content
    assert ".venv\\Scripts\\python.exe -m mcp_server.cli rebuild-index" in content
    assert ".venv\\Scripts\\python.exe -m mcp_server.cli health" in content
    assert "mcp_server\\server.py" not in content


def test_bigquery_guidance_gates_billable_queries_and_prefers_status_checks():
    content = (
        (COPILOT_SKILLS / "bigquery-patent-search" / "SKILL.md").read_text(encoding="utf-8").lower()
    )
    assert "free to query" not in content
    assert "user approval" in content
    assert "check_bigquery_status" in content
    assert "test_bigquery.py" in content
    assert "before each" in content
    assert "charges" in content
