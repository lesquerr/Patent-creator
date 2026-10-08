---
name: mpep-search
description: "Expert system for searching USPTO MPEP, 35 USC statutes, 37 CFR regulations, and post-Jan 2024 updates."
---

## Using the connected MCP server

In Copilot, connect to the configured `patent-creator` server with `/mcp` and restart Copilot after configuration changes. Discover the exposed tools and parameter schemas from that server. Invoke tools as attached MCP calls with named arguments matching the discovered schema. Server-qualified aliases vary by runtime, so invoke tools through Copilot's discovered MCP interface rather than hard-coding an alias or treating internal Python classes as exposed tools.
# MPEP Search Skill

Search MPEP corpus through hybrid RAG (FAISS vector + BM25 keyword + HyDE + cross-encoder reranking).

**Sources:**
- MPEP: Manual of Patent Examining Procedure
- 35 USC: United States Code Title 35
- 37 CFR: Code of Federal Regulations Title 37
- Subsequent Publications: Federal Register updates (post-Jan 2024)

## Core Operations

### 1. `search_mpep`

Call the attached `search_mpep` MCP tool with named arguments matching its
discovered schema. The built legal index is required. A missing-index error
means no search was performed, not that the corpus contains no responsive
law.

**Inputs:**
- `query` (string, required): Search query (minimum 3 characters)
- `top_k` (int, optional): Number of results (default: 5, max: 20)
- `retrieve_k` (int | None, optional): Candidates before reranking (default: top_k * 4, max: 100)
- `source_filter` (string | None, optional): Filter by source (`"MPEP"`, `"35_USC"`, `"37_CFR"`, `"SUBSEQUENT"`, or `None`)
- `is_statute` (bool | None, optional): Filter for statute content
- `is_regulation` (bool | None, optional): Filter for regulation content
- `is_update` (bool | None, optional): Filter for recent updates

**Outputs:**
The tool returns a list of records. Each record contains fields such
as:
```json
{
    "rank": 1,
    "source": "MPEP",
    "section": "MPEP 2173",
    "file": "mpep-2100",
    "page": 5,
    "is_statute": false,
    "is_regulation": false,
    "is_update": false,
    "relevance_score": 0.91,
    "text": "..."
}
```

For example, call `search_mpep` with `query` set to
`enablement requirement 35 USC 112` and `top_k` set to `5` as named arguments.
For statutes, set `is_statute: true`; for updates, set `is_update: true`;
for one corpus use `source_filter` such as `"MPEP"` or `"37_CFR"`.

### 2. `get_mpep_section`

Call the attached `get_mpep_section` MCP tool with `section_number` and
optional `max_chunks`; it also requires the built legal index.

Retrieve all content from specific MPEP section.

**Inputs:**
- `section_number` (string, required): MPEP section number (e.g., `"2100"`, `"608.01"`)
- `max_chunks` (int, optional): Maximum chunks to return (default: 50)

**Outputs:**
```json
{
    "section": "2100",
    "total_chunks": 1,
    "chunks": [{"text":"...","metadata":{"source":"MPEP","section":"MPEP 2100","page":1}}]
}
```

When the section has no indexed content, the tool returns an object with an
`error` field.

The `mpep://index/stats` MCP resource provides index statistics; read it to
check index readiness before citation-dependent reviews.

**Limits:**
- `top_k` capped at 20
- `retrieve_k` validated and bounded by the registered input model

## Implementation Notes

**Index Location:**
- FAISS index: `mcp_server/index/mpep_index.faiss`
- Metadata: `mcp_server/index/mpep_metadata.json`
- BM25 index: `mcp_server/index/mpep_bm25.json`

**Search Architecture:**
1. HyDE Query Expansion (hypothetical documents)
2. Hybrid Retrieval (FAISS vector + BM25 keyword via RRF)
3. Cross-Encoder Reranking (final relevance scores)
4. Metadata Filtering (source/type filters)

**Dependencies:**
- sentence-transformers (BGE-base-en-v1.5)
- FAISS (vector search)
- rank-bm25 (keyword search)
- Cross-encoder (reranking)
- HyDE (optional, graceful degradation)

**Error Handling:**
- A missing legal index is an explicit prerequisite error. If setup was
  requested, use the existing setup guidance; legal search and citation-
  enriched reviews remain unavailable until the corpus is built.
- Invalid input and missing section content are distinct from an empty
  search result.
- HyDE may be disabled by configuration; this does not mean retrieval failed.
