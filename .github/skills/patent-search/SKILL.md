---
name: patent-search
description: "Search worldwide patent records with attached patent-search MCP tools using Google Patents and BigQuery, including keyword, classification, patent-detail, and family lookup workflows."
---

## Using the connected MCP server

In Copilot, connect to the configured `patent-creator` server with `/mcp` and restart Copilot after configuration changes. Discover the exposed tools and parameter schemas from that server. Invoke tools as attached MCP calls with named arguments matching the discovered schema. Server-qualified aliases vary by runtime, so invoke tools through Copilot's discovered MCP interface rather than hard-coding an alias or treating internal Python classes as exposed tools.
# Patent Search Skill

Use the attached `patent-creator` MCP tools for patent searches. Pass named
arguments matching the schemas discovered through Copilot; do not instantiate
searcher classes as if they were tools.

## When to use

- Find prior art by keyword, classification, or family.
- Pull full patent records (title, abstract, claims, description) for US patents.
- Cross-reference an EP/WO patent into its US family member to get full text.

## Available MCP tools

| Tool | What it does |
|------|--------------|
| `search_patents_google` | **Recommended.** Full-text keyword search worldwide, one search credit per call. Needs `SERPAPI_API_KEY` (free plan: 250/month). Results contain matching snippets, not complete claims/description. |
| `check_google_patents_status` | Is the key set, and how many searches are left this month (free to call). |
| `search_patents_bigquery` | Fallback keyword search across title / abstract / claims (US only for claims). ~341 GiB, about $2, per search. |
| `get_patent_bigquery` | Patent details by publication number: bibliographic data + claims by default; abstract and description are opt-in. |
| `get_patents_bigquery` | Same, for up to 50 patents in one query at the cost of one lookup. |
| `search_patents_by_cpc_bigquery` | Search by CPC classification prefix. |
| `search_patents_by_ipc_bigquery` | Search by IPC classification prefix (good for older or non-US patents). |
| `search_patent_family_bigquery` | All publications sharing a family ID across jurisdictions. |
| `check_bigquery_status` | Verify auth and quota project before a long workflow. |

## Cost notes

BigQuery on-demand pricing is $6.25 / TiB (1 TiB free per month). The MCP server enforces a per-query bytes-billed ceiling, defaulting to 350 GiB. Override via `PATENT_BIGQUERY_MAX_BYTES_BILLED` if you need a larger scan window.

The patents table is unclustered, so a detail lookup costs the same for one patent or fifty; the cost depends only on which sections are requested:

| Detail lookup | Scan | Cost |
|---|---|---|
| Bibliographic only (`include_claims=False`): title, dates, family_id, CPC/IPC | ~44 GiB | ~$0.27 |
| Default: + claims | ~160 GiB | ~$1 |
| + abstract (`include_abstract=True`) | +~200 GiB | exceeds the default cap together with claims |
| + description (`include_description=True`) | ~1.1 TiB | exceeds the default cap |

So: batch with `get_patents_bigquery`, pass `include_claims=False` when you only need codes or `family_id`, and take abstracts from the search results rather than re-fetching them.

## Choosing keywords

`search_patents_google`:
- All words must match; "double quotes" match an exact phrase. No stemming, so search synonyms and plurals separately.
- Lead with the invention's distinctive terms. Common words match thousands of patents and push the closest art down; in testing, adding "heart valve" to a query buried the target past #300, while its distinctive claim words found it at #48.
- Use `limit=100`: it costs the same one credit as `limit=10`.
- Stay inside a classification by adding a full CPC group: `"voice biometric" CPC=G10L17/00` (a bare `CPC=G10L17` finds nothing).
- Results show one row per publication, so a US patent and its EP family member can both appear.

`search_patents_bigquery` (fallback):
- 2-3 keywords work better than long phrases (BigQuery `LIKE` matching is literal).
- For non-US patents, `claims` is empty in the dataset; the MCP keyword tool already searches title/abstract for those jurisdictions. For full text on EP/WO, use the EPO OPS tools instead.
- Use `search_patent_family_bigquery` to bridge from an EP/WO hit to its US family member when you need claims.

## Common workflows

**Prior art sweep:**
1. `search_patents_google` with `query`, `limit=100`, and optional country/date filters — broad full-text scan (fallback: `search_patents_bigquery` with the corresponding fields).
2. Pick the top hits' CPC codes with one `get_patents_bigquery` call using `patent_numbers` and `include_claims=false`.
3. Search adjacent technology with `search_patents_google` using `query` and `limit`; or use `search_patents_by_cpc_bigquery(cpc_code, limit, country)` while accounting for BigQuery scan costs.

Discover tool schemas through Copilot's MCP interface and use the exact named
arguments. Do not claim missing credentials or unavailable services as
zero-result searches.

**Cross-jurisdiction lookup:**
1. Call `search_patents_google` with named arguments `query` and
   `country="EP"` (fallback: `search_patents_bigquery` with those fields).
2. Pass the publication numbers to `get_patents_bigquery` as
   `patent_numbers`, with `include_claims: false`, to get their family IDs.
3. Invoke `search_patent_family_bigquery` with the returned `family_id` to
   find related US publications.
