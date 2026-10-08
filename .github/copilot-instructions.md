# Patent-creator for Copilot CLI

This is the [lesquerr/Patent-creator](https://github.com/lesquerr/Patent-creator)
fork of [RobThePCGuy/Claude-Patent-Creator](https://github.com/RobThePCGuy/Claude-Patent-Creator).
Use the fork name in documentation and retain upstream attribution. Package
names, MCP identities, and Claude plugin identifiers remain unchanged for
compatibility.

Use Copilot's skills and custom agents with the **existing, unchanged MCP
server**. Do not replace it with a direct tool runner or duplicate patent
business logic in skill directories.

## Discovery and tools

Skills and supporting resources live in `.github\skills`; custom agents live in
`.github\agents\*.agent.md`. Former Claude commands are named skills: prompt
`Use the create-patent skill` or `Use the full-review skill on this application`.
Use `/skills reload` after changes, and `/agent` to select a specialist.
The root `CLAUDE.md` and original plugin directories remain for Claude
compatibility; their plugin installation instructions are not needed in Copilot.

The workspace `.mcp.json` configures the `patent-creator` stdio server using
`.venv\Scripts\python.exe` and the original `mcp_server\server.py`.
Start Copilot **from the repository root** so these relative paths resolve.
Open `/mcp` to inspect connection status and exposed tool schemas. If the
current session predates configuration, restart Copilot to load it.

Invoke patent MCP tools directly with named arguments, using the actual
runtime-exposed tool names from `patent-creator`; do not invent a tool prefix.
The server exposes all 34 existing patent tools and `mpep://index/stats`.
For example, invoke `review_patent_claims` with `claims_text`, or
`search_mpep` with `query` and `top_k`. Preserve full source text in arguments.
Inspect returned error fields, including errors inside lists, and MCP error
indicators. Failed searches are not zero matches; failed reviews are not
compliance passes. Preserve warnings, `checks_skipped`, partial results,
jurisdiction and verified citations.

Custom agent profiles include `patent-creator/*` in their tool permissions so
their built-in-tool lists do not accidentally exclude the MCP server.
If the server/tool is unavailable, report the blocker instead of silently
substituting unexecuted checks.

## Windows setup

Run manual Python commands from the repository root with
`.venv\Scripts\python.exe`; shell activation does not persist between tool calls.
Check the existing environment before installing dependencies. If missing:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

The unchanged server cannot start without MPEP PDFs or an existing index.
Current downloads and generated index files are not bundled in git. After
obtaining approval for downloads and index/model building, use the existing
CLI commands (these do not perform Claude registration):

```powershell
.venv\Scripts\python.exe -m mcp_server.cli download-all
.venv\Scripts\python.exe -m mcp_server.cli rebuild-index
.venv\Scripts\python.exe -m mcp_server.cli health
```

Alternatively the unchanged `setup --non-interactive` command retains GPU
provisioning and its original Claude auto-registration attempt. That attempt
does not configure Copilot; Copilot reads `.mcp.json` independently. Do not
claim setup has a Copilot-specific flag. For EPO/PCT law retrieval, confirm
those sources were downloaded and indexed too.

Credentials are inherited environment variables: `GOOGLE_CLOUD_PROJECT`,
`GOOGLE_APPLICATION_CREDENTIALS` (local file path), `SERPAPI_API_KEY`,
`EPO_OPS_KEY`, `EPO_OPS_SECRET`, and `USPTO_API_KEY` as applicable.
The existing ignored root `.env` file is supported; real environment
variables take precedence. Do not print keys, read credential-file contents
into chat, commit secrets or ask users to paste them into prompts.
Restart Copilot after changing its inherited environment. Obtain approval
before billable queries or disclosing private invention details to providers.
Keep BigQuery budget safeguards.

To work from another project, add this checkout as a trusted directory for
skills/agents, and register the MCP server in user scope with **absolute**
interpreter and script paths via `copilot mcp add`. Do not assume workspace
relative paths work from an unrelated working directory.

## Honest limitations

Law search and citation-enriched US/EPO/PCT reviews require a built law index.
Provider searches require their credentials; drawing rendering requires
system Graphviz, not just the Python package. Registration/schema checks are
not evidence that live searches, reviews or rendering succeeded.
Automated mechanical checks do not prove novelty, inventive step,
non-obviousness, legal sufficiency or filing readiness. Do not fabricate
authority or omit skipped checks. Draft packages need practitioner review
and appropriate filing-format conversion. Do not file applications without
explicit authorization.

## Development

Keep the MCP server and existing Python setup unchanged for this migration.
Preserve original Claude resources. Use existing pytest, Black and Ruff
configuration for new discovery/configuration tests.
