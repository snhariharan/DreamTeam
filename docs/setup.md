# Setup Guide

Complete installation and environment setup for DreamTeam.

---

## Prerequisites

| Requirement | Minimum version | Notes |
|---|---|---|
| Python | 3.11 | 3.12 recommended |
| pip | 23+ | bundled with Python |
| Node.js | 18 LTS | **optional** — only for MCP servers |

---

## Step 1 — Clone the repository

```bash
git clone <your-repo-url>
cd DreamTeam
```

---

## Step 2 — Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# .\venv\Scripts\activate       # Windows PowerShell
```

---

## Step 3 — Install Python dependencies

```bash
pip install -r requirements.txt
```

This installs:

| Package | Purpose |
|---|---|
| `crewai` | Multi-agent orchestration framework |
| `crewai-tools` | Built-in tools (file, search, scrape, docs) |
| `langchain-openai` | GPT-4o / GPT-4o-mini / o-series models |
| `langchain-anthropic` | Claude Opus / Sonnet / Haiku models |
| `langchain-google-genai` | Gemini 1.5 Pro / Flash models |
| `mcp` | Model Context Protocol Python SDK |

> **Ollama (LOCAL profiles — no API keys needed)**
> If you plan to run entirely locally, also install:
> ```bash
> pip install langchain-ollama
> ollama pull qwen2.5-coder:14b   # developer (best local code model)
> ollama pull llama3.1:8b         # manager + reviewer
> ollama pull mistral:7b          # architect
> ollama pull phi3:medium         # tester + devops
> ```
> Three hardware tiers: `LOCAL_FAST` (8 GB RAM), `LOCAL_BALANCED` (16 GB), `LOCAL_QUALITY` (32 GB+).
> See **[local_models.md](local_models.md)** for the complete Ollama guide.

---

## Step 4 — Set environment variables

### Required — at least one AI provider

Set the API key(s) for the models you plan to use.
You do **not** need all three — only the ones that match your chosen profile.

```bash
# OpenAI — GPT-4o, GPT-4o-mini, o3-mini
export OPENAI_API_KEY=sk-proj-...

# Anthropic — Claude Opus, Sonnet, Haiku
export ANTHROPIC_API_KEY=sk-ant-...

# Google AI — Gemini 1.5 Pro, Flash
export GOOGLE_API_KEY=AIza...
```

### Optional — web search

```bash
# Serper (Google-powered) — free 2,500 searches/month
# Sign up at https://serper.dev
export SERPER_API_KEY=...
```

### Optional — MCP servers

```bash
# GitHub MCP — repository operations, code search, PR diffs
# Create a token at https://github.com/settings/tokens (select: repo, read:user)
export GITHUB_TOKEN=ghp_...

# Brave Search MCP — privacy-first web search
# Sign up at https://brave.com/search/api/  (free tier: 2,000 queries/month)
export BRAVE_API_KEY=BSA...
```

### Making variables permanent

**macOS / Linux — add to shell profile:**
```bash
echo 'export OPENAI_API_KEY=sk-proj-...' >> ~/.zshrc   # zsh
echo 'export OPENAI_API_KEY=sk-proj-...' >> ~/.bashrc  # bash
source ~/.zshrc
```

**Using a `.env` file (recommended for development):**
```bash
# Create .env at project root
cat > .env << 'EOF'
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
SERPER_API_KEY=...
GITHUB_TOKEN=ghp_...
BRAVE_API_KEY=BSA...
EOF

# Load before running
source .env && python agency.py
```

> ⚠️ Add `.env` to `.gitignore` — never commit API keys.

---

## Step 5 — Install MCP server runtime (optional)

MCP servers run as Node.js subprocesses and are installed automatically on first use via `npx -y`.
All you need is Node.js ≥ 18:

```bash
# Check if Node.js is installed
node --version   # should print v18.x.x or higher

# Install Node.js if missing
# macOS with Homebrew:
brew install node

# macOS with nvm:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install 18 && nvm use 18
```

The first run will download the MCP server packages (~10 MB total). Subsequent runs use the npm cache.

---

## Step 6 — Configure your team

Open `agency.py` and edit the two configuration sections at the top:

```python
# Section 1: pick a model profile
from config.profiles import BALANCED
PROFILE = BALANCED

# Section 2: assign skill packs
from skills.packs import PYTHON, CLOUD_AWS, DATABASE, SECURITY, TESTING, API

SKILL_ASSIGNMENTS = {
    "architect": [CLOUD_AWS, API],
    "developer": [PYTHON, DATABASE],
    "reviewer":  [SECURITY],
    "tester":    [TESTING, PYTHON],
    "devops":    [CLOUD_AWS],
}
```

See [configuration.md](configuration.md) for all available options.

---

## Step 7 — Write your task list

Edit `project_tasks.md` (created automatically on first run if absent):

```markdown
Task 1: Add a /health endpoint that returns {"status": "ok", "version": "1.0"}.
Task 2: Add structured request logging middleware (method, path, duration, status).
Task 3: Add JWT authentication to all /api/* routes.
```

Be specific — the more detail you provide, the better the Architect's plan.

---

## Step 8 — Run

```bash
source venv/bin/activate
python agency.py
```

### What you'll see

```
🚀  Booting up DreamTeam Multi-Model AI Agency...

🔌 Connecting to MCP servers...
  ✅  GitHub MCP      : 26 tool(s) loaded
  ✅  Brave Search MCP: 2 tool(s) loaded
  ⚠️   Filesystem MCP  : skipped — ...
🔌 MCP ready — 56 tool slot(s) distributed across roles

🤖  Profile : BALANCED — Strong quality / cost / speed balance.
    architect  skill packs: cloud_aws, api
    developer  skill packs: python, database
    reviewer   skill packs: security
    tester     skill packs: testing, python
    devops     skill packs: cloud_aws
```

---

## Output files

After a successful run, the following files are written to your project:

| File | Written by | Contents |
|---|---|---|
| `src/` | Developer | All new/modified source files |
| `src/tests/` | Tester | PyTest suite |
| `review_report.md` | Reviewer | PASS/FAIL verdict + findings |
| `Dockerfile` | DevOps | Multi-stage production image |
| `docker-compose.yml` | DevOps | Local development stack |
| `.github/workflows/deploy.yml` | DevOps | CI/CD pipeline |

---

## Troubleshooting

### `ValidationError: API key required`
You are importing a module that tries to build an LLM instance at load time.
All LLMs in DreamTeam are lazy (constructed only when `agency.py` runs), but if you
run a script that imports `config.settings` and calls a getter without a key set,
you will see this error. Set the relevant `*_API_KEY` env var.

### `ImportError: cannot import name 'CodeInterpreterTool'`
This tool is not available in the current `crewai-tools` release. It has been
replaced by a graceful placeholder in `skills/code_execution.py`. No action needed.

### MCP servers not connecting
- Confirm Node.js ≥ 18 is installed: `node --version`
- Confirm the relevant API key is set (GitHub / Brave)
- The agency still runs without MCP — servers are skipped gracefully with a ⚠️ warning

### Rate limits / quota errors
Use the `FAST` or `BUDGET` profile to reduce API calls, or add delays via
CrewAI's `max_rpm` parameter in the `Crew()` constructor:
```python
agency = Crew(..., max_rpm=10)
```
