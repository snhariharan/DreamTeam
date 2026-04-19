# Architecture

System design and data flow for the DreamTeam multi-agent agency.

---

## High-level overview

```mermaid
flowchart TD
    subgraph CFG ["agency.py"]
        P["⚙️ Section 1\nPROFILE\nmodel names"]
        S["⚙️ Section 2\nSKILL_ASSIGNMENTS\ndomain skill packs"]
    end

    MCP["run_with_mcp_tools()\nStarts MCP servers · distributes tools by role"]

    subgraph BUILD ["build_and_run_crew()"]
        CA["create_architect(model, skill_packs, mcp_tools)"]
        CD["create_developer(model, skill_packs, mcp_tools)"]
        CR["create_reviewer (model, skill_packs, mcp_tools)"]
        CT["create_tester   (model, skill_packs, mcp_tools)"]
        CDV["create_devops   (model, skill_packs, mcp_tools)"]
    end

    subgraph CREW ["CrewAI Hierarchical Crew"]
        MGR["🧠 Manager LLM\nfrom PROFILE.manager"]
        MGR -->|"1"| ATK["🏛️ Architect → analysis_task"]
        MGR -->|"2"| DTK["💻 Developer → coding_task"]
        MGR -->|"3"| RTK["🔍 Reviewer  → review_task"]
        MGR -->|"4"| TTK["🧪 Tester    → testing_task"]
        MGR -->|"5"| VTK["🚀 DevOps    → deployment_task"]
    end

    P & S --> MCP --> BUILD --> CREW
```

---

## Agent tool stack

Each agent receives three layers of tools, merged at construction time:

> `Agent.tools = [base skills] + [skill pack tools] + [MCP tools]`

```mermaid
flowchart BT
    BASE["🔧 Base Skills — skills/\nFileRead · FileWriter · DirRead\nSerper · WebScrape · DocsSearch · JSONSearch"]

    PACKS["📦 Domain Skill Packs — skills/packs/\nPYTHON · JAVA · CLOUD_AWS · DATABASE\nSECURITY · API · TESTING · GRAPHQL · ..."]

    MCP["🔌 MCP Tools — mcp_servers/\nGitHub 26 tools · Brave Search 2 tools · Filesystem 10 tools"]

    AGENT(["🤖 Agent.tools"])

    BASE -->|"base layer"| PACKS
    PACKS -->|"+ domain layer"| MCP
    MCP -->|"+ external layer"| AGENT
```

---

## Task pipeline

Tasks run **sequentially**. Each task's output becomes context for the next.

```mermaid
flowchart LR
    T(["📋 project_tasks.md"])

    A["🏛️ analysis_task\nArchitect\nreads codebase + docs\n→ implementation plan"]

    D["💻 coding_task\nDeveloper\nimplements plan\n→ src/ files"]

    R["🔍 review_task\nReviewer\nchecks code\n→ review_report.md"]

    TE["🧪 testing_task\nTester\nwrites pytest suite\n→ src/tests/"]

    DO["🚀 deployment_task\nDevOps\nwrites Dockerfile\n→ CI/CD pipeline"]

    T --> A -->|plan| D -->|code| R -->|approval| TE -->|tests| DO
```

---

## MCP server lifecycle

```mermaid
sequenceDiagram
    participant A as agency.py
    participant E as ExitStack
    participant G as GitHub MCP
    participant B as Brave MCP
    participant F as Filesystem MCP
    participant C as crew.kickoff()

    A->>E: run_with_mcp_tools(callback)
    E->>G: npx start subprocess
    E->>B: npx start subprocess
    E->>F: npx start subprocess
    note over G,F: Tools distributed to agents by role
    E->>C: callback(tools_by_role)
    C->>G: tool calls
    C->>B: tool calls
    C->>F: tool calls
    C-->>E: crew finished
    E->>G: terminate
    E->>B: terminate
    E->>F: terminate
    note over E: ExitStack ensures cleanup even on exception
```

---

## Lazy initialisation pattern

All LLMs and embedding-based tools in DreamTeam are constructed **lazily**
(only when `agency.py` actually runs), not at module import time.

This means you can `import` any module without having API keys set —
useful for testing, CI lint checks, and IDEs.

```mermaid
flowchart LR
    subgraph IMPORT ["Module load time (no keys needed)"]
        direction TB
        S["config/settings.py\ndefines functions only"]
        W["skills/web_research.py\ndefines get_*() factories"]
        AG["agents/architect.py\ndefines create_architect()"]
    end

    subgraph RUNTIME ["Runtime — agency.py __main__"]
        direction TB
        L["get_llm('gemini-1.5-flash')\n→ ChatGoogleGenerativeAI ✅"]
        T["get_web_search()\n→ SerperDevTool ✅"]
        C["create_architect(...)\n→ Agent(tools, llm) ✅"]
    end

    IMPORT -->|"python agency.py\nkeys are set"| RUNTIME
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
