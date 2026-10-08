---
name: review-epo-formalities
description: Check supplied application materials against the available EPO formalities analyzer and produce a source-aware checklist.
---

# EPO Formalities Review

Use this skill for a European patent application or Euro-PCT material, including the available requirements under Rules 42-49 EPC. Ask for the abstract, title, description, and whether drawings are present. Ask which sections the user wants reviewed and note any missing inputs. Do not overwrite or silently edit their documents.

## Review workflow

1. **Set scope.** Explain that the automated tool accepts `abstract`, `title`, `specification`, and `drawings_present`; it does not accept a separate request for grant, claims, priority document, fee schedule, or deadline data. Do not claim those omitted items were checked.
2. **Confirm citations.** Read MCP resource `mpep://index/stats` to check the local legal index required for EPO references. If absent, report citation review unavailable. Call `search_patent_law` with the question as `query` and EPO jurisdiction for relevant rules only when the index is available.
3. **Run the analyzer.** Call the registered `check_epo_formalities` MCP tool with supported named fields only.
4. **Assess returned fields.** Report the actual overall status, readiness value, issues, abstract/title/drawings/sections/claims-fee fields and references that the tool returns. Do not inflate a partial result into a complete filing check.
5. **Manual checklist.** Separately identify description content (Rule 42), claim form/fees (Rules 43-45), drawings (Rule 46), abstract and figure designation (Rule 47), request/form completeness, applicant/inventor/priority data, language, fees, current deadlines, drawing production, and excluded subject matter for human/official-source verification. Do not state stale fee estimates.
6. **Deliver corrections.** Group findings by the returned severity, explain what evidence is missing, and provide a prioritized correction list. Keep proposed wording distinct from the supplied application.

## Copilot MCP tools

Call tools directly through the configured `patent-creator` MCP server. Use `/mcp` to discover available tools and invoke the displayed registered name with its named arguments; do not guess runtime prefixes or use a subprocess runner. `check_epo_formalities` accepts `abstract`, `title`, `specification`, and `drawings_present`. `search_patent_law` accepts `query`, `jurisdiction`, and optional `top_k`. Keep application text private.

## Output and limitations

Report checked, not checked, and unavailable items distinctly. Fees and deadlines must be confirmed from current official EPO materials; this workflow does not calculate filing charges. Do not call an application filing-ready based on this analyzer.

**Disclaimer:** This is an automated formality aid, not legal advice or an EPO decision. Have a qualified European Patent Attorney verify compliance and current EPO procedures before filing.
