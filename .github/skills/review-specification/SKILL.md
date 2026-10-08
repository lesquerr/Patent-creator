---
name: review-specification
description: Review a US patent specification for written-description, enablement, best-mode, and claim-support concerns.
---

# US Specification Review

Use this workflow to review an existing specification alongside its claims. Ask the user to provide both texts or identify local files they authorize you to read. Preserve both source documents. The analyzer reports potential issues; it does not make a legal determination.

## Review steps

1. Confirm the desired focus: written description, enablement, best mode, claim support, or all available checks.
2. Read MCP resource `mpep://index/stats` to confirm the law index is built when MPEP citations are requested. The registered review tool retrieves citation context; without the index, report references unavailable rather than fabricating them.
3. Call the `review_specification` MCP tool with `claims_text` and `specification`.
5. Report the actual analysis type, specification paragraphs/indexed terms, issues and categories, coverage, summary, compliance result, and MPEP references returned. Include warnings/skipped checks from output where present.
6. Analyze support by mapping each claim limitation to disclosed paragraphs/examples. Distinguish express disclosure, reasonable inference, and absent or uncertain support. Do not fill gaps with new technical matter.
7. Identify potential enablement breadth concerns and best-mode disclosure questions without making unsupported legal conclusions. Give specific questions or proposed clarifying language, and do not alter the source unless the user approves.
8. Provide a prioritized report and list unreviewed evidence, assumptions, and follow-up needed from the inventor or attorney.

## Copilot MCP tools

Call tools directly through the configured `patent-creator` MCP server. Use `/mcp` to discover available tools and invoke the displayed registered name with its named arguments; do not guess runtime prefixes or use a subprocess runner. Call `search_mpep` with a focused `query` only after confirming the index is available. Keep claim/specification text private.

## Report format

Summarize the document and claims provided, written-description findings, enablement concerns, best-mode issues, claim-support matrix, verified MPEP sources, severity and next actions. Clearly label anything not checked.

**Disclaimer:** This is automated drafting support, not legal advice or a legal opinion. A registered patent attorney should evaluate written description, enablement, best mode, and prosecution strategy before filing.
