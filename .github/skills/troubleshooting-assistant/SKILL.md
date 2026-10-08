---
name: troubleshooting-assistant
description: "Diagnoses Copilot MCP connection, dependency, GPU, BigQuery/EPO authentication, index, import, search-quality, and performance failures."
---

## Using the connected MCP server

In Copilot, connect to the configured `patent-creator` server with `/mcp` and restart Copilot after configuration changes. Discover the exposed tools and parameter schemas from that server. Invoke tools as attached MCP calls with named arguments matching the discovered schema. Server-qualified aliases vary by runtime, so invoke tools through Copilot's discovered MCP interface rather than hard-coding an alias or treating internal Python classes as exposed tools.
# Troubleshooting Assistant Skill

Use a six-step diagnosis: gather the exact error and recent change; reproduce
the smallest case; isolate the component; identify root cause; apply a
targeted fix; and verify that the same failure no longer occurs. Do not
silently convert configuration errors into empty results.

## When to Use

MCP connection or tool errors, missing dependencies or index files, authentication
failures, GPU issues, slow or irrelevant search results, analyzer failures,
and diagram generation problems.

## First Checks

Run from the repository root:

```powershell
& .\.venv\Scripts\python.exe --version
& .\.venv\Scripts\python.exe -m mcp_server.cli health
```

Record the tool name, non-secret error message, and whether the requested
optional service is configured. Do not show `.env` contents, key values, or
credential files. Connect with `/mcp` and use Copilot's discovery to inspect
the current tool schema before changing an invocation.

## Common Issues

| Symptom | Diagnosis and response |
|---|---|
| MCP tool missing | Connect or reconnect `patent-creator` with `/mcp`, restart Copilot, and inspect its discovered tools |
| Invalid input | Inspect the attached tool schema and pass the exact named arguments and types |
| Law search/review says index missing | No search/review ran; read `mpep://index/stats` and use the `setup-assistant` workflow only if setup is requested |
| BigQuery authentication fails | Check ADC status and `GOOGLE_CLOUD_PROJECT`; never print credential data |
| Google Patents unavailable | Check `check_google_patents_status`; use BigQuery only if configured and cost is acceptable |
| EPO OPS unavailable | Check `check_epo_api_status` and the presence (not values) of `EPO_OPS_KEY` and `EPO_OPS_SECRET` |
| CUDA unavailable | Check whether the installed PyTorch build and GPU driver support CUDA; CPU fallback may be slower |
| Graphviz missing | Run `dot -V` and `check_diagram_tools_status`; install the missing Windows component only when requested |
| Results appear irrelevant | Refine terminology, jurisdiction, source filters, and date range; record the actual filters used |
| Out of memory during indexing | Reduce supported batch size or use CPU; preserve source PDFs and report failed builds |

## Component Tests

Use the project's tests and health command instead of constructing internal
classes as if they were tools:

```powershell
& .\.venv\Scripts\python.exe -m pytest tests -q
& .\.venv\Scripts\python.exe scripts\test_analyzers.py
```

Run `scripts\test_gpu.py` or `scripts\test_bigquery.py` only if those
integrations are relevant and configured. Cloud searches require network
access; do not run them just to diagnose unrelated local failures.

## Logging

To enable verbose logs for the current PowerShell process:

```powershell
$env:PATENT_LOG_LEVEL = "DEBUG"
```

Keep logs local and redact user documents, API keys, access tokens, and
authorization output before sharing diagnostics.

## Prevention

Test after dependency or configuration changes, preserve an existing `.env`
and venv, back up the index before rebuilding, and note skipped tests and
unavailable optional services in the final report. Use the `index-manager`
skill for index lifecycle work and the `testing-assistant` skill for test
selection.
