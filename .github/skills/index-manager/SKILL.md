---
name: index-manager
description: "Manages MPEP index lifecycle including downloads, building, maintenance, and optimization."
---

## Using the connected MCP server

In Copilot, connect to the configured `patent-creator` server with `/mcp` and restart Copilot after configuration changes. Discover the exposed tools and parameter schemas from that server. Invoke tools as attached MCP calls with named arguments matching the discovered schema. Server-qualified aliases vary by runtime, so invoke tools through Copilot's discovered MCP interface rather than hard-coding an alias or treating internal Python classes as exposed tools.
# Index Manager Skill

Expert system for managing MPEP search index lifecycle: PDF downloads, index building, maintenance, updates, optimization.

Use the repository's Windows virtual environment and CLI. Do not invoke
`install.py` or register an MCP server as part of Copilot setup.

## When to Use

Building/rebuilding MPEP index, corruption/missing files, optimization, adding content, troubleshooting.

## Index Lifecycle

```
PDFs Not Present -> Download (2-5 min, 500MB)
  -> Extract & Parse (500MB data)
  -> Generate Embeddings (5-10 min GPU, 35-65 min CPU)
  -> Build FAISS + BM25 Indexes
  -> Index Ready (mcp_server/index/)
  -> Maintenance (Verify -> Optimize -> Update)
```

## Phase 1: PDF Management

**Check Status:**
```powershell
Get-ChildItem .\pdfs
```

**Download PDFs and source documents** only when an index build is requested.
Use the CLI's `download-all` command, which downloads MPEP, statutes,
regulations, subsequent updates, and EPO/PCT sources:
```powershell
& .\.venv\Scripts\python.exe -m mcp_server.cli download-all
```

Do not also run `download-mpep`; it duplicates the MPEP download. The
alternative `setup --non-interactive` command attempts optional Claude MCP
registration. Avoid rebuilding through the server entry point: it proceeds
into its MCP loop after building.

**Verify Integrity:**
```powershell
@'
import fitz
from pathlib import Path
for pdf in Path('pdfs').glob('*.pdf'):
    try:
        doc = fitz.open(pdf)
        print(f'[OK] {pdf.name}: {len(doc)} pages')
        doc.close()
    except Exception as e:
        print(f'[X] {pdf.name}: ERROR - {e}')
'@ | .\.venv\Scripts\python.exe -
```

## Phase 2: Index Building

```powershell
& .\.venv\Scripts\python.exe -m mcp_server.cli rebuild-index
& .\.venv\Scripts\python.exe -m mcp_server.cli health
```

After health reports the index ready, restart Copilot and reconnect the server
with `/mcp`.

**Timeline:**
- Load PDFs: 30s
- Extract text: 1-2 min
- Chunk text (500 tokens): 30s
- Generate embeddings: 5-10 min (GPU) or 35-65 min (CPU)
- Build FAISS/BM25: 1 min
- Save to disk: 10s

**Total:** 5-15 min (GPU) or 35-65 min (CPU)

Use the CLI's supported options for custom builds; do not rely on constructing
an `MPEPIndex` object as a Copilot tool.

## Phase 3: Verification

```powershell
# Check files
Get-ChildItem .\mcp_server\index
# Expected: mpep_index.faiss (~150MB), mpep_metadata.json (~80MB), mpep_bm25.pkl (~60MB)

# Verify health
& .\.venv\Scripts\python.exe -m mcp_server.cli health
# Should show: [OK] MPEP Index: Ready (12,543 chunks)

```

Use `/mcp` to connect Copilot to `patent-creator`, restart Copilot, and discover the exposed tools and schemas. Verify the index by reading the `mpep://index/stats` MCP resource and, when ready, call `search_mpep` with named arguments such as `query` and `top_k`.

## Phase 4: Maintenance

**When to Rebuild:**
- MPEP updates (quarterly check uspto.gov)
- Index corruption
- After adding new PDFs
- Performance degradation
- Machine migration

**Rebuild Process:**
```powershell
# Backup (optional)
$backup = ".\mcp_server\index_backup_{0}" -f (Get-Date -Format yyyyMMdd)
Copy-Item .\mcp_server\index $backup -Recurse

# Rebuild and verify
& .\.venv\Scripts\python.exe -m mcp_server.cli rebuild-index
& .\.venv\Scripts\python.exe -m mcp_server.cli health

# Remove only the backup created above, and only after successful verification
if (Test-Path -LiteralPath $backup) { Remove-Item -LiteralPath $backup -Recurse }
```

## Phase 5: Content Updates

```powershell
# Use the repository's original server flags to acquire updated official sources.
# Do not add a single PDF beside an index built from a different corpus.
& .\.venv\Scripts\python.exe -m mcp_server.cli download-all
& .\.venv\Scripts\python.exe -m mcp_server.cli rebuild-index
& .\.venv\Scripts\python.exe -m mcp_server.cli health
```

**Note:** Incremental updates not supported. Full rebuild required.

## Troubleshooting

- OOM errors during build
- Build taking too long
- Corrupted index files
- Search returning no results

## Performance Tuning

- Embedding generation speed (GPU vs CPU)
- Search latency optimization
- Index size reduction
- Batch size tuning

## Quick Reference

| Command | Purpose |
|---------|---------|
| `& .\.venv\Scripts\python.exe -m mcp_server.cli download-all` | Download all legal sources without starting Claude MCP registration |
| `& .\.venv\Scripts\python.exe -m mcp_server.cli rebuild-index` | Build/rebuild search index |
| `& .\.venv\Scripts\python.exe -m mcp_server.cli health` | Check index health |
| `Get-ChildItem .\mcp_server\index` | View index files |

**Best Practices:**
1. Backup before rebuild
2. Verify PDFs before building
3. Use GPU for 10x faster builds
4. Test after rebuild
5. Keep PDFs until verified
6. Weekly health checks
