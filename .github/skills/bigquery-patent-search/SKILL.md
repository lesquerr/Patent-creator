---
name: bigquery-patent-search
description: "Fast, cloud-based patent searching across 100 million+ worldwide patents using Google BigQuery - keyword search, CPC classification, patent details retrieval"
---

## Using the connected MCP server

In Copilot, connect to the configured `patent-creator` server with `/mcp` and restart Copilot after configuration changes. Discover the exposed tools and parameter schemas from that server. Invoke tools as attached MCP calls with named arguments matching the discovered schema. Server-qualified aliases vary by runtime, so invoke tools through Copilot's discovered MCP interface rather than hard-coding an alias or treating internal Python classes as exposed tools.
# BigQuery Patent Search Skill

Fast, cloud-based patent searching across 100 million+ worldwide patents using Google BigQuery.

## When to Use

Invoke this skill when users ask to:
- Search for prior art patents
- Find patents in a specific technology area
- Search by CPC classification code
- Look up patent details by publication number
- Conduct freedom-to-operate searches
- Research patent landscapes

## What This Skill Does

Provides access to Google's public patent dataset:

1. **Keyword Search** across 100M+ patents:
   - Full-text search of titles, abstracts, claims
   - Filter by country (US, EP, JP, CN, etc.)
   - Filter by filing/grant date ranges
   - Fast cloud-based queries (< 5 seconds)

2. **CPC Classification Search**:
   - Search by CPC code (e.g., "G06F16/", "H04L29/06")
   - Browse patent classifications
   - Find patents in specific technical domains

3. **Patent Details Retrieval**:
   - Get full patent text by publication number
   - Access title, abstract, claims, description
   - View CPC codes, inventors, assignees
   - See filing and grant dates

## Required Setup

This skill requires Google Cloud authentication:

**Prerequisites**:
1. Google Cloud Project (free to create)
2. BigQuery API enabled; query usage may incur charges
3. Application Default Credentials configured

**Setup Commands**:
```powershell
# Install Google Cloud SDK (if not installed)
# Visit: https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth application-default login

# Set project (get ID from console.cloud.google.com)
$env:GOOGLE_CLOUD_PROJECT = "your-project-id"
```

**Environment Variable**:
Set in `.env` file: `GOOGLE_CLOUD_PROJECT=your-project-id`

## How to Use

When this skill is invoked:

Use the attached MCP tools with named arguments matching the schemas
discovered from `patent-creator`; do not construct `BigQueryPatentSearch`
directly:

1. Keyword search: `search_patents_bigquery` with `query`, `limit`,
   `country`, and optional `start_year` / `end_year`.
2. CPC search: `search_patents_by_cpc_bigquery` with `cpc_code`, `limit`,
   and `country`.
3. Details: `get_patent_bigquery` with `patent_number`. Claims are included
   by default; abstract and description are opt-in. Use
   `get_patents_bigquery` with `patent_numbers` for up to 50 records in one
   query.

Before invoking a tool, discover its current schema through Copilot's MCP
tool interface. BigQuery requires a project and Application Default
Credentials; missing configuration is an explicit tool error, not an empty
search result. **Before any patent search, detail lookup, CPC search, or test
script that issues BigQuery queries, explain that Google Cloud may charge for
the query and obtain the user's explicit approval.** Do not treat the public
dataset or free-tier allowance as making a query free. Without approval, do
not issue a query; for basic setup troubleshooting, use the
`check_bigquery_status` MCP tool first.

## BigQuery Dataset

Uses `patents-public-data.patents` on Google BigQuery:
- **100M+ worldwide patents**
- **12M+ US patents** with full text
- Updated weekly
- Publicly available dataset; querying it may incur Google Cloud BigQuery
  charges depending on bytes processed, billing configuration, and applicable
  free-tier allowance.

## Search Result Format

Each result includes:
```python
{
    "publication_number": "US10123456B2",
    "title": "Method and system for...",
    "abstract": "A system for...",
    "filing_date": "2019-01-15",
    "grant_date": "2020-06-30",
    "country": "US",
    "cpc_codes": ["G06F16/245", "H04L29/06"],
    "inventors": ["John Doe", "Jane Smith"],
    "assignee": "Example Corp"
}
```

Full patent details also include:
- `claims`: Full text of all claims
- `description`: Complete description section
- `priority_date`: Earliest priority date
- `family_id`: Patent family ID

## Presentation Format

Present search results as:

```
PATENT SEARCH RESULTS
====================

Query: "blockchain authentication"
Found: 247 patents (showing top 20)
Date Range: 2020-2024
Country: US

[1] US10123456B2 - System for blockchain-based authentication
    Assignee: Example Corp
    Filed: 2019-01-15 | Granted: 2020-06-30
    CPC: G06F16/245, H04L29/06

    Abstract: A system for authenticating users using blockchain
    technology with distributed ledger verification...

[2] US10234567B1 - Method of secure authentication using blockchain
    ...

---

Top 5 Most Relevant:
1. US10123456B2 (95% relevance)
2. US10234567B1 (92% relevance)
...
```

## Advanced Search Techniques

1. **Boolean Operators** in queries:
   - "blockchain AND authentication"
   - "encryption OR cryptography"
   - "(mobile OR wireless) AND security"

2. **Phrase Search**:
   - "distributed ledger technology"
   - "public key infrastructure"

3. **CPC Code Hierarchies**:
   - "G06F" = Computing
   - "G06F16/" = Information retrieval
   - "G06F16/245" = Structured query language

## Common CPC Codes

- **G06F**: Computing, calculating, counting
- **H04L**: Digital communication
- **G06Q**: Business methods
- **H04W**: Wireless communication
- **G06N**: Computer systems based on specific models
- **G06T**: Image processing

## Error Handling

If BigQuery is not configured:
1. Check if `google-cloud-bigquery` is installed
2. Verify authentication: `gcloud auth application-default login`
3. Confirm project ID in environment: `GOOGLE_CLOUD_PROJECT`
4. Use the attached MCP tool `check_bigquery_status` for a basic status check.
   Do not run `scripts/test_bigquery.py` without explicit user approval: it
   executes keyword, detail, and CPC queries that may incur BigQuery charges.

## Cost Considerations

BigQuery pricing:
- Queries may incur charges according to the Google Cloud billing account's
  pricing, bytes processed, and any applicable free-tier allowance.
- **Bytes-billed ceiling**: enforced per-query via `PATENT_BIGQUERY_MAX_BYTES_BILLED` (default 350 GiB)

Never describe BigQuery as unconditionally free. Get explicit user approval
before each search, detail lookup, CPC query, or query-based test. For initial
troubleshooting that does not need patent results, prefer
`check_bigquery_status`; do not run query-based tests without approval.

## Tools Available

- **MCP tools**: `check_bigquery_status`, `search_patents_bigquery`,
  `search_patents_by_cpc_bigquery`, `get_patent_bigquery`, and
  `get_patents_bigquery`
- Save results through the host's normal file-writing workflow; the tool
  returns JSON and does not create result files.
