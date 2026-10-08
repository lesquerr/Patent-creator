---
name: review-formalities
description: Check US application title, abstract, description, and drawing-related formalities with the registered analyzer.
---

# US Patent Formalities Review

Use this skill to screen supplied application materials against formalities associated with MPEP 608. Ask for the title, abstract, specification, and whether drawings are present. Confirm whether the user wants a section-specific or full available review. Preserve original text; do not edit it without permission.

## Steps

1. Read MCP resource `mpep://index/stats` to confirm the law index is built if the user expects MPEP citations. The formalities tool retrieves MPEP context; without the index, mark references unavailable and do not invent citations.
2. Call `check_formalities` directly with its supported named fields.
4. Report the actual `overall_compliant`, readiness summary, abstract, title, drawings, sections, claim fee information, issues, and MPEP references returned by the tool. Do not infer a missing field passed.
5. Manually flag request/declaration completeness, signatures, fees, IDS, drawing quality, and any filing-format requirements not reported by the analyzer. Verify these against official current USPTO sources. Do not estimate fees.
6. Give prioritized corrections and distinguish mandatory legal review from analyzer suggestions. Suggest text edits, but apply them only at the user's request.

## Copilot MCP tools

Call tools directly through the configured `patent-creator` MCP server. Use `/mcp` to discover available tools and invoke the displayed registered name with its named arguments; do not guess runtime prefixes or use a subprocess runner. `check_formalities` accepts `abstract`, `title`, `specification`, and `drawings_present`. Call `search_mpep` with `query` and optional `top_k` for MPEP research. Use only citations actually returned from the local law index.

## Report

Include the application sections received, checklist status, issues with exact returned counts/locations, verified citations, unchecked material, and next actions. Do not describe automated compliance as a USPTO approval or filing guarantee.

**Disclaimer:** This is informational assistance, not legal advice, and does not replace advice from a registered patent attorney. Confirm formalities and filing requirements with current official USPTO materials and qualified counsel.
