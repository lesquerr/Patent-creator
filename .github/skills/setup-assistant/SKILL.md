---
name: setup-assistant
description: "Guides Windows setup, authentication, and Copilot connection to the existing Patent Creator MCP server."
---

## Using the connected MCP server

In Copilot, connect to the configured `patent-creator` server with `/mcp` and restart Copilot after configuration changes. Discover the exposed tools and parameter schemas from that server. Invoke tools as attached MCP calls with named arguments matching the discovered schema. Server-qualified aliases vary by runtime, so invoke tools through Copilot's discovered MCP interface rather than hard-coding an alias or treating internal Python classes as exposed tools.
# Setup Assistant Skill

Guide Windows setup of the Patent Creator Python package, its local legal index, optional cloud credentials, and Copilot connection to its existing MCP server. Keep existing environment credentials and dependencies; never print secret values or replace a populated `.env` file.

## When to Use

First setup, configuring an existing checkout or virtual environment, optional search authentication, dependency trouble, health checks, and moving the project to another machine.

## Setup on Windows

Use Python 3.10 or newer. Run commands from the repository root in PowerShell:

```powershell
python --version
if (-not (Test-Path .\.venv\Scripts\python.exe)) {
    python -m venv .venv
}
```

Use the venv's Python executable directly; activation is optional:

```powershell
& .\.venv\Scripts\python.exe -m pip --version
```

If a required package is missing, install only that package into this venv. Do not reinstall or upgrade the project's full dependency set unless a reported dependency problem requires it. Preserve installed Python dependencies and any existing GPU-enabled PyTorch.

To download the legal corpus and build the index without starting Claude MCP registration, run these existing CLI commands from the repository root:

```powershell
& .\.venv\Scripts\python.exe -m mcp_server.cli download-all
& .\.venv\Scripts\python.exe -m mcp_server.cli rebuild-index
& .\.venv\Scripts\python.exe -m mcp_server.cli health
```

`download-all` downloads MPEP, 35 USC, 37 CFR, subsequent updates, and EPO/PCT sources; do not also run `download-mpep`, which would duplicate the MPEP download. Downloads and index building can take a long time and require substantial disk space. Do not start another setup while one is already running.

The alternative `setup --non-interactive` command also attempts optional Claude MCP registration; this is unrelated to Copilot. Avoid rebuilding through the server entry point: it proceeds into its MCP loop after rebuilding.

Run downloads or index builds only when setup was requested. The MCP server only starts when its source PDFs or built index are present. After the corpus and index are ready, restart Copilot and connect with `/mcp`.

## Environment and Credentials

Keep existing `.env` values and environment credentials. If configuration is needed, update only the required keys and never display secret values in output.

- The local MPEP/USC/CFR tools require a successfully built law index.
- BigQuery patent search is optional and uses `GOOGLE_CLOUD_PROJECT` plus Google Application Default Credentials.
- Google Patents search is optional and uses `SERPAPI_API_KEY`.
- EPO OPS search is optional and uses `EPO_OPS_KEY` and `EPO_OPS_SECRET`.
- Do not ask for, echo, or store credentials in skill files, logs, command transcripts, or generated reports.

For Google Cloud authentication, use the official `gcloud auth application-default login` flow only when the user requests BigQuery setup. In PowerShell, set a project for the current process with `$env:GOOGLE_CLOUD_PROJECT = "project-id"`; persist it only if the user asks.

## Verify Setup

Run the project health check. After the workspace MCP server is configured, connect with `/mcp`, restart Copilot, and use tool discovery to confirm `patent-creator` is attached:

```powershell
& .\.venv\Scripts\python.exe -m mcp_server.cli health
```

Read the `mpep://index/stats` MCP resource to check index status. If the law index is unavailable, citation-enriched legal searches and reviews cannot run; report the prerequisite instead of treating the result as clean or empty.

For optional service status, call the discovered `check_bigquery_status`, `check_google_patents_status`, `check_epo_api_status`, or `check_diagram_tools_status` MCP tools with their exposed arguments. Report which optional service is unavailable without revealing keys or credentials.

## Resources and Scope

Resolve `filing-reference.md` relative to this loaded skill's base path. It is filing guidance, not a substitute for current official USPTO requirements or attorney review. The workspace `.mcp.json` connects Copilot to the existing server; setup does not replace or modify the Python server. Preserve the original Claude integration and keep its setup side effect separate from Copilot connectivity.

## Common Setup Problems

| Symptom | Response |
|---|---|
| Python below 3.10 | Install a supported Python version, then recreate only a missing venv |
| Required module missing | Install only that missing dependency into `.venv` |
| Law index unavailable | If setup is requested and not already running, use the `download-all`, `rebuild-index`, and `health` sequence above; report any failure explicitly |
| BigQuery unavailable | Verify project configuration and ADC status; do not request credentials in chat |
| Google Patents unavailable | Check whether `SERPAPI_API_KEY` is configured without printing its value |
| EPO OPS unavailable | Check `EPO_OPS_KEY` and `EPO_OPS_SECRET` presence without exposing values |
| Diagram tools unavailable | Check `dot -V` and the Python `graphviz` package |

## Maintenance

```powershell
& .\.venv\Scripts\python.exe -m mcp_server.cli health
& .\.venv\Scripts\python.exe -m mcp_server.cli rebuild-index
```

Use the `index-manager` skill for PDF/index lifecycle steps and the `testing-assistant` skill for focused validation.
