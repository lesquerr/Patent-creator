"""Offline contract checks for Copilot profiles using the unchanged MCP server."""

import ast
import json
import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
ORIGINALS = ROOT / "agents"
PROFILES = ROOT / ".github" / "agents"
NAMES = sorted(path.stem for path in ORIGINALS.glob("*.md"))
ALIASES = {"execute", "read", "edit", "search", "agent", "web"}


def read_profile(name):
    path = PROFILES / f"{name}.agent.md"
    assert path.is_file(), f"Missing native profile: {path.name}"
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    assert len(parts) == 3 and not parts[0].strip(), path.name
    return yaml.safe_load(parts[1]), parts[2]


def registered_parameters():
    parameters = {}
    for path in (ROOT / "mcp_server" / "tools").glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if any(
                isinstance(decorator, ast.Call)
                and isinstance(decorator.func, ast.Attribute)
                and decorator.func.attr == "tool"
                for decorator in node.decorator_list
            ):
                parameters[node.name] = {arg.arg for arg in node.args.args}
    return parameters


def test_all_thirteen_agents_have_native_profiles():
    assert len(NAMES) == 13
    assert sorted(path.name for path in PROFILES.glob("*.agent.md")) == [
        f"{name}.agent.md" for name in NAMES
    ]


@pytest.mark.parametrize("name", NAMES)
def test_frontmatter_uses_native_aliases_and_session_model(name):
    frontmatter, body = read_profile(name)
    assert isinstance(frontmatter["description"], str)
    assert frontmatter["description"].strip()
    assert frontmatter.get("name", name) == name
    assert "model" not in frontmatter
    assert "mcp-servers" not in frontmatter
    assert isinstance(frontmatter["tools"], list)
    assert set(frontmatter["tools"]) <= ALIASES | {"patent-creator/*"}
    assert {"read", "execute", "patent-creator/*"} <= set(frontmatter["tools"])
    assert len(body) <= 30000


@pytest.mark.parametrize("name", NAMES)
def test_mcp_execution_and_prerequisite_safeguards(name):
    _, body = read_profile(name)
    assert "patent-creator" in body
    assert "/mcp" in body
    assert "MCP" in body
    for requirement in (
        "environment",
        "never print",
        "approval",
        "paid",
        "MPEP index",
        "checks_skipped",
        "all registered US, EPO, and PCT",
        "attorney",
    ):
        assert requirement in body, (name, requirement)
    assert "unchanged" in body
    assert f"/agent {name}" in body


@pytest.mark.parametrize("name", NAMES)
def test_no_unsupported_platform_calls_or_model_overrides(name):
    _, body = read_profile(name)
    unsupported = (
        r"mcp__",
        r"Via MCP server",
        r"Available MCP Tools",
        r"Task\s*\(",
        r"subagent_type\s*=",
        r"\.claude[/\\]",
        r"/claude-patent-creator:",
        r"model\s*[:=]\s*[\"']?(?:sonnet|opus|haiku)",
        r"from mcp_server\.(?:mpep_search|bigquery_search|claims_analyzer|"
        r"specification_analyzer|formalities_checker|diagram_generator) import",
        r"native_tools",
        r"--skip-mcp",
        r"native-input\.json",
        r"no MCP connection or server",
    )
    for pattern in unsupported:
        assert not re.search(pattern, body, re.IGNORECASE), (name, pattern)


@pytest.mark.parametrize("name", NAMES)
def test_domain_workflow_headings_are_preserved(name):
    _, body = read_profile(name)
    original = (ORIGINALS / f"{name}.md").read_text(encoding="utf-8").split("---", 2)[2]
    headings = re.findall(r"^#{2,6} .+$", original, re.MULTILINE)
    for heading in headings:
        expected = heading.replace("Available MCP Tools", "Available Patent MCP Tools")
        assert expected in body, (name, heading)


@pytest.mark.parametrize("name", NAMES)
def test_mcp_json_examples_match_registered_tool_parameters(name):
    _, body = read_profile(name)
    parameters = registered_parameters()
    examples = re.findall(r"<!-- mcp-tool: ([a-z_]+) -->\s*```json\s*(.*?)```", body, re.DOTALL)
    assert examples, f"{name} needs an executable JSON example"
    for tool, payload in examples:
        assert tool in parameters, (name, tool)
        data = json.loads(payload)
        assert isinstance(data, dict)
        assert set(data) <= parameters[tool], (name, tool, set(data) - parameters[tool])
        assert f"`{tool}`" in body
