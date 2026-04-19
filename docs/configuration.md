# Configuration Reference

All team configuration lives in the top two sections of `agency.py`.
No other files need to be edited for typical use.

---

## Section 1 — Model Profiles

A profile assigns one LLM to each role in the agency.

### Switching profiles

```python
# agency.py — Section 1
from config.profiles import BALANCED   # ← change this import
PROFILE = BALANCED
```

### Pre-built profiles

| Profile | Manager | Architect | Developer | Reviewer | Tester / DevOps |
|---|---|---|---|---|---|
| `POWER` | claude-3-opus | gemini-1.5-pro | gpt-4o | claude-3-5-sonnet | gpt-4o |
| `BALANCED` ✦ | claude-3-5-sonnet | gemini-1.5-flash | gpt-4o | claude-3-5-sonnet | gpt-4o-mini |
| `FAST` | claude-3-haiku | gemini-1.5-flash | gpt-4o-mini | claude-3-haiku | gpt-4o-mini |
| `BUDGET` | gpt-4o-mini | gemini-1.5-flash | gpt-4o-mini | gpt-4o-mini | gpt-3.5-turbo |
| `COPILOT_PRO` ★ | gh:claude-3-7-sonnet | gh:claude-3-7-sonnet | gh:gpt-4o | gh:claude-3-7-sonnet | gh:gpt-4o-mini |
| `COPILOT_STANDARD` | gh:gpt-4o | gh:gpt-4o | gh:gpt-4o | gh:gpt-4o | gh:gpt-4o-mini |
| `LOCAL` / `LOCAL_BALANCED` | llama3.1:8b | mistral:7b | qwen2.5-coder:14b | llama3.1:8b | phi3:medium |
| `LOCAL_FAST` | mistral:7b | mistral:7b | qwen2.5-coder:7b | mistral:7b | phi3:mini |
| `LOCAL_QUALITY` | llama3.1:70b | llama3.1:70b | qwen2.5-coder:32b | llama3.1:70b | mistral:7b |

✦ Recommended default. ★ Requires `GITHUB_TOKEN` with `models:read` scope. Local profiles require Ollama — see **[local_models.md](local_models.md)**.


### Custom profile

```python
from config.profiles import AgencyProfile

PROFILE = AgencyProfile(
    name="my_team",
    description="Cost-optimised with strong developer model.",
    manager="claude-3-5-sonnet-20241022",
    architect="gemini-1.5-pro",
    developer="gpt-4o",           # best for coding tasks
    reviewer="claude-3-5-sonnet-20241022",
    default="gpt-4o-mini",        # used for tester + devops
    temperatures={                # optional per-role overrides
        "developer": 0.0,         # fully deterministic code
        "architect": 0.3,         # slightly more creative plans
    },
)
```

### Per-agent model override

You can override individual agents independently of the profile
by passing `model=` directly to the factory in `build_and_run_crew()`:

```python
architect = create_architect(
    model="gemini-1.5-pro",          # override just this agent
    skill_packs=_packs.get("architect"),
    extra_tools=mcp_tools.get("architect", []),
)
```

### Supported model name prefixes

The `get_llm(model, temperature)` function in `config/settings.py` detects
providers automatically:

| Prefix | Provider | Example |
|---|---|---|
| `gh:<model>` | **GitHub Models API** (OpenAI-compat, uses `GITHUB_TOKEN`) | `gh:gpt-4o`, `gh:claude-3-7-sonnet-20250219` |
| `gpt-*`, `o1-*`, `o3-*`, `o4-*` | OpenAI | `gpt-4o`, `o3-mini` |
| `claude-*` | Anthropic | `claude-3-5-sonnet-20241022` |
| `gemini-*` | Google AI | `gemini-1.5-pro`, `gemini-1.5-flash` |
| `llama*`, `codellama*`, `phi*`, `mistral*`, `deepseek*`, `qwen*`, `mixtral*` | Ollama (local) | `llama3.1`, `codellama` |
| anything else | OpenAI (fallback) | custom fine-tuned model IDs |

---

## GitHub Copilot Pro models

All GitHub Models are accessed through a single OpenAI-compatible endpoint — no extra
API keys beyond your existing `GITHUB_TOKEN`.

### Setup

