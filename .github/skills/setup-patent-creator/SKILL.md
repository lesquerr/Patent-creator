---
name: setup-patent-creator
description: Set up local Patent Creator sources and law index, then verify the Copilot MCP server connection.
---

# Set Up Patent Creator

Use this skill for a first-time local setup. Confirm the repository root and whether a `.venv` with project dependencies already exists. Do not change dependency manifests or install alternate packages. If dependencies or the virtual environment are absent, explain that environment installation can download substantial packages and ask before installing them.

## Setup workflow

1. **Confirm prerequisites.** Check that an installed Python version is compatible with project dependencies, sufficient disk space is available, and the user intends to build a local law index. Do not claim a particular Python upper bound beyond the current project/dependency support.
2. **Confirm downloads.** Setup may download roughly 500 MB of MPEP PDFs plus other law sources and may download model weights when building the index. Obtain explicit approval before starting large downloads. Do not run paid patent queries during setup.
3. **Confirm environment.** Use the existing repository `.venv`; if it does not exist, stop until the user approves creation and dependency installation. Keep credentials in the user's environment or normal ADC store, never in source files.
4. **Run the existing corpus download and index commands only after approval**, from the repository root, using the existing environment and one command at a time:

   ```powershell
   .\.venv\Scripts\python.exe -m mcp_server.cli download-all
   .\.venv\Scripts\python.exe -m mcp_server.cli rebuild-index
   .\.venv\Scripts\python.exe -m mcp_server.cli health
   ```

   `download-all` downloads MPEP PDFs, statutes, regulations, updates, and EPO/PCT sources; it already includes MPEP, so do not run a second MPEP download. `rebuild-index` builds the index and exits; `health` checks local setup. These CLI commands do not start an MCP server. After they finish, restart or reconnect Copilot's `patent-creator` server through `/mcp` so its process starts with the completed corpus and index.
5. **Monitor and report actual phases:** hardware/PyTorch handling; missing source downloads; EPO/PCT legal source availability; FAISS/BM25 index build; optional BigQuery status; and diagram tool status. Durations vary by connection, hardware, and cache; do not promise estimates as guarantees.
6. **Verify without a paid search.** After reconnecting the server, read resource `mpep://index/stats` through `patent-creator` to confirm index availability; call `check_bigquery_status` only if BigQuery readiness is relevant and `check_diagram_tools_status` only if diagrams are being configured. These checks do not run patent queries.
7. **Handle optional authentication separately.** For BigQuery or EPO OPS credentials, use their configuration workflows and keep values private. Never print credentials or tokens in command output.

## Boundaries

Setup does not require paid patent queries. Do not run BigQuery/SerpApi searches or download large corpora without explicit user approval. A working local law index is needed for US legal citations in claims and US reviews. Diagram generation and analyzers that do not retrieve legal citations can run without that index.

If setup is interrupted or fails, report the exact stage and error. Do not rerun downloads blindly; inspect installed source files and ask before repeating large transfers.

## Copilot MCP tools

The workspace `.mcp.json` configures the local `patent-creator` server using `.venv\Scripts\python.exe` and `mcp_server\server.py`. After corpus setup, restart or reconnect it through `/mcp`, then discover and call tools by their displayed registered names and named arguments. Do not guess runtime prefixes or use a subprocess runner.

**Disclaimer:** Setup prepares local software and reference materials only. It does not provide legal advice or ensure the law corpus is current for every filing.
