---
name: testing-assistant
description: "Guides unit, integration, MCP-tool, performance, and regression testing for the Patent Creator."
---

## Using the connected MCP server

In Copilot, connect to the configured `patent-creator` server with `/mcp` and restart Copilot after configuration changes. Discover the exposed tools and parameter schemas from that server. Invoke tools as attached MCP calls with named arguments matching the discovered schema. Server-qualified aliases vary by runtime, so invoke tools through Copilot's discovered MCP interface rather than hard-coding an alias or treating internal Python classes as exposed tools.
# Testing Assistant Skill

Use the project's tests and the attached MCP tools to validate changes. Run focused tests first; expand to broader suites only when needed. Do not install or update dependencies unless a required package is missing.

## When to Use

Unit/integration tests, MCP connection verification, regression testing, performance checks, failure diagnosis, and test authoring.

## Test Suite

Tests are under `tests/`; additional system validation scripts are under `scripts/`.

```powershell
& .\.venv\Scripts\python.exe -m pytest tests -q
```

For a focused change, select the smallest relevant test file:

```powershell
& .\.venv\Scripts\python.exe -m pytest tests\test_server_boot.py -q
```

Relevant existing scripts include `scripts/test_gpu.py`,
`scripts/test_bigquery.py`, `scripts/test_analyzers.py`, and
`scripts/test_install.py`. Some require GPU, credentials, a built index, or
network access; inspect prerequisites and run only those appropriate to the
task.

## Verifying MCP Tools

1. Connect the configured `patent-creator` server with `/mcp` and restart
   Copilot if the server configuration changed.
2. Discover the attached tools and parameter schemas through Copilot's MCP
   interface; runtime-qualified aliases may vary.
3. Invoke the exposed tool through that interface with named arguments
   matching its schema.
4. Verify the returned structure and explicitly inspect any `error` or
   prerequisite message.
5. Read `mpep://index/stats` before searches or reviews that require the law
   index. A missing-index error is not an empty result.

Optional integrations should be tested only when configured: BigQuery ADC
and project, Google Patents API key, EPO OPS credentials, or Graphviz. Never
print or include credential values in test output.

## Validation Checklist

- [ ] Legal search returns cited passages when a law index is built.
- [ ] Missing index produces an explicit prerequisite error.
- [ ] BigQuery/Google Patents return useful results only when configured.
- [ ] Claims, specification, and formalities tools return their documented
      analysis shape.
- [ ] EPO checks retain the Art. 123(2) added-matter limitation disclosure.
- [ ] Diagram tools produce files only when Graphviz is ready.
- [ ] Attached MCP tools execute and return the documented result shapes.
- [ ] Invalid inputs and unavailable optional services report errors clearly.

## Creating Tests

Prefer isolated tests for one behavior, deterministic fixtures, and real
production entry points. Add coverage for normal input, boundaries, missing
prerequisites, validation errors, and failures. Avoid tests that only assert
mock calls or depend on credentials/network when a focused unit test can
cover the behavior.

## Performance Checks

Measure after warm-up, separate model load time from steady-state work, and
record hardware, corpus size, and external-service latency. Historical targets
are indicative only, not guaranteed service levels:

| Operation | Indicative target | Notes |
|---|---|---|
| MPEP search, warm | <500 ms | Depends on model/corpus and hardware |
| Claims analysis | <3 s | Depends on claim length |
| Specification analysis | <10 s | Depends on document length |
| Diagram generation | <1 s | SVG, Graphviz already installed |
| Cloud patent search | Network-dependent | External API or BigQuery latency |

## Troubleshooting Test Failures

| Problem | Response |
|---|---|
| Import error | Use `.venv\Scripts\python.exe`; install only the missing dependency |
| GPU test fails | Inspect PyTorch/CUDA availability; skip GPU-specific tests if not configured |
| BigQuery fails | Check ADC and `GOOGLE_CLOUD_PROJECT` without exposing credentials |
| Index missing | Use the `setup-assistant` guidance if index setup is requested |
| MCP tool missing | Confirm `patent-creator` is connected with `/mcp`, restart Copilot, then rediscover tools and schemas |

## Best Practices

Run targeted tests after each change, keep tests independent, use the same
virtual environment used by the project, and distinguish skipped checks from
passing checks in reports.