```bash
# 1. Create a PAT at https://github.com/settings/tokens
#    Required scopes:  repo  +  models:read
export GITHUB_TOKEN=ghp_...
```

> **Rate limits**
> - Free GitHub account: limited RPM and daily token cap
> - **GitHub Copilot Pro**: ~10× higher limits across all models
> - **GitHub Copilot Pro+**: highest available limits

### Switching to Copilot

```python
# agency.py — Section 1
from config.profiles import COPILOT_PRO  # or COPILOT_STANDARD
PROFILE = COPILOT_PRO
```

### Available models on GitHub Models

Browse the full catalogue: <https://github.com/marketplace/models>

Use any model with the `gh:` prefix:

| Model (gh: prefix) | Provider | Best for |
|---|---|---|
| `gh:claude-3-7-sonnet-20250219` | Anthropic | Manager, Architect, Reviewer |
| `gh:claude-3-5-sonnet-20241022` | Anthropic | Reviewer, Manager |
| `gh:claude-3-5-haiku-20241022` | Anthropic | Fast tasks |
| `gh:gpt-4o` | OpenAI | Developer, general purpose |
| `gh:gpt-4o-mini` | OpenAI | Tester, DevOps, bulk tasks |
| `gh:o3-mini` | OpenAI | Complex reasoning |
| `gh:meta-llama/Llama-3.3-70B-Instruct` | Meta | Open-weight alternative |
| `gh:microsoft/Phi-4` | Microsoft | Fast small model |
| `gh:mistral-large-2411` | Mistral | European data-residency |

### Custom Copilot profile

```python
from config.profiles import AgencyProfile

PROFILE = AgencyProfile(
    name="my_copilot",
    description="Copilot Pro with o3-mini for reasoning roles.",
    manager="gh:claude-3-7-sonnet-20250219",  # deep orchestration
    architect="gh:o3-mini",                   # strong reasoning for planning
    developer="gh:gpt-4o",                    # best coder
    reviewer="gh:claude-3-7-sonnet-20250219", # sharpest review
    default="gh:gpt-4o-mini",                 # fast + cheap
)
```

---

## Section 2 — Skill Pack Assignments

Skill packs extend agents with:
1. **Domain-specific documentation tools** (pre-configured scrapers pointing at official docs)
2. **Expertise injected into the agent backstory** (tells the LLM what it knows)

### Assignment syntax

```python
# agency.py — Section 2
from skills.packs import PYTHON, JAVA, CLOUD_AWS, DATABASE, SECURITY, API, TESTING

SKILL_ASSIGNMENTS = {
    "architect": [CLOUD_AWS, API],     # list of SkillPack objects
    "developer": [PYTHON, DATABASE],
    "reviewer":  [SECURITY],
    "tester":    [TESTING, PYTHON],
    "devops":    [CLOUD_AWS],
}
```

- Any role can have **zero or more** packs.
- Multiple packs are merged — tools from all packs are combined, backstory
  addenda are concatenated.
- Packs can be used on **multiple roles** (e.g. `PYTHON` on both developer and tester).

### Full pack list

See **[skill_packs.md](skill_packs.md)** for descriptions, tool lists, and use-case guidance.

---

## Environment variables

| Variable | Required? | Used by |
|---|---|---|
| `OPENAI_API_KEY` | If using GPT models | Developer (default), Tester, DevOps |
| `ANTHROPIC_API_KEY` | If using Claude models | Manager, Reviewer (default) |
| `GOOGLE_API_KEY` | If using Gemini models | Architect (default) |
| `SERPER_API_KEY` | Optional | All agents (web search skill) |
| `GITHUB_TOKEN` | Optional | GitHub MCP + GithubSearchTool |
| `BRAVE_API_KEY` | Optional | Brave Search MCP server |

---

## Source directory and task file

```python
# agency.py — near the bottom
SOURCE_DIRECTORY = "./src"           # where developer writes code
TASK_FILE        = "./project_tasks.md"
```

Change these paths to point to your actual source tree.

---

## Controlling verbosity and rate limits

Edit the `Crew()` constructor inside `build_and_run_crew()`:

```python
agency = Crew(
    ...
    verbose=True,        # set False to suppress per-step output
    max_rpm=10,          # max requests per minute (throttle API calls)
    memory=True,         # enable cross-task memory (experimental)
)
```
