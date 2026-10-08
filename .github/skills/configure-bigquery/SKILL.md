---
name: configure-bigquery
description: "Configure local Google Cloud authentication and a project ID for optional patent searches without exposing credentials."
---

## Copilot MCP tools

Call tools directly through the configured `patent-creator` MCP server. Use `/mcp` to confirm the server and discover its exposed tools, then invoke the displayed registered tool with named arguments from its schema. Do not guess runtime-qualified prefixes or replace tool calls with a Python runner.
# Configure BigQuery

Use this skill to set up optional Google BigQuery access for patent search. BigQuery configuration is not required for local analyzers, law search, or diagram generation. Explain that a Google Cloud project, enabled BigQuery API, ADC authentication, and a project ID may be needed. Never ask the user to paste a credential, token, client secret, or credential file into chat.

## Steps

1. **Check the environment.** Confirm the repository root and the existing `.venv`. Do not install or change dependencies as part of authentication. If dependencies are missing, report that and use the repository's approved environment setup procedure.
2. **Check available Google Cloud tooling.** In PowerShell, run `gcloud --version`. If `gcloud` is unavailable, stop and give the official Google Cloud SDK installation guidance; do not download or install it without permission.
3. **Authenticate locally.** After the user authorizes the browser sign-in, run:

   ```powershell
   gcloud auth application-default login
   ```

   This creates Application Default Credentials in the user's local Google Cloud configuration. Do not open, display, copy, or log the credential file contents.
4. **Set the project ID.** For the current PowerShell session:

   ```powershell
   $env:GOOGLE_CLOUD_PROJECT = "YOUR_PROJECT_ID"
   ```

   Use the user's real project ID only when they provide it. Do not commit it into source code. Do not set a key or secret as a substitute for ADC.
5. **Verify configuration without running a patent query.** Call the zero-argument `check_bigquery_status` MCP tool. This checks readiness; it is not a patent search. Never display authentication tokens or secret values in verification output.
6. **Only test or search after cost approval.** BigQuery scans can incur charges after applicable free quota. Explain the expected scan/cost information available from the tool documentation before running a query, and require explicit user approval for any paid or potentially billable query.

The `check_bigquery_status` MCP tool takes no arguments. Do not call `search_patents_bigquery` as a connectivity test. The repository's optional `scripts\test_bigquery.py` performs search/detail queries; run it only after the user explicitly approves the potential cost.

## Credential handling

Never print, display, share, echo, or commit credentials, secrets, or access tokens. Do not save secrets into skills, logs, command history, or tracked files. Keep Google-managed ADC in its normal user configuration. If authentication fails, report the error without asking the user to reveal credential contents.

**Disclaimer:** This configures optional search access only. It does not guarantee Google Cloud billing eligibility, free quota, dataset permissions, or legal clearance to use search results.
