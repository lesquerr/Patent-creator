---
name: rebuild-index
description: Rebuild the local patent-law search index from already available source documents.
---

# Rebuild the Search Index

Use this skill when the user needs a fresh local hybrid search index after source updates, corruption, or an approved model change. Rebuilding replaces derived index data; explain that first and confirm before starting. It may take several minutes on a GPU and substantially longer on CPU.

## Procedure

1. Confirm the repository root and `.venv` are correct.
2. Check that the law-source documents are already available. Do not start a large download without explicit approval. If sources are missing, ask before using setup, which can download the MPEP and other legal materials.
3. Tell the user that an index rebuild is CPU/GPU intensive and replaces the existing derived index.
4. After approval, rebuild from existing sources:

   ```powershell
   .\.venv\Scripts\python.exe -m mcp_server.cli rebuild-index
   ```

   This CLI command rebuilds the index and exits; it does not start the MCP server. Do not use the MCP server entry point for rebuilding: it starts the stdio process after building and keeps the command attached. If corpus documents are missing, use `setup-patent-system` only after explicit approval for large downloads.
5. Confirm completion from the command's exit status and output. If it fails, report the error; do not call the index healthy based on an assumed fallback.
   Then run the local status check:

   ```powershell
   .\.venv\Scripts\python.exe -m mcp_server.cli health
   ```

6. Restart or reconnect Copilot's `patent-creator` server through `/mcp` so it loads the rebuilt index. Verify availability by reading resource `mpep://index/stats`. A small law search is optional and only if the user wants that additional check. Do not run patent database queries as index verification.

If the documents are absent, do not use a guessed setup flag. Use the setup-patent-system skill only after explicit approval of any required large download.

## Copilot MCP tools

Use `/mcp` to restart or reconnect the configured `patent-creator` server after the rebuild, then read its resource `mpep://index/stats` to verify index status. Do not guess runtime prefixes or use a subprocess runner. Do not install packages or change dependency manifests as part of rebuilding.

## Expected index contents and use

The index supports hybrid legal retrieval over available MPEP, statutes, regulations, and any downloaded EPO/PCT materials. US claims and other US reviews need it to provide MPEP citations. A missing index does not prevent diagram generation or independent analyzers that do not need citations, but do not claim legal references were verified.

**Disclaimer:** An index search is a retrieval aid, not legal advice. Confirm cited legal requirements against official, current sources.
