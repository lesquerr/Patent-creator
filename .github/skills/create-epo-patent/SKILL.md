---
name: create-epo-patent
description: "Guide preparation of an EPO-focused draft application from invention intake through review and package validation."
---

## Copilot MCP tools

Call tools directly through the configured `patent-creator` MCP server. Use `/mcp` to confirm the server and discover its exposed tools, then invoke the displayed registered tool with named arguments from its schema. Do not guess runtime-qualified prefixes or replace tool calls with a Python runner.
# Create an EPO Patent Application

Guide the user through a working draft, not an automatic legal filing. Ask questions as needed and keep a durable user-approved working outline. Confirm the output directory before creating or overwriting files. Use the user's chosen filing route (direct EP or Euro-PCT) and flag that the available automated EPO checks are partial.

## Phase 1 — Step 1: Invention disclosure

Collect the technical problem, solution, essential components/steps, alternatives, examples, prototypes, commercial context only if relevant, and known competing approaches. Ask which features are essential and which are optional. Record unanswered facts as questions rather than filling them in.

## Phase 2 — Prior art research

Build a search strategy from the disclosed features: synonyms, distinctive technical terms, likely IPC/CPC areas, and relevant filing periods. Prefer EPO OPS searches for EP material. Call `search_epo_patents` directly with `query` and optional `limit`, and use Google Patents or BigQuery tools only after the user gives explicit approval for any paid or credit-consuming query. BigQuery may incur charges after free quota; do not trigger it automatically. Keep a search log with query, source, date, and actual result identifiers. Do not fabricate patents or claim a comprehensive search.

## Phase 3 — Claims drafting

Draft independent and dependent claims from features supported by the disclosure. For each independent claim, identify a plausible preamble and, where appropriate, a characterising part under Rule 43(1) EPC. Keep claim categories and dependencies coherent; avoid excluded subject matter and explain uncertainty. Do not state that two-part form is invariably mandatory.

## Phase 4 — Description

Draft title, technical field, background art with verified citations, technical problem, disclosure/solution, brief description of figures, detailed embodiments, and industrial applicability where relevant. Ensure every claim feature has description support. Do not insert unsupported details or imply that the draft establishes priority or added-matter compliance.

## Phase 5 — Figures

Create a figure list and draft patent-style diagrams with consistent reference signs. Call `create_flowchart` with `steps`, `filename`, `output_format`, and `output_dir`; call `create_block_diagram` with `blocks`, `connections`, `filename`, `output_format`, and `output_dir`; or call `render_diagram` with `dot_code`, `filename`, `output_format`, `engine`, and `output_dir`. Use only fields exposed by the selected tool. Save only into the user-approved output directory. Verify that every figure reference is described and every described reference is present. SVG output is a draft; assess EPO drawing conventions and obtain appropriate PDF/filing-format conversion separately.

## Phase 6 — EPO review

Call `review_epo_claims` with `claims_text` for Art. 84 EPC claim review, `review_epo_specification` with `claims_text` and `specification` for Art. 83 EPC sufficiency/description review, and `check_epo_formalities` with supported fields `abstract`, `title`, `specification`, and `drawings_present`. Call `search_patent_law` with a legal question as `query` and `jurisdiction="EPO"` for legal research. A built law index is required for reliable legal references in these reviews; read the MCP resource `mpep://index/stats` first. Art. 123(2) EPC added-matter review is not implemented: explicitly mark it unchecked. Review exclusions under Arts. 52-53 with verified sources and human oversight.

## Phase 7 — Assemble and validate draft package

Create a draft package in the approved directory:

```text
epo-patent-application-[date]\
  01-research\
  02-claims\
  03-specification\
  04-figures\
  05-compliance\
  06-filing-package\  filing-checklist.md, final package notes
```

Include invention disclosure, search report and limitations, claim drafts, description, figure files/list, analyzer results, and a filing checklist. Validate actual file existence, claim dependencies, reference signs, and abstract word count. Report **draft assembled** only if the generated files exist and hard checks pass; do not describe the package as filing-ready until documents meet current filing-format requirements and qualified review is complete.

## MCP execution and cost safeguards

Use `/mcp` to discover the exact `patent-creator` tool names and exposed arguments. Keep user disclosures private. Require explicit approval before any paid search, BigQuery scan, large download, or overwriting existing work. A missing law index does not prevent diagram generation or drafting, but legal citation checks cannot be claimed complete.

**Disclaimer:** This is drafting assistance, not legal advice or a guarantee of patentability, validity, or grant. Have a qualified European Patent Attorney review the application and verify current EPO rules, fees, forms, and deadlines before filing.
