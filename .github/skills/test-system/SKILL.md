---
name: test-system
description: Run local Patent Creator checks by category and clearly gate tests that download data or may incur search charges.
---

# Test Patent Creator

Use this workflow to verify the component the user is concerned about. Ask whether they want analyzer, GPU, BigQuery, embeddings, or complete installation checks. First confirm the repository root and use the existing `.venv`; do not install or upgrade dependencies as a test side effect.

## Test choices

Run one selected local script from the repository root:

```powershell
.\.venv\Scripts\python.exe scripts\test_analyzers.py
.\.venv\Scripts\python.exe scripts\test_gpu.py
.\.venv\Scripts\python.exe scripts\test_embedding_speed.py
.\.venv\Scripts\python.exe scripts\test_bigquery.py
.\.venv\Scripts\python.exe scripts\test_install.py
```

- **Analyzers:** exercises local claims, specification, and formalities analyzers; report actual results without treating sample output as a legal review.
- **GPU:** checks hardware/torch availability; it does not prove that an index build will fit in memory.
- **Embeddings:** loads the BGE model and benchmarks local encoding. If model weights are not cached, it may download a large model; inspect cache/readiness and obtain explicit approval before downloading.
- **BigQuery:** the existing test script performs keyword, patent-detail, and CPC queries. It may incur charges beyond free quota; do not run without explicit approval of the query and possible cost.
- **Complete installation:** imports dependencies and loads an embedding model; it may download model weights if absent. Obtain approval before any large download. This script does not set up assistant registration.

For a BigQuery readiness-only check, call the zero-argument `check_bigquery_status` MCP tool; do not mistake it for a search test. Read resource `mpep://index/stats` to inspect law-index availability and call `check_diagram_tools_status` to inspect diagram readiness.

## Execution and reporting

For each selected check, state what it will do before running it. Capture exit status and relevant output; redact any credential values. Do not automatically retry a failed test that could repeat a paid query, download, or model installation. Report exactly which test ran, pass/fail status, failures, skipped checks, and limitations. A successful local test does not establish patent-law accuracy, cloud billing status, or GPU performance for another workload.

## Copilot MCP tools

Call tools directly through the configured `patent-creator` MCP server. Use `/mcp` to discover available tools and invoke the displayed registered name with its named arguments; do not guess runtime prefixes or use a subprocess runner.

**Disclaimer:** Tests verify software behavior only. They do not validate a patent application, provide legal advice, or guarantee search completeness.
