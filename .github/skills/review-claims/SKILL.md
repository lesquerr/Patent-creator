---
name: review-claims
description: Analyze supplied US patent claims for 35 USC 112(b) concerns with returned evidence and MPEP references.
---

# US Patent Claims Review

Use this workflow for an existing claim set, not to invent claims on the user's behalf. Ask the user to paste the claims or identify a local file they authorize you to read. Preserve the original claims exactly and confirm whether they want review only or proposed edits.

## Analysis

1. Record the number of claims and identify independent/dependent claims if the supplied text permits.
2. Confirm the US law index is built before promising MPEP citations. `review_patent_claims` needs the index to retrieve citation context. If unavailable, report the blocker and do not fabricate citations.
3. Call the registered `review_patent_claims` MCP tool directly with `claims_text`.
4. Explain actual returned results, including compliance score, claim counts, issue totals, severity categories, issues, summary, references, and `checks_skipped` where present. Preserve any skipped-check disclosure verbatim or faithfully.
5. Discuss concerns in context: antecedent basis, definiteness, subjective or relative terms, claim structure and dependencies, cross-references, and possible means-plus-function wording. Treat these as issues for attorney review, not conclusive rejection predictions.
6. For each item, quote only the relevant user text, identify its claim/location when supplied by the analyzer, explain the potential concern, and suggest a possible revision or question. Do not make an edit without explicit authorization.
7. Rerun only after the user supplies or approves revised text; compare results without overstating improvement.

## Copilot MCP tools

Call tools directly through the configured `patent-creator` MCP server. Use `/mcp` to discover available tools and invoke the displayed registered name with its named arguments; do not guess runtime prefixes or use a subprocess runner. Call `review_patent_claims` with `claims_text`. Read resource `mpep://index/stats` before citation work and call `search_mpep` with a focused `query` only when the index is available. Use returned section/page data and do not invent pinpoint citations.

## Report

Provide a concise summary, issues grouped by returned severity, claim-structure observations, verified MPEP references, omitted checks, and recommended next actions. If the user requests a saved deliverable, use a dated `claims-review-[date]\` folder containing `analysis-report.md`, `critical-issues.md`, `suggested-fixes.md`, and `mpep-citations.md`. Save `claims-original.txt` or `claims-fixed.txt` only with the user's permission; never overwrite source files. Do not describe a score as USPTO approval or claim "ready to file" based on automated analysis.

**Disclaimer:** This automated review is informational, not legal advice, and does not replace advice from a registered patent attorney. Confirm claim scope, legal conclusions, and current USPTO practice with qualified counsel before filing.
