---
name: full-review
description: Coordinate an end-to-end US application review using the registered claims, specification, and formalities analyzers.
---

# Complete Application Review

Use this skill when the user supplies a complete or substantially complete US application. Collect claims, specification, abstract, title, and drawing information. If they have only one section, narrow the review and state what was not checked. Use the configured `patent-creator` MCP server; use `/mcp` to inspect its available tools and invoke each displayed tool directly with its named arguments. Do not guess runtime-qualified prefixes or use a subprocess runner.

## Review sequence

1. **Intake and scope:** confirm application version, jurisdiction, and whether drawings are present. Keep the supplied text unchanged; do not overwrite it.
2. **Claims review:** call `review_patent_claims` with the exact `claims_text`.
3. **Specification review:** call `review_specification` with `claims_text` and `specification`.
4. **Formalities review:** call `check_formalities` with the available `abstract`, `title`, `specification`, and `drawings_present` value.
5. **Citation checks:** read the MCP resource `mpep://index/stats` first; a built law index is required for citations in claims/US reviews. Then call `search_mpep` with a focused `query` for US patent-law support and cite only source passages returned. If the index is missing, stop citation searches, label citations unavailable, and offer the setup skill only with consent to required downloads.
6. **Synthesis:** merge overlapping issues, retain each analyzer's severity and evidence, and distinguish analyzer output from reviewer interpretation. Prioritize critical issues, then important issues, then minor improvements. Show section/location when returned; don't fabricate line numbers, authority, or scores.
7. **Action list:** list concrete next steps, unresolved assumptions, and what requires attorney judgment. Suggest edits, but apply changes only after the user requests them.

## Registered tool calls

Call `review_patent_claims` with `claims_text`; call `review_specification` with `claims_text` and `specification`; call `check_formalities` with supported `abstract`, `title`, `specification`, and `drawings_present` fields. Retain returned results for the report and protect the source text. Optional prior-art research is a separate step and requires explicit approval before any paid/credit-consuming query or potentially billable BigQuery scan.

## Consolidated report

Include an executive summary; separate critical, important, and minor issues; claims, written-description/enablement, and formalities sections; verified MPEP references; missing evidence; and prioritized actions. State which inputs were absent. Do not call the application ready to file based only on automated results.

**Disclaimer:** Automated checks are screening assistance, not legal advice or a guarantee of acceptance. A registered patent attorney should review the application and confirm current USPTO requirements before filing.
