# Patent-creator Security Policy

This policy applies to
[lesquerr/Patent-creator](https://github.com/lesquerr/Patent-creator), a fork of
[Claude Patent Creator](https://github.com/RobThePCGuy/Claude-Patent-Creator).

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.2.x   | Yes       |
| < 0.2   | No        |

## Reporting a Vulnerability

**Do not open a public issue for security vulnerabilities.**

Use the fork's [GitHub Security page](https://github.com/lesquerr/Patent-creator/security)
to check whether private reporting is enabled. If enabled, use **Report a
vulnerability**. Do not send fork-specific reports to the upstream project
unless the issue also affects upstream.

### Response Timeline

Response times depend on the fork maintainer's availability. The upstream
project's response targets do not constitute a commitment for this fork.

## Security Architecture

### Local-First Design

- Patent data stays on your machine
- No cloud storage of user data
- API keys stored in environment variables (`.env` excluded via `.gitignore`)
- MCP server runs with user-level permissions only

### External API Communication

| API | Data Sent | Purpose |
|-----|-----------|---------|
| BigQuery | Search queries | Patent search (100M+) |
| USPTO API | Search queries | Live patent lookup |
| HuggingFace | Model downloads | Embedding/reranker models (first run only) |

Queries are sent over HTTPS. No patent application content is transmitted to external services.

### What IS a Security Issue

- API key exposure or leakage
- Command injection via MCP tool inputs
- Path traversal in file operations
- Unauthorized file system access
- Dependency vulnerabilities with known exploits

### What is NOT a Security Issue

- Local index files being readable (they're meant to be)
- GPU memory usage or allocation
- Rate limiting on external APIs
- Search result quality or accuracy

## Best Practices for Users

1. Use a virtual environment to isolate dependencies
2. Keep API keys in `.env` (never commit them)
3. Keep dependencies updated (`pip install --upgrade`)
4. Verify package source before installing
