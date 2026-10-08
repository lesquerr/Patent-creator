---
name: development-assistant
description: "Guides through adding new features, MCP tools, analyzers, and extending the patent creator system."
---

## Using the connected MCP server

In Copilot, connect to the configured `patent-creator` server with `/mcp` and restart Copilot after configuration changes. Discover the exposed tools and parameter schemas from that server. Invoke tools as attached MCP calls with named arguments matching the discovered schema. Server-qualified aliases vary by runtime, so invoke tools through Copilot's discovered MCP interface rather than hard-coding an alias or treating internal Python classes as exposed tools.
# Development Assistant Skill

Guidance for developing and extending the patent creator's Python package, registered MCP tools, analyzers, configuration, and tests while following existing patterns.

## When to Use This Skill

Activate when adding MCP tools, analyzers, configuration options, BigQuery queries, skills, or performance optimizations.

## Development Workflow

```
Feature Request -> Planning -> Implementation (Code + Validation + Monitoring + Tests) -> Testing -> Documentation -> Integration
```

## Adding New MCP Tools

**Quick Start:**
1. Define inputs, outputs, dependencies
2. Create or reuse a Pydantic model in `mcp_server/validation.py`
3. Add the tool in the appropriate `mcp_server/tools/` registration module,
   preserving its registered name and argument schema
4. Ensure the server registers it during initialization; verify it using
   Copilot's MCP discovery after connecting `patent-creator` with `/mcp`
5. Add focused tests under `tests/`

**Key Decorators:**
Follow the surrounding `register_*_tools(...)` closure pattern in
`mcp_server/tools/`; MCP tools expose those registered functions through the
attached server.
Keep input validation, structured logging, and performance tracking
consistent with nearby registrations. Do not expose a Python class as if it
were a tool.

**Registration template:**
```python
def register_your_tools(mcp, validate_input, YourInput, track_performance):
    @mcp.tool()
    @track_performance("tool_your_tool")
    def your_tool(param: str, optional: int = 10) -> dict:
        """Describe behavior and each parameter for MCP tool discovery.

        Args:
            param: Description.
            optional: Description with its default.

        Returns:
            JSON-serializable result.
        """
        validated = validate_input(YourInput, param=param, optional=optional)
        return {"result": validated.param}
```

## Adding New Analyzers

**Overview:** Analyzers inherit from `BaseAnalyzer` and check USPTO compliance.

**Minimal Example:**
```python
from mcp_server.analyzer_base import BaseAnalyzer

class YourAnalyzer(BaseAnalyzer):
    def __init__(self):
        super().__init__()
        self.mpep_sections = ["608", "2173"]

    def analyze(self, content: str) -> dict:
        issues = []
        if violation:
            issues.append({
                "type": "violation_name",
                "severity": "critical",
                "mpep_citation": "MPEP 608",
                "recommendation": "Fix description"
            })
        return {"compliant": len(issues) == 0, "issues": issues}
```

## Adding Configuration Options

Use Pydantic settings in `mcp_server/config.py`:

```python
# In config.py
class AppSettings(BaseSettings):
    enable_feature_x: bool = Field(default=False, description="Enable X")

# In your code
from mcp_server.config import get_settings
if get_settings().enable_feature_x:
    # Feature enabled
```

## Adding Performance Monitoring

```python
@track_performance
def your_function(data):
    with OperationTimer("step1"):
        result1 = step1(data)
    with OperationTimer("step2"):
        result2 = step2(result1)
    return result2
```

## Modifying RAG Search Pipeline

Pipeline: `Query -> HyDE -> Vector+BM25 -> RRF -> Reranking -> Results`

**Customization Points:** Query expansion, custom scoring, filtering, reranking strategies

## Converting a Workflow to a Skill

Copilot workflow guidance belongs in `.github/skills/<skill-name>/SKILL.md`.
Use a unique lowercase skill name and a quoted description in its frontmatter.
For existing workflows, reference the skill by its stem (for example,
"Use the `patent-reviewer` skill"). Repository instructions belong in
`.github/copilot-instructions.md`; agents belong in
`.github/agents/*.agent.md`. Do not add model/tool keys, execute
pre-approvals, or command/configuration files for this migration.

## Development Best Practices

1. Follow existing patterns
2. Use type hints
3. Write docstrings (Google style)
4. Handle errors gracefully
5. Validate inputs (Pydantic)
6. Log operations
7. Monitor performance

## Common Development Tasks

**Add BigQuery Query:** Add method in `mcp_server/bigquery_search.py`

**Add Validation Rule:**
```python
class YourInput(BaseModel):
    field: str

    @field_validator("field")
    @classmethod
    def validate_field(cls, v):
        if not meets_requirement(v):
            raise ValueError("Error message")
        return v
```

**Add Logging:**
```python
from mcp_server.logging_config import get_logger
logger = get_logger()
logger.info("event_name", extra={"context": "data"})
```

## Quick Reference: File Locations

| Task | Primary File | Related Files |
|------|-------------|---------------|
| Add MCP tool | `mcp_server/tools/` | `mcp_server/server.py`, `mcp_server/validation.py` |
| Add analyzer | `mcp_server/your_analyzer.py` | `mcp_server/analyzer_base.py` |
| Add config | `mcp_server/config.py` | `.env` |
| Add BigQuery query | `mcp_server/bigquery_search.py` | - |
| Add test | `scripts/test_your_feature.py` | - |

## Key Patterns

**MCP Tool Pattern:**
```python
@mcp.tool()
@validate_input(InputModel)
@track_performance
def tool_name(param: type) -> dict:
    """Description exposed by the registered MCP tool."""
    from module import Component
    if invalid:
        return {"error": "message"}
    result = process(param)
    return {"key": "value"}
```

**Analyzer Pattern:**
```python
class YourAnalyzer(BaseAnalyzer):
    def analyze(self, content: str) -> dict:
        issues = []
        issues.extend(self._check_x(content))
        return {
            "compliant": len(issues) == 0,
            "issues": issues,
            "recommendations": self._generate_recommendations(issues)
        }
```
