"""Workspace configuration connects Copilot to the original stdio server."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_workspace_patent_mcp_configuration():
    servers = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))["mcpServers"]
    server = servers["patent-creator"]
    assert server["type"] == "local"
    assert server["command"] == r".venv\Scripts\python.exe"
    assert server["args"] == [r"mcp_server\server.py"]
    assert server["tools"] == ["*"]
    assert "env" not in server
    assert (ROOT / server["args"][0]).is_file()


def test_copilot_documentation_uses_mcp_not_withdrawn_runner():
    for path in (ROOT / "README.md", ROOT / ".github" / "copilot-instructions.md"):
        text = path.read_text(encoding="utf-8")
        assert "native_tools" not in text
        assert "--skip-mcp" not in text
        assert "patent-creator" in text
        assert "/mcp" in text
