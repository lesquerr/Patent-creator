---
name: patent-reviewer
description: "Expert system for reviewing utility patent applications against USPTO MPEP guidelines."
---

## Using the connected MCP server

In Copilot, connect to the configured `patent-creator` server with `/mcp` and restart Copilot after configuration changes. Discover the exposed tools and parameter schemas from that server. Invoke tools as attached MCP calls with named arguments matching the discovered schema. Server-qualified aliases vary by runtime, so invoke tools through Copilot's discovered MCP interface rather than hard-coding an alias or treating internal Python classes as exposed tools.
# Patent Reviewer Skill

Comprehensive USPTO application review workflow using the registered native
analysis, search, and diagram tools. This review is not legal advice.

## When to Use

Review patent applications for USPTO compliance, analyze claims/specifications/formalities, integrate prior art, get USPTO guidance, assist with patent drafting.

## Related skills

Use the `full-review` skill for complete review, `review-claims` for claims,
`review-specification` for written-description/enablement review,
`review-formalities` for MPEP 608, and `patent-application-creator` to draft
a new application.

## Available MCP tools

### MPEP & Regulations

- `search_mpep` - Search MPEP, 35 USC, 37 CFR
- `get_mpep_section` - Get complete MPEP section by number

### Patent Search

- `search_patents_google` - Full-text search worldwide, claims included (recommended)
- `search_patents_bigquery` - Fallback keyword search (~$2 a search)
- `get_patent_bigquery` - Get patent details (claims by default; abstract/description opt-in)
- `get_patents_bigquery` - Details for up to 50 patents in one query, same cost as one
- `search_patents_by_cpc_bigquery` - Search by CPC classification

### Patent Analysis

- `review_patent_claims(claims_text)` - Analyze claims for 35 USC 112(b)
- `review_specification(claims_text, specification)` - Check support under 112(a)
- `check_formalities(abstract, title, specification, drawings_present)` -
  Check MPEP 608 formalities

These US reviews use MPEP references and require the built legal index.
Report a missing-index error as a skipped review, not a clean result. Preserve
any `checks_skipped` disclosure in claim-review reporting.

### Diagram Generation

- `render_diagram` - Create diagrams from DOT code
- `create_flowchart` - Generate patent-style flowcharts
- `create_block_diagram` - Create system block diagrams
- `add_diagram_references` - Add reference numbers

## Review Workflows

### Complete Patent Review

Runs the available analyzers as separate attached MCP calls for a
comprehensive analysis:

**Output:**
- All compliance issues across components
- Severity ratings (critical/important/minor)
- Specific MPEP citations
- Actionable fix recommendations
- Prioritized remediation plan

### Claims-Only Review

**35 USC 112(b) Compliance:**
- Antecedent basis
- Definiteness
- Claim structure
- Subjective terms
- Means-plus-function compliance

### Specification Review

**35 USC 112(a) Requirements:**
- Written description
- Enablement
- Best mode
- Claim support

### Formalities Check

**MPEP 608 Compliance:**
- Abstract (50-150 words)
- Title (<=500 characters)
- Drawing references
- Required sections

## Patent Creation Workflow

Complete 6-phase patent drafting (55-80 minutes):

1. **Discovery (10-15 min)** - Gather invention details
2. **Technology Analysis (5 min)** - Assess patentability (101, 102, 103)
3. **Specification Drafting (15-20 min)** - Background, summary, detailed description
4. **Claims Drafting (10-15 min)** - Independent + dependent claims
5. **Diagrams & Abstract (10-15 min)** - Block diagrams, flowcharts, abstract
6. **Automatic Validation (5-10 min)** - Run the review tools below and
   resolve findings; use the `full-review` skill for the combined workflow.

**Output:** USPTO-ready filing package with diagrams

## MPEP Research

Call the attached `search_mpep` tool with named arguments `query` and `top_k`;
optionally pass `source_filter` (for example `"35_USC"` or `"MPEP"`). Retrieve
a section by calling `get_mpep_section` with `section_number` set to `"2173"`.
A built legal index is required.

### Common MPEP Sections

| Section | Topic |
|---------|-------|
| 608 | Formalities (abstract, title, drawings) |
| 2100 | Patentability requirements |
| 2163 | Guidelines for 35 USC 112(a) |
| 2173 | Claim definiteness (35 USC 112(b)) |

## Prior Art Integration

For full-text search, call `search_patents_google` with named arguments such
as `query`, `country`, `start_year`, `end_year`, and `limit`. If no Google
Patents key is configured or its quota is exhausted, use
`search_patents_bigquery` only with awareness of its scan cost. For CPC
classification, call `search_patents_by_cpc_bigquery` with `cpc_code`,
`limit`, and optional `country`.

**Integrate findings:**
1. Cite in Background section
2. Emphasize distinctions in Summary
3. Explain advantages in Detailed Description
4. Draft claims to avoid/distinguish
5. List in IDS

## Best Practices

**Before Review:**
- Prepare complete application
- Use the `full-review` skill
- Address critical issues first

**During Review:**
- Focus on critical issues (antecedent basis, claim support, definiteness)
- Use MPEP citations
- Iterate until compliant

**After Review:**
- Document compliance
- Final review with the `full-review` skill
- Prepare filing package

## Common Review Findings

**Critical (Must Fix):**
- Missing antecedent basis
- Claim elements unsupported
- Abstract exceeds 150 words
- Indefinite language

**Important (Should Fix):**
- Subjective terms without criteria
- Weak enablement
- Inconsistent terminology

**Minor (Optional):**
- Add example embodiments
- Strengthen best mode
- Improve claim scope

## Quick Reference

### Key Compliance Checks

| Requirement | Citation | Tool |
|-------------|----------|------|
| Antecedent basis | 35 USC 112(b) | review_patent_claims |
| Written description | 35 USC 112(a) | review_specification |
| Enablement | 35 USC 112(a) | review_specification |
| Abstract length | MPEP 608.01(b) | check_formalities |
| Title format | MPEP 606 | check_formalities |
