---
name: search-prior-art
description: Conduct a structured preliminary patent prior-art search and report evidence, limitations, and follow-up questions.
---

# Preliminary Prior-Art Search

Use this workflow to organize a prior-art investigation, not to render a legal patentability or freedom-to-operate opinion. Ask the inventor to describe the problem, solution, key technical features, alternatives, and what they believe is new. Do not send unpublished invention details to an external service unless the user approves that disclosure and any associated cost.

## Seven-step (7-step) search

1. **Define the invention.** Extract technical features, their relationships, and possible claim elements. Ask the user to confirm the summary.
2. **Develop terminology.** Prepare distinctive keywords, synonyms, technical terms, and possible CPC/IPC areas. Avoid broad generic terms as the only query.
3. **Broad search.** Search Google Patents or BigQuery only after explicit approval for any paid/credit-consuming or potentially billable query. Google Patents search uses a limited SerpApi credit quota; BigQuery can scan hundreds of GiB and may cost about $2 per search beyond applicable free quota. Do not auto-fallback from one paid source to another.
4. **Classifications.** Extract classes only from actual returned results; verify codes and descriptions rather than guessing. Use CPC search only after the same cost approval.
5. **Focused searches.** Refine keyword/classification searches, dates, and jurisdictions. If detailed patent text is needed, first inspect the detail-tool cost notes and require approval; claims/description columns may cause large scans.
6. **Timeline and landscape.** Summarize actual publication/filing dates and classifications returned. Note coverage limits, duplicate family publications, missing full text, and unsearched languages/offices.
7. **Preliminary assessment.** Compare each relevant reference against the user's actual features. Separate exact disclosures, similarities, and differences. Avoid assigning authoritative novelty/obviousness scores; identify questions for a patent professional.

## Copilot MCP search tools

Call tools directly through the configured `patent-creator` MCP server. Use `/mcp` to discover available tools and invoke the displayed registered name with its named arguments; do not guess runtime prefixes or use a subprocess runner. `search_patents_google` accepts `query`, `limit`, `country`, `start_year`, and `end_year`. `search_patents_by_cpc_bigquery` accepts `cpc_code`, `limit`, and `country`. Do not call either until the user explicitly approves the expected cost/credit use. Keep unpublished invention details private.

## Report contents

Create a search log with date, database, query, filters, actual results inspected, and limitations. Present the top relevant publications with identifiers, title, source, dates, returned abstracts/snippets, similarities, differences, and why follow-up may be useful. Include search terms/classes actually used, not invented statistics. An IDS list may include only publication identifiers actually reviewed; remind the user to verify disclosure requirements.

If the user asks for saved deliverables, use a dated `prior-art-search-[date]\` directory with `search-report.md`, `top-10-patents.md`, `ids-list.md`, and `claim-strategy.md`; include raw data only when the source actually returned it and the user approves saving it. Do not fabricate sample patent numbers or sample search counts.

State conclusions as preliminary hypotheses, not "high/medium/low" legal findings. Recommend attorney review and a separate claim-focused analysis before filing.

**Disclaimer:** This is research assistance, not legal advice, a patentability opinion, or an exhaustive prior-art search. A registered patent attorney or qualified search professional should assess the evidence and current law.
