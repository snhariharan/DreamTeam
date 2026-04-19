# Extending DreamTeam

How to add custom skill packs, agents, tasks, and MCP servers.

---

## Adding a custom skill pack

A `SkillPack` is just a dataclass with a `tools_factory` (lazy callable)
and text that is appended to the agent's backstory and goal.

### 1. Create the pack file

```python
# skills/packs/django_pack.py
from crewai_tools import ScrapeWebsiteTool
from skills.packs import SkillPack


def _django_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://docs.djangoproject.com/en/stable/"),
        ScrapeWebsiteTool(website_url="https://www.django-rest-framework.org/"),
        ScrapeWebsiteTool(website_url="https://channels.readthedocs.io/en/stable/"),
    ]


DJANGO = SkillPack(
    name="django",
    description="Django ORM, DRF, Channels, and deployment best practices.",
    tools_factory=_django_tools,
    backstory_addendum=(
        "You are a Django expert. You use the ORM efficiently (select_related, "
        "prefetch_related, bulk_create), write DRF serializers with proper "
        "validation, and structure projects following Django best practices "
        "(apps, signals, management commands, custom middleware). You handle "
        "async views with Django Channels where needed."
    ),
    goal_addendum="Use Django ORM and DRF following project conventions.",
)
```

### 2. Register in `skills/packs/__init__.py`

```python
# Add alongside the existing imports
from skills.packs.django_pack import DJANGO   # noqa: E402

__all__ = [
    ...,
    "DJANGO",
]
```

### 3. Use in `agency.py`

```python
from skills.packs import PYTHON, DATABASE, DJANGO

SKILL_ASSIGNMENTS = {
    "developer": [PYTHON, DJANGO, DATABASE],
    "tester":    [TESTING, PYTHON, DJANGO],
}
```

---

## Adding a custom agent

### 1. Create the agent factory

```python
# agents/data_scientist.py
"""
Data Scientist
--------------
Produces data analysis, visualisations, and ML model prototypes.
"""
from __future__ import annotations
from crewai import Agent
from config.settings import get_llm, get_default_llm
from skills.filesystem import read_file, write_file, read_dir
from skills.web_research import get_web_search
from skills.docs_search import get_code_docs


def create_data_scientist(
    model:       str | None = None,
    extra_tools: list | None = None,
    skill_packs: list | None = None,
) -> Agent:
    tools = [
        read_dir, read_file, write_file,
        get_web_search(), get_code_docs(),
    ]
    backstory_addendum = ""
    goal_addendum      = ""
    if skill_packs:
        for pack in skill_packs:
            tools.extend(pack.get_tools())
            backstory_addendum += f" {pack.backstory_addendum}"
            goal_addendum      += f" {pack.goal_addendum}"
    if extra_tools:
        tools.extend(extra_tools)

    llm = get_llm(model, temperature=0.1) if model else get_default_llm()

    return Agent(
        role="Data Scientist",
        goal=(
            "Analyse data, build ML prototypes, and produce "
            f"clear visualisations.{goal_addendum}"
        ),
        backstory=(
            "You are a senior Data Scientist with expertise in Python, "
            "pandas, scikit-learn, and matplotlib / seaborn. You write "
            "clean, reproducible Jupyter-compatible scripts and explain "
            f"your findings in plain language.{backstory_addendum}"
        ),
        tools=tools,
        llm=llm,
        allow_delegation=False,
        verbose=True,
    )
```

### 2. Create the task

```python
# tasks/data_analysis.py
from crewai import Task

def create_data_analysis_task(data_scientist) -> Task:
    return Task(
        description=(
            "Analyse the dataset at {data_file}. "
            "Produce a summary of key statistics, identify outliers, "
            "and recommend an ML approach for the target variable."
        ),
        expected_output=(
            "A Markdown report with: summary stats, outlier analysis, "
            "and ML recommendations. Python scripts saved to src/analysis/."
        ),
        agent=data_scientist,
    )
```

### 3. Wire into `agency.py`

```python
from agents.data_scientist import create_data_scientist
from tasks.data_analysis   import create_data_analysis_task

def build_and_run_crew(mcp_tools):
    ...
    data_scientist   = create_data_scientist(model=PROFILE.default)
    data_analysis_task = create_data_analysis_task(data_scientist)

    agency = Crew(
        agents=[architect, developer, data_scientist, reviewer, tester, devops],
        tasks=[analysis_task, coding_task, data_analysis_task, review_task, ...],
        ...
    )
```

---

## Adding a new model profile

```python
# config/profiles.py — add at the bottom
RESEARCH = AgencyProfile(
    name="research",
    description="Optimised for long-context analysis and reasoning tasks.",
    manager="claude-3-5-sonnet-20241022",
    architect="gemini-1.5-pro",          # 2M token context window
    developer="gpt-4o",
    reviewer="claude-3-5-sonnet-20241022",
    default="gpt-4o-mini",
    temperatures={
        "architect": 0.4,   # more creative plans
        "developer": 0.0,   # fully deterministic code
    },
)
```

Then in `agency.py`:
```python
from config.profiles import RESEARCH
PROFILE = RESEARCH
```

---

## Adding an Ollama local model

1. Install Ollama: <https://ollama.com>
2. Pull a model: `ollama pull llama3.1` or `ollama pull codellama`
3. Use the `LOCAL` profile (or a custom profile):

```python
from config.profiles import LOCAL
PROFILE = LOCAL
```

4. Verify Ollama is running: `ollama list`

The `get_llm()` factory detects Ollama models by name prefix and uses
`langchain_ollama.ChatOllama` automatically.

---

## Adding a new MCP server

See **[mcp_servers.md](mcp_servers.md#adding-a-new-mcp-server)** for the full walkthrough.

Short version:
1. Define `StdioServerParameters` in `mcp_servers/servers.py`
2. Add `_safe_attach()` call in `mcp_servers/adapters.py`
3. Add the tools to the appropriate role(s) in `tools_by_role`

---

## Changing the task pipeline

To run only a subset of tasks (e.g. skip DevOps in a quick iteration):

```python
agency = Crew(
    agents=[architect, developer, reviewer],
    tasks=[analysis_task, coding_task, review_task],   # only 3 tasks
    ...
)
```

To add a new task between existing ones:

```python
tasks=[
    analysis_task,
    coding_task,
    my_custom_task,    # inserted between coding and review
    review_task,
    testing_task,
    deployment_task,
]
```
