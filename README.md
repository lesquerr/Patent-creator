# Patent-creator

**[Patent-creator](https://github.com/lesquerr/Patent-creator) is a fork of
[Claude Patent Creator](https://github.com/RobThePCGuy/Claude-Patent-Creator),
originally developed by RobThePCGuy.** This fork adds GitHub Copilot CLI skills,
agents, and workflow documentation while keeping the original Python MCP
server and Claude integration.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![MCP Server](https://img.shields.io/badge/MCP-Python%20SDK%202.x-purple.svg)](https://github.com/modelcontextprotocol/python-sdk)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.9+-red.svg)](https://pytorch.org/)
[![Status](https://img.shields.io/badge/status-beta%20(WIP)-orange.svg)](#project-status)

**An AI-powered patent creation and analysis system for Claude Code and GitHub Copilot CLI.**

The upstream author created the original system to help prepare their own
patent application and released it as open source. This fork adapts that work
for Copilot CLI. You do not need to be a lawyer or a programmer to begin:
describe your idea in a chat window and use the guided workflows.

In plain terms, this tool lets you:

- **Ask patent-rule questions in plain English.** "Do my claims have to be numbered?" "How long can the abstract be?" You get the actual rule, with a citation, in about a second. (Under the hood it searches the MPEP, the examiner's rulebook, plus the patent statutes and regulations.)
- **Find out whether your idea is actually new.** Search more than 100 million existing patents worldwide for anything close to your invention. This is called a *prior art* search, and it is the single most important step — it is how you learn whether a patent is even worth pursuing.
- **Get your draft checked before a human ever bills you an hour.** The tool reads your claims and application the way an examiner would and flags the mechanical problems: unclear wording, missing sections, an abstract that is too long. It also tells you which checks it *did not* run, so a clean report means what it says.
- **Make the drawings.** Patent-style diagrams and flowcharts from a description, no design software.
- **Go from "here is my idea" to a reviewable draft application.** A guided workflow takes your description (or even your source code), hunts for prior art, drafts claims and a specification, checks everything, and hands you a package a patent professional can review quickly — for US or European filing.

New to the vocabulary? Every term this page uses is explained in the [Glossary](#glossary) in plain English.

---

## What this tool will and will not do — read this first

This tool is built for people who cannot afford a mistake, so it is honest to a fault. Know what you are getting:

- **It will tell you "no."** If the search finds your idea already exists, the tool's job is to show you the evidence and save you the filing fee — not to flatter you into spending money. A well-reasoned "this is not new, and here is why" is the tool working, not failing.
- **It never says "verified" loosely.** Every automated check reports what it ran *and what it skipped*. If a report looks clean, you can trust that the words mean exactly what they say.
- **It does not file anything for you.** You review, you decide, you file. The tool prepares; you commit.
- **It is not a lawyer and does not give legal advice.** What it produces is a well-prepared draft plus organized evidence — built so that a patent professional's review is fast and cheap instead of slow and expensive. For anything you intend to file, have a registered patent practitioner look at it. The point of this tool is to make that look-over affordable, not to skip it.
- **Some judgments are human-only.** Whether your invention is "non-obvious" and whether it is the kind of thing patent law protects at all are legal judgments no software makes reliably. The tool arms you for those conversations; it does not have them for you.

---

## Table of Contents

- [What this tool will and will not do](#what-this-tool-will-and-will-not-do--read-this-first)
- [Patent-creator Quick Start](#patent-creator-quick-start)
- [What Can I Actually Do With This?](#what-can-i-actually-do-with-this)
- [How It Works](#how-it-works)
- [Patent-creator Installation Options](#patent-creator-installation-options)
- [CLI Commands](#cli-commands)
- [MCP Tools Reference](#mcp-tools-reference)
- [Skills, Agents, and Slash Commands](#skills-agents-and-slash-commands)
- [Configuration](#configuration)
- [Requirements](#requirements)
- [Patent-creator Architecture](#patent-creator-architecture)
- [Performance](#performance)
- [Known Issues](#known-issues)
- [Glossary](#glossary)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)

---

## Patent-creator Quick Start

### GitHub Copilot CLI (Windows, Skills and Agents + Existing MCP Server)

Open Copilot CLI in this checkout. The native integration includes the existing
17 patent skills, all 16 command workflows as additional skills, and 13 custom
agents. It connects to the **existing, unchanged MCP server** for search,
analysis, and diagrams. No Claude installation is needed for Copilot.
The original Python code, setup, and Claude integration are preserved.

With Python 3.10+ installed, run these commands from the repository root in
PowerShell. To obtain this fork first:

```powershell
git clone https://github.com/lesquerr/Patent-creator.git
Set-Location Patent-creator
```

If `.venv` and dependencies already exist, skip the first two commands below:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -e ".[dev]"

# If your legal corpus/index is not yet built, use the existing commands.
# Downloads/model loading/index building may take several minutes.
.venv\Scripts\python.exe -m mcp_server.cli download-all
.venv\Scripts\python.exe -m mcp_server.cli rebuild-index
.venv\Scripts\python.exe -m mcp_server.cli health

copilot
```

The workspace `.mcp.json` registers `patent-creator` using the local `.venv`
interpreter and the original `mcp_server\server.py`. Start Copilot from the
repository root; open `/mcp` to inspect connection status and available tools.
If Copilot was already running when the configuration changed, restart it.
The server requires source PDFs or a built index before it can start.

In Copilot, enter `/skills reload`, then prompt:

```text
Use the create-patent skill to draft an application for my invention.
Use the full-review skill to review this application.
Use the search-prior-art skill to research my invention.
```

Select a specialist using `/agent`, for example `/agent patent-creator`.
These are native **skills**, not Claude-style registered slash commands.
Their files live in `.github\skills`; agent profiles are in `.github\agents`.
To use them from another project, launch Copilot with
`--add-dir "C:\path\to\Patent-creator"` and register the server in user
scope with absolute paths (replace these example paths with your checkout):

```powershell
copilot mcp add patent-creator -- "C:\path\to\Patent-creator\.venv\Scripts\python.exe" "C:\path\to\Patent-creator\mcp_server\server.py"
```

Search credentials are inherited from environment variables:
`GOOGLE_CLOUD_PROJECT` and optionally `GOOGLE_APPLICATION_CREDENTIALS` for
BigQuery, `SERPAPI_API_KEY` for Google Patents, and `EPO_OPS_KEY` /
`EPO_OPS_SECRET` for EPO OPS. The existing ignored `.env` file also works;
real environment variables take precedence. Do not paste keys into chat.
No Anthropic API key is needed with default HyDE off. Restart Copilot after
changing its inherited environment.

Copilot calls all 34 existing MCP tools (including async EPO operations) and
can access the index-statistics resource. Use `/mcp` to inspect their actual
input schemas; skills supply workflow guidance rather than replacing tools.
Law search and citation-enriched US/EPO/PCT reviews require a built index;
provider searches require credentials, and diagram rendering requires
system Graphviz. Missing prerequisites are reported as errors, not successful
checks. The existing `setup --non-interactive` command is still available
for GPU provisioning and automated setup, but retains its original Claude
registration attempt; Copilot configuration is independent.
See [Copilot instructions](.github/copilot-instructions.md).

### Claude Code

Never used Claude Code? It's Anthropic's AI assistant that runs in a terminal or as a desktop app — [install it first](https://claude.com/claude-code) (a paid Claude subscription is the only cost to start). Then come back here; setup is one command and the tool talks you through the rest.

Pick the path that fits your setup. All three get you to the same place.

### Option A: Claude Code Plugin (Easiest)

For the original Claude Code plugin, use the **upstream marketplace** below.
This installs upstream's plugin, not the Copilot-adapted fork. To use
Patent-creator's source code, use the fork installation options that follow.

```bash
# Add the marketplace and install
/plugin marketplace add RobThePCGuy/Claude-Patent-Creator
/plugin install claude-patent-creator-standalone@claude-patent-creator

# Run setup
/claude-patent-creator-standalone:setup-patent-system
```

### Option B: One-Line Install

```bash
pip install git+https://github.com/lesquerr/Patent-creator.git && patent-creator setup
```

This handles everything automatically: installs dependencies, detects your GPU, downloads MPEP PDFs (~500MB), builds the search index, and registers the MCP server with Claude Code. Restart Claude Code when it finishes.

### Option C: Manual Install

```bash
git clone https://github.com/lesquerr/Patent-creator.git
cd Patent-creator
# Optional: use a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -e .
patent-creator setup
```

### Verify It Worked

After any install path, run:

```bash
patent-creator health
```

You should see a status report showing which components are ready. If something's off, the output will tell you what to fix.

---

## What Can I Actually Do With This?

Here are some real examples. You can type these directly in Claude Code and the right skill or tool kicks in automatically. Say it in your own words — the "what to say" column is a starting point, not a required incantation.

| What you want to do | What to say | What happens |
|---|---|---|
| Find out if a rule applies to you | "Search MPEP for claim definiteness requirements" — or just "do my claims have to be written a certain way?" | The tool searches the examiner's rulebook and returns the relevant sections, with citations you can read yourself |
| See if your idea already exists | "Search for patents about [your idea]" — e.g. "self-heating coffee mug" | Searches 100M+ existing patents and shows you the closest matches, so you know what you're up against |
| Get your draft claims checked | "Review these claims" (paste them in) | Flags unclear wording, terms used before they're introduced, and structural problems — the mechanical mistakes an examiner rejects first |
| Check a whole application | `/full-review` | Runs the claims, description, and formatting checks together and reports everything at once |
| Go from idea to draft application | `/create-patent` | A guided workflow: describe the invention, the tool searches prior art, drafts, checks, and assembles a reviewable package (typically about an hour) |
| Make a drawing | "Create a block diagram showing [your system]" | Produces a patent-style figure, no design software needed |
| Dig deep on whether your idea is new | "Conduct a prior art search for [your invention]" | A thorough multi-angle hunt through existing patents, with an honest verdict on what it found |

---

## How It Works

*Everything from here down gets progressively more technical. You do not need any of it to use the tool — the sections above plus the [Glossary](#glossary) are enough. This part is for developers, patent professionals, and the curious.*

The system has three integrations that reuse the same Python engine:

**MCP Server** is the engine. It exposes 20+ tools that any MCP-compatible client (Claude Code, Claude Desktop, etc.) can call programmatically. These tools handle search, analysis, and diagram generation.

**Claude Code Plugin** adds the interactive layer. Skills activate automatically based on what you're doing. Agents handle long-running tasks in the background. Slash commands give you quick access to common workflows.

**Copilot CLI Native Integration** uses repository skills and custom agents.
The former Claude command workflows become named skills; the tools continue
to run through the existing MCP server configured in `.mcp.json`.

Under the hood, patent regulation search uses a hybrid approach: FAISS vector search finds semantically similar content, BM25 lexical search catches exact terminology matches, and a cross-encoder reranker sorts the combined results by relevance. Patent search goes through Google BigQuery's public patent dataset.

```
You (Claude Code) ──> MCP Server ──> Search / Analysis / Diagrams
                           │
            ┌──────────────┼──────────────┐
            v              v              v
     MPEP/USC/CFR     BigQuery        Graphviz
     (hybrid RAG)    (100M+ patents)   (diagrams)
```

---

## Patent-creator Installation Options

<details>
<summary><strong>What the setup wizard does (step by step)</strong></summary>

1. Installs Python package dependencies
2. Detects your hardware (NVIDIA GPU, Apple Silicon, or CPU-only)
3. If a GPU is detected, uninstalls CPU-only PyTorch and installs the GPU version
4. Restarts the setup process with GPU-enabled PyTorch
5. Downloads MPEP, 35 USC, and 37 CFR PDFs (~500MB) from the USPTO
6. Builds the hybrid search index (FAISS + BM25) with GPU acceleration if available
7. Registers the MCP server with Claude Code

</details>

<details>
<summary><strong>Using a virtual environment (recommended for isolation)</strong></summary>

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install git+https://github.com/lesquerr/Patent-creator.git && patent-creator setup
```

If you go this route, remember to activate the venv before running any manual commands. Claude Code handles activation automatically.

</details>

<details>
<summary><strong>Loading as a local plugin (for development)</strong></summary>

```bash
claude --plugin-dir ./Patent-creator
```

This loads the plugin directly from your local checkout without installing from the marketplace.

</details>

---

## CLI Commands

```bash
patent-creator setup             # Full setup wizard (downloads, builds index, registers MCP)
patent-creator health            # System health check (shows what's working and what isn't)
patent-creator status            # Same as health
patent-creator verify-config     # Check Claude Code MCP configuration
patent-creator serve             # Run the MCP server manually
patent-creator rebuild-index     # Rebuild the MPEP search index
patent-creator download-mpep     # Download MPEP PDFs only
patent-creator download-all      # Download all sources (MPEP + 35 USC + 37 CFR)
patent-creator check-bigquery    # Test BigQuery connection
```

---

## MCP Tools Reference

### Search

| Tool | What it does |
|---|---|
| `search_mpep` | Hybrid RAG search across MPEP, 35 USC, and 37 CFR with filters |
| `get_mpep_section` | Pull full content of a specific MPEP section |
| `search_patents_google` | Full-text keyword search worldwide, claims included (recommended; free SerpApi key, 250 searches/month) |
| `search_patents_bigquery` | Keyword search fallback when no SerpApi key is set (~$2 a search past the free monthly TiB) |
| `get_patent_bigquery` | Get details on a specific patent (claims by default; abstract/description opt-in) |
| `get_patents_bigquery` | Get details on up to 50 patents in one query, same cost as one |
| `search_patents_by_cpc_bigquery` | Search by CPC classification code |
| `search_uspto_api` | Search via the USPTO API |
| `get_uspto_patent` | Get patent details from USPTO |
| `get_recent_uspto_patents` | Pull recent filings |

### Getting the campaign workflow (skills)

The MCP server above gives Claude the TOOLS. The campaign workflow — the
skill that runs mining, prior art, worth-it economics, drafting, and the
red teams end to end — ships as a Claude Code plugin. Two commands:

```bash
claude plugin marketplace add RobThePCGuy/Claude-Patent-Creator
claude plugin install claude-patent-creator-standalone@claude-patent-creator
```

These commands install the upstream Claude plugin. Re-run the install command
after upstream upgrades to refresh it. In this fork, Copilot loads the
repository workflows from `.github\skills` instead.

### Analysis

| Tool | What it does |
|---|---|
| `review_patent_claims` | 35 USC 112(b) compliance check (definiteness, antecedent basis, structure) |
| `review_specification` | 35 USC 112(a) adequacy check (written description, enablement, best mode) |
| `check_formalities` | MPEP 608 compliance (abstract, title, drawings, required sections) |
| `check_package` | Whole-package consistency: stale verification stamps, claim-count disagreements, status contradictions, commentary inside filing copies, date errors |

### Generation

| Tool | What it does |
|---|---|
| `render_diagram` | Generate patent-style diagrams from Graphviz DOT code |
| `create_flowchart` | Build a flowchart from a list of steps and connections |
| `create_block_diagram` | Build a block diagram from components and relationships |
| `add_diagram_references` | Add patent reference numbers to an existing SVG diagram |
| `get_diagram_templates` | List available diagram templates |

### System

| Tool | What it does |
|---|---|
| `get_index_stats` | Search index statistics |
| `check_bigquery_status` | BigQuery configuration status |
| `check_diagram_tools_status` | Graphviz availability |
| `check_uspto_api_status` | USPTO API connectivity |
| `get_patent_details` | Combined patent retrieval across sources |

---

## Skills, Agents, and Slash Commands

### Skills (activate automatically)

You don't need to call these directly. Just describe what you want to do and the right skill kicks in.

| Skill | When it activates | What it brings |
|---|---|---|
| **setup-assistant** | Installing, configuring, or troubleshooting | Full setup lifecycle guidance |
| **patent-reviewer** | Reviewing a complete application for compliance | Comprehensive review (claims + spec + formalities) |
| **patent-claims-analyzer** | Reviewing claims specifically for 35 USC 112(b) | Deep-dive claims analysis (definiteness, antecedent basis, structure) |
| **patent-search** | Searching patents or prior art | BigQuery search workflows via the MCP tools |
| **bigquery-patent-search** | Quick BigQuery-only patent search | Keyword, CPC, and patent detail retrieval across 100M+ patents |
| **mpep-search** | Finding MPEP sections or regulations | Hybrid RAG search |
| **patent-diagram-generator** | Creating technical diagrams | Flowcharts, block diagrams, system architectures via Graphviz |
| **patent-application-creator** | Drafting a patent application interactively | Guided end-to-end workflow (prior art, claims, spec, diagrams, compliance) |
| **prior-art-search** | Novelty or freedom-to-operate analysis | 7-step prior art discovery methodology |
| **index-manager** | Building or rebuilding the search index | MPEP index lifecycle management |
| **development-assistant** | Adding features or creating tools | Development workflows and patterns |
| **troubleshooting-assistant** | Something's broken | Systematic 6-step diagnostics |
| **testing-assistant** | Running tests or validation | Test suite execution |

### Agents (long-running, work independently)

These run in the background while you keep working on other things.

| Agent | What it does | How long | Output |
|---|---|---|---|
| **patent-creator** | Drafts a complete USPTO-ready application | 55-80 min | Specification, claims, abstract, diagrams, validation report |
| **prior-art-searcher** | Comprehensive prior art search | 15-30 min | Patentability report, top 10 prior art, claim strategy, IDS list |

To use them: "Create a patent for [your invention], use the patent-creator agent"

### Slash Commands

```
/create-patent          # Complete patent creation workflow (55-80 min)
/search-prior-art       # Prior art search with novelty analysis
/full-review            # Parallel review (claims + spec + formalities)
/review-claims          # Claims-only 35 USC 112(b) analysis
/review-specification   # Specification-only 35 USC 112(a) analysis
/review-formalities     # MPEP 608 formalities check
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root (see `.env.example`):

```bash
# Required for BigQuery patent search
GOOGLE_CLOUD_PROJECT=your-project-id

# Optional: EPO OPS API (for EP patent full-text search)
# Free registration at https://developers.epo.org
EPO_OPS_KEY=your-consumer-key
EPO_OPS_SECRET=your-consumer-secret

# Optional API keys (for HyDE query expansion)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Optional settings
PATENT_LOG_LEVEL=INFO
PATENT_LOG_FORMAT=human
PATENT_ENABLE_METRICS=true
PATENT_MPEP_USE_HYDE=false
PATENT_MPEP_DEVICE=gpu
PATENT_OPERATION_TIMEOUT=300
```

<details>
<summary><strong>Setting up BigQuery (optional, for patent search)</strong></summary>

BigQuery gives you access to 100M+ worldwide patents. It requires a Google Cloud project with billing enabled (the public patent dataset itself is free to query within BigQuery's free tier).

```bash
# 1. Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# 2. Authenticate
gcloud auth application-default login

# 3. Set quota project (replace with your project ID)
gcloud auth application-default set-quota-project your-project-id

# 4. Set the environment variable
export GOOGLE_CLOUD_PROJECT="your-project-id"   # Linux/macOS
$env:GOOGLE_CLOUD_PROJECT="your-project-id"     # Windows PowerShell

# 5. Test it
patent-creator check-bigquery
```

</details>

<details>
<summary><strong>Windows-specific setup notes</strong></summary>

**Git Bash is required** for the `claude mcp add` command on Windows. Install [Git for Windows](https://git-scm.com/download/win) and set the path:

```bash
# In your .env file
CLAUDE_CODE_GIT_BASH_PATH=C:\Program Files\Git\bin\bash.exe
```

**Use forward slashes in MCP config paths.** The setup wizard handles this, but if you're configuring manually:

```bash
# Correct
claude mcp add ... -- "C:/Users/YourName/venv/Scripts/python.exe"

# Wrong (will fail)
claude mcp add ... -- "C:\Users\YourName\venv\Scripts\python.exe"
```

</details>

---

## Requirements

### Minimum

- **Python:** 3.9 - 3.13 (3.14 is experimental)
- **RAM:** 8GB
- **Disk:** ~2GB (MPEP PDFs + search index)

### Optional (but recommended)

- **GPU:** NVIDIA with CUDA 12.8 (makes indexing 5-10x faster) or Apple Silicon (2-3x faster)
- **Google Cloud:** Project with BigQuery enabled (for patent search)
- **Graphviz:** System package (for diagram generation)

<details>
<summary><strong>Full dependency list</strong></summary>

| Package | Version | Purpose |
|---|---|---|
| mcp | >=2.0.0, <3.0.0 | MCP Python SDK (MCPServer) |
| sentence-transformers | >=5.1.2, <7.0.0 | Text embeddings |
| faiss-cpu | >=1.13.2 | Vector similarity search |
| numpy | >=1.26.0, <3.0.0 | Array operations |
| rank-bm25 | >=0.2.2 | Lexical search |
| transformers | >=4.57.6, <6.0.0 | HuggingFace models |
| google-cloud-bigquery | >=3.41.0 | Patent search |
| pydantic | >=2.12.5 | Data validation |
| graphviz | >=0.21 | Diagram generation |
| PyMuPDF | >=1.26.0 | PDF processing |

See `pyproject.toml` for the complete list.

</details>

---

## Patent-creator Architecture

```
Patent-creator/
├── .github/
│   ├── skills/              # Copilot skills and command workflows (33)
│   ├── agents/              # Copilot custom agents (13)
│   └── copilot-instructions.md  # Fork-specific Copilot guidance
├── .mcp.json                # Copilot connection to the existing MCP server
├── .claude-plugin/          # Plugin manifest and marketplace config
├── mcp_server/              # Core MCP server
│   ├── server.py            # MCPServer entry point
│   ├── mpep_search.py       # Hybrid RAG search engine
│   ├── bigquery_search.py   # BigQuery patent search
│   ├── claims_analyzer.py   # 35 USC 112(b) analyzer
│   ├── specification_analyzer.py  # 112(a) analyzer
│   ├── formalities_checker.py     # MPEP 608 checker
│   ├── diagram_generator.py       # Graphviz diagrams
│   ├── tools/               # MCP tool definitions
│   └── index/               # FAISS + BM25 index (git-ignored)
├── skills/                  # Claude Code skills (13)
├── agents/                  # Autonomous agents (10)
├── commands/                # Slash commands (11)
├── hooks/                   # Event-driven automation
├── scripts/                 # Testing and utilities
├── docs/                    # Additional documentation
├── pdfs/                    # Downloaded MPEP PDFs (git-ignored)
└── CLAUDE.md                # Full project documentation
```

For the complete architecture documentation, development workflows, and troubleshooting guides, see [CLAUDE.md](CLAUDE.md).

The repository is named `Patent-creator`; the Python distribution
`claude-patent-creator`, CLI command `patent-creator`, MCP server identity,
data-directory names, and Claude plugin identifiers retain their upstream
names for compatibility. Documentation filenames such as `README.md` and
`CLAUDE.md` remain unchanged so GitHub and assistant discovery keep working.

---

## Performance

| Operation | Time | Notes |
|---|---|---|
| **MPEP Search** | 50-200ms | Hybrid FAISS + BM25 |
| **BigQuery Patent Search** | 1-3 sec | 100M+ patents |
| **USPTO API** | 500ms - 2s | Rate-limited by USPTO |
| **Index Build (GPU)** | 3-5 min | NVIDIA CUDA 12.8 |
| **Index Build (Apple Silicon)** | 8-12 min | MPS acceleration |
| **Index Build (CPU)** | 25-35 min | No GPU |

Resource usage: the loaded search index takes about 2-4GB of RAM and the index files are 500MB-1GB on disk. If you have a GPU, it'll use 1-2GB of VRAM for acceleration.

---

## Known Issues

> **This project is a work in progress.** Most features work, but expect some rough edges. Contributions, issues, and PRs are welcome.

Things to be aware of:

- **PyTorch install order matters.** Install PyTorch before `sentence-transformers`, or you'll end up with CPU-only PyTorch even on a GPU system. The setup wizard handles this, but it can bite you on manual installs.
- **BigQuery requires a Google Cloud project** with billing enabled. The patent data itself is free to query within the BigQuery free tier.
- **Some diagram types need Graphviz installed** as a system package (not just the Python bindings).
- **HyDE query expansion requires API keys** (Anthropic or OpenAI). It's optional and off by default.
- **Windows users need Git Bash** for the `claude mcp add` command. See [Windows setup notes](#configuration).

See [CLAUDE.md](CLAUDE.md) for the full troubleshooting guide.

---

## Glossary

If you're coming from the development side and patent terminology is new (or vice versa), here's a quick reference:

| Term | What it means |
|---|---|
| **MPEP** | Manual of Patent Examining Procedure. The handbook patent examiners use at the USPTO. Think of it as the rulebook. |
| **35 USC** | Title 35 of the United States Code. The federal patent statutes. |
| **37 CFR** | Title 37 of the Code of Federal Regulations. The rules that implement the patent statutes. |
| **USPTO** | United States Patent and Trademark Office. The agency that grants patents. |
| **CPC** | Cooperative Patent Classification. A system for categorizing patents by technology area. |
| **Prior Art** | Anything publicly available before your filing date that's relevant to your invention. Finding it is how you figure out if your idea is actually new. |
| **112(a)** | The section of patent law requiring your application to fully describe and enable the invention. |
| **112(b)** | The section requiring your claims to be definite and clear. |
| **MPEP 608** | The section covering formalities like abstract length, title format, and drawing requirements. |
| **RAG** | Retrieval Augmented Generation. Instead of relying only on what the AI was trained on, it searches a database first and uses those results to give a better answer. |
| **FAISS** | Facebook AI Similarity Search. A fast way to find similar text by comparing mathematical representations of meaning. |
| **BM25** | A text search algorithm that matches exact words and phrases. Works alongside FAISS to catch things vector search might miss. |
| **MCP** | Model Context Protocol. A standard for connecting AI tools to AI models. It's how this system talks to Claude. |
| **IDS** | Information Disclosure Statement. A form listing prior art references you need to disclose to the USPTO. |

---

## Roadmap

- [x] Support for international patent offices (EPO, WIPO/PCT)
- [ ] Web interface for non-Claude Code users
- [ ] Claim dependency graph visualization
- [ ] Automated obviousness analysis (35 USC 103)
- [ ] Patent portfolio analysis tools
- [ ] Integration with patent drafting software

---

## Contributing

This project is open to contributions. Since it's a work in progress, expect breaking changes and incomplete documentation. Issues and PRs are welcome.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development setup, branch naming, commit conventions, and code style guide.

---

## Credits

### Upstream Project

Patent-creator is maintained as a fork at
[lesquerr/Patent-creator](https://github.com/lesquerr/Patent-creator).
The original project is
[RobThePCGuy/Claude-Patent-Creator](https://github.com/RobThePCGuy/Claude-Patent-Creator).
Credit for the original patent workflows, Python MCP server, and Claude
integration belongs to the upstream author and contributors. Original license
and copyright notices are retained. `CHANGELOG.md` preserves upstream history;
the fork's Copilot integration is described in this README and
[Copilot instructions](.github/copilot-instructions.md).

### Open Source Dependencies

This project builds on excellent open source work: [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk), [FAISS](https://github.com/facebookresearch/faiss) (Meta AI Research), [Sentence Transformers](https://www.sbert.net/) (UKP Lab), [HuggingFace Transformers](https://huggingface.co/transformers/), [PyTorch](https://pytorch.org/), [rank-bm25](https://github.com/dorianbrown/rank-bm25), [PyMuPDF](https://pymupdf.readthedocs.io/), [Graphviz](https://graphviz.org/), [Pydantic](https://docs.pydantic.dev/), and [Google Cloud BigQuery](https://cloud.google.com/bigquery).

### Data Sources

MPEP, 35 USC, and 37 CFR are published by the USPTO. Patent data comes from Google BigQuery's `patents-public-data` dataset (100M+ patents). Embedding models are [BGE-base-en-v1.5](https://huggingface.co/BAAI/bge-base-en-v1.5) (BAAI) and [MS-MARCO MiniLM-L-6-v2](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2) (Microsoft).

### Trademark Notice

"USPTO" is a registered trademark of the United States Patent and Trademark Office. This project isn't affiliated with, endorsed by, or sponsored by the USPTO.

---

## Project Status

Patent-creator is in **beta**. Some features may not work as described.
Report fork-specific issues in
[lesquerr/Patent-creator](https://github.com/lesquerr/Patent-creator/issues).
For upstream behavior and history, consult the
[original repository](https://github.com/RobThePCGuy/Claude-Patent-Creator).

For detailed documentation: [CLAUDE.md](CLAUDE.md) | For security issues: [SECURITY.md](SECURITY.md)

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

**Originally built with Claude Code; adapted for GitHub Copilot CLI in this
fork.** See the upstream attribution above.
