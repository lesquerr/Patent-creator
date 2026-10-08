---
name: search-epo
description: Search European patent publications through EPO OPS and optionally approved Google Patents or BigQuery queries.
---

# European Patent Search

Use this skill to search for EP publications and organize results for research. Ask for technical terms, synonyms, applicant/inventor names, IPC/CPC codes, filing/publication dates, countries, and desired result count. Keep queries focused and record each source and search scope; do not claim the results are exhaustive.

## Search workflow

1. **Start with EPO OPS.** Use `search_epo_patents` with a CQL query and `limit` (maximum 100 per the registered function). CQL supports simple keywords and fields such as `ta=`, `ti=`, `in=`, `pa=`, `ic=`, and `pd=`. This returns bibliographic data and abstracts; do not claim it returns full claims or complete description unless the actual result does.
2. **Expand only with approval.** Google Patents searches consume SerpApi credits; BigQuery reads can become billable after free quota. Do not run either paid or potentially billable search without explicit approval. Prefer OPS first; never auto-fallback into a paid query.
3. **Use the exact tool fields.** `search_patents_google` accepts `query`, `limit`, `country`, `start_year`, and `end_year`. BigQuery keyword search accepts `query`, `limit`, `country`, `start_year`, and `end_year`; CPC search accepts `cpc_code`, `limit`, and `country`. Use only the registered MCP tool arguments shown by `/mcp`; there are no `--cpc` or `--year-range` CLI switches.
4. **Inspect relevant results.** Record publication number, title, applicants, inventors, dates, classification codes, family identifier, and abstract only as returned. De-duplicate publications/families where possible and distinguish applications from granted publications by kind code.
5. **Analyze and report.** Compare actual disclosures to the user's described features, explain similarities and differences, record unsearched jurisdictions/languages and missing text, and suggest focused follow-up queries. Do not call a result novelty-destroying or provide a freedom-to-operate opinion without qualified analysis.

## Copilot MCP tools

Call tools directly through the configured `patent-creator` MCP server. Use `/mcp` to discover available tools and invoke the displayed registered name with its named arguments; do not guess runtime prefixes or use a subprocess runner. Call `search_epo_patents` with `query` and optional `limit` for EPO OPS. Invoke paid-capable alternatives only after explicit approval and confirmation of the expected charge/credit use. Keep unpublished invention details private; do not send them to an external search provider without the user's informed approval.

## Result presentation

Present only actual returned records. For example, summarize a result using its returned `publication_number`, `title`, `applicants`, `inventors`, `filing_date`, `publication_date`, `ipc_codes`, `cpc_codes`, and `family_id` fields when present; omit fields the source did not return. Add a short evidence-based relevance note, query/source/date, and limitations. Don't invent example patents, legal statuses, or search counts. Cite returned legal materials separately from patent search results.

**Disclaimer:** Patent searching is preliminary research, not legal advice, a patentability opinion, or a freedom-to-operate analysis. A qualified patent professional should review relevant documents and current legal status.
