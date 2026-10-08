---
name: check-pct-formalities
description: "Check a PCT application against the available PCT formalities analyzer and prepare a cited correction checklist."
---

## Copilot MCP tools

Call tools directly through the configured `patent-creator` MCP server. Use `/mcp` to confirm the server and discover its exposed tools, then invoke the displayed registered tool with named arguments from its schema. Do not guess runtime-qualified prefixes or replace tool calls with a Python runner. Treat a tool error as an explicit prerequisite failure; do not claim a search or review ran when it did not.
# PCT Formalities Check

Use this skill to review an international application against PCT formality requirements. Ask the user to provide the application text or identify a local file they authorize you to read. Collect the request form details, description, claims, abstract, drawings, sequence-listing status, receiving office, and International Searching Authority separately; do not assume missing facts.

## Review workflow

1. **Scope the review.** Ask whether they want the request, description, claims, abstract, drawings, physical requirements, unity, or all available checks. Identify missing sections and distinguish text supplied for review from assumptions.
2. **Check the law source.** Call `search_patent_law` with a focused legal question as `query` and `jurisdiction="PCT"` to find relevant requirements and cite returned source names and sections. Citation-enriched formalities checks require the law index; read the MCP resource `mpep://index/stats` to check its availability. If it is not built, explain citations are unavailable and offer setup only with permission for required large downloads.
3. **Run the available formalities analyzer.** The registered `check_pct_formalities` function accepts only `abstract`, `title`, `specification`, and `drawings_present`; it does not accept a request form, a separate claims field, fee data, priority documents, a sequence listing, or an ISA selection. Put supplied description/claims text in `specification` only when appropriate, and disclose which material was actually checked. Do not report these unsupported checks as passed.
4. **Review the result.** Report the analyzer's actual status and issues. Separately list unchecked requirements—request completeness, priority documents, language, unity, fees, deadlines, and sequence-listing details—as items requiring human verification. Do not calculate filing fees or deadlines from memory; refer to current WIPO/receiving-office sources.
5. **Prepare prioritized corrections.** For each issue, state its source citation if returned, the affected section, the evidence, and a practical next step. Keep suggestions distinct from legal conclusions.
6. **Close with a checklist.** Summarize checked, failed, not checked, and user-supplied assumptions. Recommend review by a qualified patent professional before filing.

## Registered calls

Call `check_pct_formalities` with named arguments `abstract`, `title`, `specification`, and `drawings_present`; call `search_patent_law` with the relevant `query`, `jurisdiction="PCT"`, and optional `top_k`. Pass the supplied text only as tool arguments and use the returned results in the report.

## Requirements covered in the manual checklist

Use the applicable requirements under Rule 4 PCT (request), Rule 5 (description), Rule 6 (claims), Rule 8 (abstract), Rule 11 (drawings and physical requirements), Rule 12 (sequence listings/language), and Rule 13 (unity). Confirm current requirements against official WIPO materials. Report that the analyzer does not verify all of these fields.

## Report and limitations

Label the report **automated assistance, not a legal opinion**. Do not invent citations, fee totals, deadlines, or a pass result for information the tool did not inspect. Preserve the user's source text; make edits only when requested and keep proposed wording separate from the original.

**Disclaimer:** This workflow is informational, not legal advice, and does not replace advice from a registered patent attorney or agent. Confirm PCT requirements with qualified counsel and official WIPO/receiving-office sources before filing.
