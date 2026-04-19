# DreamTeam 🤖

**A multi-model AI software agency** — an autonomous crew of specialised agents that plans, codes, reviews, tests, and deploys your features end-to-end.

Each agent runs a different frontier LLM, carries a curated set of tools (skills), and can be extended with domain-specific **skill packs** (Python, Java, AWS, Security, etc.) and real external tool servers via the **Model Context Protocol (MCP)**.

---

## What it does

You drop a task list into `project_tasks.md`, run `python agency.py`, and the crew does the rest:

```
📋 project_tasks.md
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│  🧠  Crew Manager  (claude-3-5-sonnet by default)           │
│                                                             │
│  • Reads the task list and all agent outputs                │
│  • Delegates each task to the right specialist              │
│  • Evaluates results — sends back if incomplete or wrong    │
│  • Re-assigns between agents when one gets stuck            │
│  • Synthesises the final deliverable                        │
│                                                             │
│  ⚡ No tools — pure reasoning and orchestration only        │
└──────────────────────────┬──────────────────────────────────┘
                           │  delegates & evaluates
          ┌────────────────┼─────────────────┐
          │                │                 │
          ▼                ▼                 ▼
   ┌──────────────┐  ┌───────────────┐  ┌──────────────┐
   │ 🏛️ Architect  │  │ 💻 Developer  │  │ 🔍 Reviewer  │
   │              │  │               │  │              │
   │ Reads code   │  │ Implements    │  │ Checks code  │
   │ + docs →     │  │ plan →        │  │ → PASS/FAIL  │
   │ impl. plan   │  │ src/ files    │  │ report.md    │
   └──────────────┘  └───────────────┘  └──────────────┘

   ┌──────────────┐  ┌─────────────────────────────────┐
   │ 🧪 Tester    │  │ 🚀 DevOps                       │
   │              │  │                                 │
   │ Writes pytest│  │ Writes Dockerfile +             │
   │ suite →      │  │ docker-compose +                │
   │ tests/ dir   │  │ CI/CD pipeline YAML             │
   └──────────────┘  └─────────────────────────────────┘
```

Each agent runs a **different LLM** chosen for that role's strengths, extended
with domain **skill packs** (Python, AWS, Security, etc.) and live external tools
via **MCP servers** (GitHub, Brave Search, Filesystem).

See **[docs/agents.md](docs/agents.md)** for full role details including the Manager.


---

## Quick start

```bash
# 1. Clone and enter
git clone <your-repo-url>
cd DreamTeam

# 2. Create virtual environment
python3 -m venv venv && source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set API keys (minimum: one provider)
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
export GOOGLE_API_KEY=AIza...

# 5. Configure your team (optional — defaults are ready to use)
#    Edit agency.py: pick a PROFILE and set SKILL_ASSIGNMENTS

# 6. Write your tasks
echo "Task 1: Add a /health endpoint." > project_tasks.md

# 7. Run
python agency.py
```

See **[docs/setup.md](docs/setup.md)** for the full installation guide.

---

## Running with local models (no API keys)

