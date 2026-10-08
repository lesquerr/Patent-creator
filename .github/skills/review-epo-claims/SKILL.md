---
name: review-epo-claims
description: Review supplied European patent claims for Art. 84 EPC clarity, conciseness, support, and claim structure.
---

# EPO Claims Review

Use this workflow for a supplied claim set intended for a European patent application. Request the claims and, for support analysis, the relevant description. The registered claims tool accepts `claims_text` only; its support checks do not replace a full description review. Preserve the original text and ask before applying edits.

## Process

1. Confirm the target is EPO/European practice and record the user's focus (clarity, conciseness, support, or all).
2. Confirm the legal-source index is available by reading MCP resource `mpep://index/stats`. The registered analyzer retrieves EPC guidance through the local law index. If no index is built, report that citation retrieval is unavailable and do not invent legal references.
3. Call `review_epo_claims` directly with the supplied `claims_text`.
4. Review actual output for clarity, conciseness, description support, claim dependencies/categories, and two-part form under Rule 43(1) where appropriate. Report the tool's returned score, issues, severity, summary, and EPC references without converting them into a grant prediction.
5. Check the description separately for Art. 84 support in context and identify what additional evidence would be needed. Two-part form has exceptions; do not state it is invariably mandatory.
6. Art. 123(2) EPC added-matter review is not implemented. Mark added-matter as **not checked** and do not imply an Art. 84 result covers it.
7. Provide possible fixes with the affected claim and explanation. Keep recommendations separate from the user's text; make changes only when explicitly asked.

## Copilot MCP tools

Call tools directly through the configured `patent-creator` MCP server. Use `/mcp` to discover available tools and invoke the displayed registered name with its named arguments; do not guess runtime prefixes or use a subprocess runner. Call `review_epo_claims` with `claims_text`, and call `search_patent_law` with the question as `query`, `jurisdiction="EPO"`, and optional `top_k`. Keep the claim text private.

## Output

Summarize claim count if available, score and issue counts if returned, critical/important/minor findings, citations, unchecked matters, and next steps. If the user requests a saved deliverable, use a dated `epo-claims-review-[date]\` folder with `analysis-report.md`, `critical-issues.md`, `suggested-fixes.md`, and `epc-citations.md`. Save the original or a proposed fixed claims file only with permission; do not overwrite supplied material. Do not call the claims "EPO-ready" solely because an automated score is high.

**Disclaimer:** This tool provides informational drafting assistance, not legal advice. A qualified European Patent Attorney should assess the claims and current EPO practice before filing or responding to an objection.
