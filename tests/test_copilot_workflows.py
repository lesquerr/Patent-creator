"""Contract tests for the native Copilot skill migrations of command workflows."""

from __future__ import annotations

import ast
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / ".github" / "skills"
COMMAND_STEMS = {
    "check-pct-formalities",
    "configure-bigquery",
    "create-epo-patent",
    "create-patent",
    "full-review",
    "rebuild-index",
    "review-claims",
    "review-epo-claims",
    "review-epo-formalities",
    "review-formalities",
    "review-specification",
    "search-epo",
    "search-prior-art",
    "setup-patent-creator",
    "setup-patent-system",
    "test-system",
}

TOOL_WORKFLOWS = {
    "check-pct-formalities": {"check_pct_formalities", "search_patent_law"},
    "configure-bigquery": {"check_bigquery_status"},
    "create-epo-patent": {
        "search_epo_patents",
        "review_epo_claims",
        "review_epo_specification",
        "check_epo_formalities",
        "search_patent_law",
        "create_flowchart",
        "create_block_diagram",
        "render_diagram",
    },
    "create-patent": {
        "search_patents_google",
        "search_patents_bigquery",
        "search_patents_by_cpc_bigquery",
        "review_patent_claims",
        "review_specification",
        "check_formalities",
        "search_mpep",
        "create_flowchart",
        "create_block_diagram",
        "render_diagram",
    },
    "full-review": {"review_patent_claims", "review_specification", "check_formalities"},
    "review-claims": {"review_patent_claims", "search_mpep"},
    "review-epo-claims": {"review_epo_claims", "search_patent_law"},
    "review-epo-formalities": {"check_epo_formalities", "search_patent_law"},
    "review-formalities": {"check_formalities", "search_mpep"},
    "review-specification": {"review_specification", "search_mpep"},
    "search-epo": {"search_epo_patents", "search_patents_google"},
    "search-prior-art": {"search_patents_google", "search_patents_by_cpc_bigquery"},
    "setup-patent-creator": {
        "check_bigquery_status",
        "check_diagram_tools_status",
    },
    "setup-patent-system": {
        "check_bigquery_status",
        "check_diagram_tools_status",
    },
    "test-system": {
        "check_bigquery_status",
        "check_diagram_tools_status",
    },
}

MCP_RESOURCES = {
    "check-pct-formalities",
    "create-epo-patent",
    "create-patent",
    "full-review",
    "rebuild-index",
    "review-claims",
    "review-epo-claims",
    "review-epo-formalities",
    "review-formalities",
    "review-specification",
    "setup-patent-creator",
    "setup-patent-system",
    "test-system",
}

REQUIRED_TOOL_ARGUMENTS = {
    "review_patent_claims": {"claims_text"},
    "review_specification": {"claims_text", "specification"},
    "review_epo_claims": {"claims_text"},
    "review_epo_specification": {"claims_text", "specification"},
    "search_mpep": {"query"},
    "search_patent_law": {"query"},
    "search_epo_patents": {"query"},
    "search_patents_google": {"query"},
    "search_patents_bigquery": {"query"},
    "search_patents_by_cpc_bigquery": {"cpc_code"},
    "create_flowchart": {"steps"},
    "create_block_diagram": {"blocks", "connections"},
    "render_diagram": {"dot_code"},
}

WORKFLOW_MARKERS = {
    "check-pct-formalities": ("Rule 5", "Rule 11", "Rule 13"),
    "configure-bigquery": ("credentials", "GOOGLE_CLOUD_PROJECT"),
    "create-epo-patent": ("Step 1", "Art. 84", "Rule 43"),
    "create-patent": ("Step 1", "35 USC 112", "filing-ready"),
    "full-review": ("claims", "specification", "formalities"),
    "rebuild-index": ("rebuild", "index"),
    "review-claims": ("antecedent", "35 USC 112(b)"),
    "review-epo-claims": ("Art. 84", "Rule 43"),
    "review-epo-formalities": ("Rules 42-49", "Rule 47"),
    "review-formalities": ("MPEP 608", "abstract"),
    "review-specification": ("written description", "enablement"),
    "search-epo": ("EPO OPS", "BigQuery"),
    "search-prior-art": ("7-step", "novelty"),
    "setup-patent-creator": ("setup", "index"),
    "setup-patent-system": ("setup", "index"),
    "test-system": ("analyzers", "GPU", "BigQuery"),
}

