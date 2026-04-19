# Architecture

System design and data flow for the DreamTeam multi-agent agency.

---

## High-level overview

```
 ┌─────────────────────────────────────────────────────┐
 │                    agency.py                         │
 │  ┌──────────────┐    ┌──────────────────────────┐   │
 │  │   Section 1  │    │       Section 2           │   │
 │  │ PROFILE      │    │ SKILL_ASSIGNMENTS         │   │
 │  │ (model names)│    │ (domain skill packs)      │   │
 │  └──────┬───────┘    └────────────┬─────────────┘   │
 └─────────┼───────────────────────┼─────────────────┘
           │                       │
           ▼                       ▼
 ┌─────────────────────────────────────────────────────┐
 │              run_with_mcp_tools()                    │
 │  Starts MCP servers, collects tools per role         │
 └───────────────────────┬─────────────────────────────┘
                         │
                         ▼
 ┌─────────────────────────────────────────────────────┐
 │              build_and_run_crew()                    │
 │                                                      │
 │  create_architect(model, skill_packs, mcp_tools)     │
 │  create_developer(model, skill_packs, mcp_tools)     │
 │  create_reviewer (model, skill_packs, mcp_tools)     │
 │  create_tester   (model, skill_packs, mcp_tools)     │
 │  create_devops   (model, skill_packs, mcp_tools)     │
 └───────────────────────┬─────────────────────────────┘
                         │
                         ▼
 ┌─────────────────────────────────────────────────────┐
 │          CrewAI Hierarchical Crew                    │
 │                                                      │
 │  Manager LLM (from PROFILE.manager)                  │
 │      │                                               │
 │      ├─► Architect  ──► analysis_task                │
 │      ├─► Developer  ──► coding_task                  │
 │      ├─► Reviewer   ──► review_task                  │
 │      ├─► Tester     ──► testing_task                 │
 │      └─► DevOps     ──► deployment_task              │
 └─────────────────────────────────────────────────────┘
```

---

## Agent tool stack

Each agent receives three layers of tools, merged at construction time:

```
Agent tools = [base skills] + [skill pack tools] + [MCP tools]
```

```
 ┌─────────────────────────────────────────────────────┐
 │  skills/                   (crewai_tools wrappers)   │
 │  ├── filesystem.py         FileRead, FileWriter, Dir │
 │  ├── web_research.py       Serper, Scrape, GitHub    │
 │  ├── config_parsing.py     JSON, TXT, XML search     │
 │  └── docs_search.py        CodeDocs, MDX search      │
 └────────────────────┬────────────────────────────────┘
                      │ base layer
 ┌────────────────────▼────────────────────────────────┐
 │  skills/packs/             (domain SkillPacks)       │
 │  ├── python_pack.py        docs.python.org, pypi     │
 │  ├── cloud_pack.py         AWS / GCP / Azure docs    │
 │  ├── security_pack.py      OWASP, NVD, CWE           │
 │  └── ...                                             │
 └────────────────────┬────────────────────────────────┘
                      │ domain layer
 ┌────────────────────▼────────────────────────────────┐
 │  mcp_servers/              (external processes)      │
 │  ├── GitHub MCP            26 tools                  │
 │  ├── Brave Search          2 tools                   │
 │  └── Filesystem MCP        10 tools                  │
 └─────────────────────────────────────────────────────┘
                      │ external layer
                      ▼
              Agent.tools = all merged
```

---

## Task pipeline

Tasks run **sequentially**. Each task's output becomes context for the next.

```
 project_tasks.md
        │
        ▼
 ┌──────────────────┐
 │  analysis_task   │  Architect reads codebase + tasks → implementation plan
 └────────┬─────────┘
          │ plan
          ▼
 ┌──────────────────┐
 │  coding_task     │  Developer implements plan → writes files to src/
 └────────┬─────────┘
          │ code
          ▼
 ┌──────────────────┐
 │  review_task     │  Reviewer checks code → writes review_report.md
 └────────┬─────────┘
          │ approval
          ▼
 ┌──────────────────┐
 │  testing_task    │  Tester writes PyTest suite → src/tests/
 └────────┬─────────┘
          │ tests
          ▼
 ┌──────────────────┐
 │  deployment_task │  DevOps writes Dockerfile + docker-compose + CI/CD
 └──────────────────┘
```

---

## Lazy initialisation pattern

All LLMs and embedding-based tools in DreamTeam are constructed **lazily**
(only when `agency.py` actually runs), not at module import time.

This means you can `import` any module without having API keys set —
useful for testing, CI lint checks, and IDEs.

```
Module load time:
  config/settings.py   → defines functions (no LLM instances)
  skills/web_research  → defines get_*() factories (no tool instances)
  agents/architect.py  → defines create_architect() (no Agent instances)

Runtime (agency.py __main__):
  get_llm("gemini-1.5-flash")  → ChatGoogleGenerativeAI(...)  ✅ key is set
  get_web_search()             → SerperDevTool()               ✅ ready
  create_architect(...)        → Agent(tools=[...], llm=...)   ✅ fully built
```

---

## MCP server lifecycle

```
  ExitStack context opens
    │
    ├─ npx -y @modelcontextprotocol/server-github     (subprocess)
    ├─ npx -y @modelcontextprotocol/server-brave-search (subprocess)
    └─ npx -y @modelcontextprotocol/server-filesystem   (subprocess)
    │
    │  Each MCPServerAdapter wraps the subprocess stdin/stdout
    │  and exposes its tools as crewai BaseTool instances
    │
    ├─ Agents created with MCP tools in their tool list
    ├─ crew.kickoff() — all tool calls are routed through adapters
    │
  ExitStack context closes
    └─ All subprocesses terminated (SIGTERM → SIGKILL fallback)
```

---

## Key design decisions

| Decision | Rationale |
|---|---|
| **Factory functions for agents** | Agents need LLMs + tools at runtime. Factories delay construction, enabling lazy credentials and flexible injection. |
| **`run_with_mcp_tools(callback)`** | MCP subprocesses must be alive while the crew runs. The callback pattern enforces this without requiring nested `with` blocks in `agency.py`. |
| **Folder named `mcp_servers/` not `mcp/`** | Avoids shadowing the `mcp` pip package. |
| **All tool getters are lazy** | `crewai_tools` RAG-based tools and GithubSearchTool validate credentials at construction time. Lazy getters prevent import-time failures. |
| **SkillPack `tools_factory` is callable** | Prevents tools from being instantiated at module load. Tools are only built when `pack.get_tools()` is called inside an agent factory. |
| **Profile temperatures** | Different tasks have different creativity needs. Planning (0.2) benefits from slight creativity; coding and review (0.1) should be deterministic. |
