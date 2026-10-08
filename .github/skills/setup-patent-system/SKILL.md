---
name: setup-patent-system
description: Set up local patent-law sources and index, then verify optional services through the attached MCP server.
---

# Set Up the Patent System

This workflow prepares local Patent Creator sources and index, then verifies status through the attached MCP server. Explain each side effect first. Do not change project dependencies or begin large downloads until the user approves.

## 1. Preflight

- Confirm the current folder is the repository root (contains `pyproject.toml`).
- Inspect the existing `.venv`; preserve it and its dependencies. If no environment exists or packages are missing, explain what installation would download and ask before creating/installing.
- Check available Python compatibility against the package's current dependency constraints; do not rely on an obsolete hard-coded version range.
- Confirm disk space and whether the user wants the local legal search index. The MPEP PDFs alone are approximately 500 MB; other sources and embedding model weights add to this. Obtain explicit approval before any large download.
- Explain that setup may install or adjust PyTorch for detected hardware. Do not do this without the user's approval of environment changes.

## 2. Download the corpus and build the index

After the user approves source/model downloads and any environment changes, run the existing CLI commands from the repository root, one at a time:

```powershell
.\.venv\Scripts\python.exe -m mcp_server.cli download-all
.\.venv\Scripts\python.exe -m mcp_server.cli rebuild-index
.\.venv\Scripts\python.exe -m mcp_server.cli health
```

`download-all` downloads MPEP PDFs, statutes, regulations, updates, and EPO/PCT sources; do not run a separate MPEP download. It exits after downloading. `rebuild-index` builds the local index and exits without starting the MCP server. Run `health` to check local setup. Once these commands complete, restart or reconnect Copilot's `patent-creator` server through `/mcp`; its startup requires the corpus and index now in place.

## 3. Verify and configure optional services

- After restarting the server, read resource `mpep://index/stats` through the connected `patent-creator` MCP server to confirm legal source/index status. A built index is required for citation retrieval in legal reviews.
- BigQuery and EPO OPS credentials are optional. Keep them in environment variables or normal local auth stores; never echo or commit secret values.
- BigQuery authentication is not required for local review or diagram work.
- Call the zero-argument `check_bigquery_status` MCP tool to check readiness without running a patent query. Do not use `scripts\test_bigquery.py` as a no-cost health check; it runs search/detail queries.
- Call `check_diagram_tools_status` to verify Graphviz readiness. Do not install Graphviz from the internet without approval.

## 4. No index or incomplete setup

If the user declines a large download, stop before downloading. Explain that diagrams and analyzers that do not need retrieved law citations may still work, while claims/US legal citation workflows need the index. Do not substitute generic internet text as if it were indexed MPEP guidance.

If setup failed, preserve logs without credential values, report the failing step, and avoid an automatic retry that repeats downloads or alters the environment.

## Operational safeguards

Never run paid BigQuery or SerpApi searches during setup. Ask for explicit approval before large source/model downloads, dependency installation, or changes to the environment. Keep all environment credentials private. Use `/mcp` to confirm the `patent-creator` connection and discover tools; invoke registered MCP tools directly by their displayed name and named arguments, never through a Python runner.

**Disclaimer:** Installation provides tools and source retrieval only. It does not make the system an official patent authority or replace professional legal review.