OUTPUT_MARKERS = {
    "create-epo-patent": ("06-filing-package", "filing-checklist"),
    "review-claims": ("analysis-report.md", "suggested-fixes.md"),
    "review-epo-claims": ("analysis-report.md", "suggested-fixes.md"),
    "search-epo": ("publication_number", "applicants", "filing_date"),
    "search-prior-art": (
        "search-report.md",
        "top-10-patents.md",
        "ids-list.md",
        "claim-strategy.md",
    ),
}

LEGAL_WORKFLOWS = {
    "check-pct-formalities",
    "create-epo-patent",
    "create-patent",
    "full-review",
    "review-claims",
    "review-epo-claims",
    "review-epo-formalities",
    "review-formalities",
    "review-specification",
    "search-epo",
    "search-prior-art",
}


def read_skill(stem: str) -> tuple[dict[str, object], str]:
    path = SKILLS_ROOT / stem / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    assert match, f"{path.relative_to(ROOT)} must start with YAML frontmatter"
    metadata = yaml.safe_load(match.group(1))
    assert isinstance(metadata, dict), f"{path.relative_to(ROOT)} frontmatter must be a mapping"
    return metadata, text


def registered_mcp_tools() -> dict[str, set[str]]:
    tools: dict[str, set[str]] = {}
    for path in (ROOT / "mcp_server" / "tools").glob("*.py"):
        module = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(module):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if not any(
                isinstance(decorator, ast.Call)
                and isinstance(decorator.func, ast.Attribute)
                and isinstance(decorator.func.value, ast.Name)
                and decorator.func.value.id == "mcp"
                and decorator.func.attr == "tool"
                for decorator in node.decorator_list
            ):
                continue
            positional = node.args.posonlyargs + node.args.args
            required_count = len(positional) - len(node.args.defaults)
            tools[node.name] = {argument.arg for argument in positional[:required_count]}
    return tools


def registered_mcp_resources() -> set[str]:
    resources: set[str] = set()
    for path in (ROOT / "mcp_server" / "tools").glob("*.py"):
        module = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(module):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for decorator in node.decorator_list:
                if (
                    isinstance(decorator, ast.Call)
                    and isinstance(decorator.func, ast.Attribute)
                    and isinstance(decorator.func.value, ast.Name)
                    and decorator.func.value.id == "mcp"
                    and decorator.func.attr == "resource"
                    and decorator.args
                    and isinstance(decorator.args[0], ast.Constant)
                    and isinstance(decorator.args[0].value, str)
                ):
                    resources.add(decorator.args[0].value)
    return resources


def test_all_command_stems_have_native_skills_without_name_collisions() -> None:
    command_stems = {path.stem for path in (ROOT / "commands").glob("*.md")}
    assert command_stems == COMMAND_STEMS

    source_skill_stems = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
    assert COMMAND_STEMS.isdisjoint(source_skill_stems)

    for stem in COMMAND_STEMS:
        assert (
            SKILLS_ROOT / stem / "SKILL.md"
        ).is_file(), f"Missing native Copilot skill for commands/{stem}.md"


def test_native_skill_frontmatter_is_valid_and_uses_directory_name() -> None:
    for stem in COMMAND_STEMS:
        metadata, text = read_skill(stem)
        assert metadata.get("name") == stem
        assert isinstance(metadata.get("description"), str)
        assert metadata["description"].strip()
        assert len(text) >= 800, f"{stem} does not preserve a substantial workflow"


def test_migrated_skills_preserve_the_command_workflow() -> None:
    for stem, markers in WORKFLOW_MARKERS.items():
        _, text = read_skill(stem)
        for marker in markers:
            assert (
                marker.casefold() in text.casefold()
            ), f"{stem} is missing source workflow detail: {marker}"


def test_migrated_skills_preserve_output_artifact_examples() -> None:
    for stem, markers in OUTPUT_MARKERS.items():
        _, text = read_skill(stem)
        for marker in markers:
            assert (
                marker.casefold() in text.casefold()
            ), f"{stem} is missing output example: {marker}"


def test_tool_workflows_call_registered_mcp_tools_directly() -> None:
    for stem, tools in TOOL_WORKFLOWS.items():
        _, text = read_skill(stem)
        assert "patent-creator" in text, f"{stem} must identify the configured MCP server"
        assert "/mcp" in text, f"{stem} must explain how to discover attached tools"
        assert re.search(
            r"\b(call|invoke|use)\b.{0,100}\btool", text, re.I | re.S
        ), f"{stem} must direct the agent to invoke MCP tools, not shell out"
        for tool_name in tools:
            assert tool_name in text, f"{stem} must call registered tool {tool_name}"