Run the entire agency on your own hardware using [Ollama](https://ollama.com).
No API keys, no cloud costs, full data privacy.

```bash
# 1. Install Ollama
brew install ollama   # macOS, or visit https://ollama.com/download

# 2. Install the Python integration
pip install langchain-ollama

# 3. Pull models (example: 16 GB RAM laptop setup)
ollama pull llama3.1:8b          # manager + reviewer
ollama pull mistral:7b           # architect
ollama pull qwen2.5-coder:14b    # developer  ← best local code model
ollama pull phi3:medium          # tester + devops

# 4. Start Ollama
ollama serve &

# 5. Set the profile in agency.py
#    from config.profiles import LOCAL   ← one-line change

# 6. Run
python agency.py
```

Three hardware tiers available: `LOCAL_FAST` (8 GB), `LOCAL_BALANCED` (16 GB), `LOCAL_QUALITY` (32 GB+).

Full guide: **[docs/local_models.md](docs/local_models.md)**

---

## Project structure

```
DreamTeam/
├── agency.py                    ← Entry point — configure & run here
├── requirements.txt
│
├── config/
│   ├── settings.py              ← API keys + universal get_llm() factory
│   └── profiles.py              ← Model presets (POWER / BALANCED / FAST / BUDGET / LOCAL)
│
├── agents/                      ← Agent factory functions
│   ├── architect.py             Solution Architect
│   ├── developer.py             Senior Software Engineer
│   ├── reviewer.py              Principal Code Reviewer
│   ├── tester.py                QA Automation Engineer
│   └── devops.py                Cloud DevOps Specialist
│
├── tasks/                       ← Task factory functions
│   ├── analysis.py              Architecture / implementation plan
│   ├── coding.py                Code implementation
│   ├── review.py                Code review → review_report.md
│   ├── testing.py               Test suite generation
│   └── deployment.py            Dockerfile + CI/CD pipeline
│
├── skills/                      ← crewai_tools tool instances (lazy)
│   ├── filesystem.py            FileRead, FileWriter, DirectoryRead
│   ├── web_research.py          Serper search, WebScrape, GitHub search
│   ├── config_parsing.py        JSON, TXT, XML search
│   ├── docs_search.py           CodeDocs, MDX search
│   └── packs/                   ← Domain skill packs
│       ├── python_pack.py       PYTHON
│       ├── java_pack.py         JAVA, KOTLIN
│       ├── cloud_pack.py        CLOUD_AWS, CLOUD_GCP, CLOUD_AZURE
│       ├── database_pack.py     DATABASE, NOSQL
│       ├── security_pack.py     SECURITY
│       ├── api_pack.py          API, GRAPHQL
│       ├── testing_pack.py      TESTING
│       └── language_pack.py     NODEJS, TYPESCRIPT, RUST, GO
│
└── mcp_servers/                 ← Model Context Protocol servers
    ├── servers.py               Server parameter definitions
    └── adapters.py              run_with_mcp_tools() lifecycle manager
```

---

## Configuration (two lines to change)

Open `agency.py` and edit **Section 1** and **Section 2**:

### Section 1 — Model profile

```python
from config.profiles import BALANCED   # ← change this
PROFILE = BALANCED
```

| Profile | Best for | Cost |
|---|---|---|
| `POWER` | Production, highest quality | $$$ |
| `BALANCED` | Day-to-day development | $$ |
| `FAST` | Rapid prototyping | $ |
| `BUDGET` | Experiments | ¢ |
| `LOCAL` | Privacy / no API costs | Free (Ollama) |

### Section 2 — Skill packs per agent

```python
SKILL_ASSIGNMENTS = {
    "architect": [CLOUD_AWS, API],      # cloud design + REST expertise
    "developer": [PYTHON, DATABASE],    # Python + SQL skills
    "reviewer":  [SECURITY],            # OWASP / CVE review
    "tester":    [TESTING, PYTHON],     # pytest + hypothesis
    "devops":    [CLOUD_AWS],           # AWS deployment
}
```

Full list of packs: **[docs/skill_packs.md](docs/skill_packs.md)**

---

## MCP Servers (optional)

Three external tool servers extend agents with real GitHub, web-search, and filesystem capabilities:

| Server | Provides | Requires |
|---|---|---|
| GitHub | code search, PR diffs, issue lookup | `GITHUB_TOKEN` |
| Brave Search | privacy-respecting web search | `BRAVE_API_KEY` |
| Filesystem | directory tree, bulk file ops | Node.js ≥ 18 |

Setup: **[docs/mcp_servers.md](docs/mcp_servers.md)**

---

## Docs

| Document | Contents |
|---|---|
| [docs/setup.md](docs/setup.md) | Prerequisites, installation, environment variables |
| [docs/local_models.md](docs/local_models.md) | **Ollama local model setup — no API keys** |
| [docs/agents.md](docs/agents.md) | **Manager + all 5 agents — roles, models, tools, outputs** |
| [docs/configuration.md](docs/configuration.md) | Profiles and skill pack reference |
| [docs/skill_packs.md](docs/skill_packs.md) | All 16 skill packs with descriptions |
| [docs/mcp_servers.md](docs/mcp_servers.md) | MCP server setup and troubleshooting |
| [docs/extending.md](docs/extending.md) | Add custom skill packs, agents, or tasks |
| [docs/architecture.md](docs/architecture.md) | System design and data flow |

---

## Requirements

- Python 3.11+
- At least one API key: OpenAI **or** Anthropic **or** Google AI
- Node.js ≥ 18 *(optional — only needed for MCP servers)*

---

## License

MIT
