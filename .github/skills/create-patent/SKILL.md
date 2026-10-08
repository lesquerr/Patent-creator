---
name: create-patent
description: "Guide a user through a US patent application draft, from invention disclosure and prior-art search through package checks."
---

## Copilot MCP tools

Call tools directly through the configured `patent-creator` MCP server. Use `/mcp` to confirm the server and discover its exposed tools, then invoke the displayed registered tool with named arguments from its schema. Do not guess runtime-qualified prefixes or replace tool calls with a Python runner.
# Create a US Patent Application Draft

This skill coordinates a complete drafting workflow. It does not file an application or produce a filing-ready package automatically. Ask for the user's preferred output directory and guided or autonomous drafting style. In guided mode, pause at the checkpoints below; in autonomous mode, still ask when key technical facts or cost approvals are missing.

## Phase 1 — Step 1: Invention disclosure

Interview the inventor about the problem, how the invention works, components or method steps, what is believed to be new, alternatives, examples/prototypes, and known related work. Separate facts from assumptions, retain the inventor's terminology, and flag unclear or missing disclosure.

## Phase 2 — Prior-art search

Define distinctive features, keywords and synonyms, search dates, and CPC classes. Search in stages: initial keywords, review actual returned publications, refine terms/classes, then analyze the most relevant references and timelines. Call `search_patents_google` with `query`, `limit`, and any applicable country/year filters; it consumes search credits. When relevant, call `search_patents_bigquery` with `query`, `limit`, `country`, and optional years, or `search_patents_by_cpc_bigquery` with `cpc_code`, `limit`, and `country`. BigQuery scans may be billable. Do not run paid or potentially billable searches without explicit approval. Never treat a limited search as exhaustive or claim a patentability conclusion is legal advice.

## Phase 3 — Claims

Draft one or more independent claims and dependent fallbacks around disclosed distinctions, with consistent terminology and dependency. Do not add technical features that the inventor did not disclose. Explain alternatives and tradeoffs; the user must verify claim scope.

## Phase 4 — Specification

Prepare title, abstract, field, background, summary, brief figure descriptions, detailed embodiments, examples, and claim support. Check that each claim limitation has written-description support and that a skilled person could make and use the embodiments. Do not promise page counts or legal sufficiency.

## Phase 5 — Diagrams

Identify useful method flowcharts and system/block diagrams. Call `create_flowchart` with `steps`, `filename`, `output_format`, and `output_dir`; call `create_block_diagram` with `blocks`, `connections`, `filename`, `output_format`, and `output_dir`; or call `render_diagram` with `dot_code`, `filename`, `output_format`, `engine`, and `output_dir`. Use only fields exposed by the selected tool. Use consistent reference numerals, save in the approved output location, and cross-check each numeral against the description. Figures are draft SVG/PNG unless separately converted and verified for filing.

## Phase 6 — Compliance review

Call `review_patent_claims` with `claims_text` for 35 USC 112(b), `review_specification` with `claims_text` and `specification` for 35 USC 112(a), and `check_formalities` with supported `abstract`, `title`, `specification`, and `drawings_present` fields on the exact final draft. Call `search_mpep` or `search_patent_law` for returned citations where appropriate. Read the MCP resource `mpep://index/stats` first when citations are required. The analyzers are screening aids, not legal determinations. Resolve or explicitly disclose critical results; never silently mark an issue as fixed.

## Phase 7 — Assemble and validate

Create the following draft structure only in the user's chosen output folder:

```text
patent-application-[date]\
  01-research\       disclosure, search report, preliminary assessment
  02-claims\         claim drafts and final reviewed claims
  03-specification\ full description and abstract
  04-figures\        SVG figures and figure description
  05-compliance\     claims, specification, and formalities reports
  06-filing-package\ filing checklist, IDS list, validation report
```

Hard checks before calling the draft complete: required files exist; abstract is 50-150 words; every figure numeral is supported by the description and every described figure numeral appears; claim dependencies are checked; and critical analyzer issues are resolved or clearly remain open. A missing DOCX/PDF is an expected manual conversion step, not a successful filing-format check. State separately:

- **Drafting complete:** generated draft files exist and hard checks pass.
- **Filing-ready:** not established by this workflow; the user must convert to current required formats, verify filing procedures, and complete professional review.

Do not estimate fees. Refer to the live USPTO fee schedule and Patent Center. Preserve citations as returned; never create placeholder patent references that look real.

## MCP tool and cost safeguards

Use `/mcp` to discover the connected `patent-creator` server and its exposed named arguments. Keep sensitive drafts private. Require explicit approval for paid patent queries, potentially billable BigQuery scans, large downloads, and overwriting files. Claims and US-law review citations require the law index; drafting and diagrams can continue without it, but do not claim citations were verified.

## Review checkpoints

In guided mode, pause after prior-art research, claims, specification, and compliance/figures. At each checkpoint ask the user to verify technical accuracy and approve proceeding. In autonomous mode, report each phase and retain uncertainty in the final report.

**Disclaimer:** This is drafting assistance, not legal advice or a patentability opinion. A registered patent attorney should review the application before filing. The workflow does not submit anything to the USPTO; confirm current Patent Center procedures, filing formats, fees, and deadlines from official sources.