def test_workflow_calls_match_registered_mcp_tools_and_required_arguments() -> None:
    registered = registered_mcp_tools()
    for stem, names in TOOL_WORKFLOWS.items():
        _, text = read_skill(stem)
        for name in names:
            assert name in registered, f"{name} is not a registered MCP tool"
            assert REQUIRED_TOOL_ARGUMENTS.get(name, set()) <= registered[name]
            for argument in REQUIRED_TOOL_ARGUMENTS.get(name, set()):
                assert argument in text, f"{stem} omits required {name} argument {argument}"


def test_index_dependent_workflows_read_the_registered_mcp_resource() -> None:
    assert "mpep://index/stats" in registered_mcp_resources()
    for stem in MCP_RESOURCES:
        _, text = read_skill(stem)
        assert "patent-creator" in text
        assert "/mcp" in text
        assert "mpep://index/stats" in text
        assert re.search(r"(read|check|inspect).{0,80}resource", text, re.I | re.S)


def test_skills_do_not_use_a_subprocess_tool_runner_or_unsupported_skip_flag() -> None:
    forbidden = (
        "mcp_server.native_tools",
        "--skip-mcp",
        "--describe",
        "--input",
    )
    for stem in COMMAND_STEMS:
        _, text = read_skill(stem)
        for legacy in forbidden:
            assert (
                legacy.casefold() not in text.casefold()
            ), f"{stem} must use attached MCP calls, not {legacy}"


def test_setup_uses_only_supported_local_download_and_index_commands() -> None:
    _, setup = read_skill("setup-patent-system")
    _, creator_setup = read_skill("setup-patent-creator")
    for text in (setup, creator_setup):
        assert ".venv\\Scripts\\python.exe -m mcp_server.cli download-all" in text
        assert ".venv\\Scripts\\python.exe -m mcp_server.cli rebuild-index" in text
        assert ".venv\\Scripts\\python.exe -m mcp_server.cli health" in text
        assert "mcp_server\\server.py --rebuild-index" not in text
        assert "server.py --download-mpep" not in text
        assert re.search(r"download-all.{0,160}rebuild-index.{0,160}health", text, re.I | re.S)
        assert re.search(r"restart.{0,80}Copilot.{0,80}/mcp", text, re.I | re.S)
    assert re.search(r"approval.{0,100}(download|500\s*MB|500\s*mb)", setup, re.I | re.S)


def test_index_rebuild_uses_cli_not_mcp_server_startup_flags() -> None:
    _, skill = read_skill("rebuild-index")
    assert ".venv\\Scripts\\python.exe -m mcp_server.cli rebuild-index" in skill
    assert ".venv\\Scripts\\python.exe -m mcp_server.cli health" in skill
    assert "mcp_server\\server.py --rebuild-index" not in skill
    assert re.search(r"restart.{0,80}Copilot.{0,80}/mcp", skill, re.I | re.S)


def test_workspace_mcp_config_connects_the_existing_server() -> None:
    config = yaml.safe_load((ROOT / ".mcp.json").read_text(encoding="utf-8"))
    server = config["mcpServers"]["patent-creator"]
    assert server["type"] == "local"
    assert server["command"] == ".venv\\Scripts\\python.exe"
    assert server["args"] == ["mcp_server\\server.py"]
    assert server["tools"] == ["*"]


def test_paid_patent_search_requires_explicit_approval() -> None:
    for stem in ("search-epo", "search-prior-art"):
        _, text = read_skill(stem)
        assert re.search(r"explicit approval.{0,120}(paid|cost|BigQuery)", text, re.I | re.S)


def test_legal_workflows_retain_legal_disclaimers() -> None:
    for stem in LEGAL_WORKFLOWS:
        _, text = read_skill(stem)
        assert re.search(r"not legal advice|does not replace.{0,40}legal advice", text, re.I)


def test_credentials_are_not_exposed_in_bigquery_guidance() -> None:
    _, text = read_skill("configure-bigquery")
    assert re.search(
        r"(never|do not|don't).{0,40}(print|display|share|echo).{0,50}(secret|credential|token)",
        text,
        re.I | re.S,
    )
    assert "GOOGLE_CLOUD_PROJECT" in text


def test_native_skills_do_not_rely_on_claude_plugin_runtime() -> None:
    forbidden = (
        "CLAUDE_PLUGIN_ROOT",
        ".copilot\\commands",
        "claude mcp",
        "claude-sonnet",
        "Claude Code",
        "python install.py",
        "$ARGUMENTS",
        "allowed-tools:",
    )
    for stem in COMMAND_STEMS:
        metadata, text = read_skill(stem)
        assert "allowed-tools" not in metadata
        assert "model" not in metadata
        for legacy in forbidden:
            assert (
                legacy.casefold() not in text.casefold()
            ), f"{stem} contains Claude-only guidance: {legacy}"
