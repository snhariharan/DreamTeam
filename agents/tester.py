"""
QA Automation Engineer
-----------------------
Writes an exhaustive test suite for all new or changed code.

Core skills (crewai_tools):
  - Read existing test structure and source files to derive test cases
  - Write test files to disk under tests/
  - Web search for pytest plugins, testing patterns

Flexible configuration:
  model       — override the LLM (any model string; provider auto-detected)
  skill_packs — inject domain skill bundles, e.g. TESTING, PYTHON

Recommended skill packs: TESTING | PYTHON | JAVA

MCP-augmented (optional — injected via extra_tools):
  - GitHub MCP : find test patterns used in similar open-source libraries
"""
from __future__ import annotations

from crewai import Agent

from config.settings import get_llm, get_default_llm
from skills.filesystem   import read_file, write_file, read_dir
from skills.web_research import get_web_search


def create_tester(
    model:       str | None = None,
    extra_tools: list | None = None,
    skill_packs: list | None = None,
) -> Agent:
    """
    Factory: returns a fully configured QA Automation Engineer agent.

    Args:
        model:       LLM model name string override.
                     Uses the profile default when None.
        extra_tools: Additional BaseTool instances (e.g. from MCP servers).
        skill_packs: Domain SkillPack instances to inject
                     (e.g. [TESTING, PYTHON]).
    """
    # ── Base tool set ────────────────────────────────────────────────────
    tools = [
        read_dir,             # Locate existing test structure and conventions
        read_file,            # Read source files to derive precise test cases
        write_file,           # Write test files under {source_directory}/tests/
        get_web_search(),     # Research pytest plugins and hypothesis strategies
    ]

    # ── Domain skill packs ───────────────────────────────────────────────
    backstory_addendum = ""
    goal_addendum      = ""
    if skill_packs:
        for pack in skill_packs:
            tools.extend(pack.get_tools())
            if pack.backstory_addendum:
                backstory_addendum += f" {pack.backstory_addendum}"
            if pack.goal_addendum:
                goal_addendum += f" {pack.goal_addendum}"

    # ── MCP tools ────────────────────────────────────────────────────────
    if extra_tools:
        tools.extend(extra_tools)

    # ── LLM (profile or explicit override) ──────────────────────────────
    llm = get_llm(model, temperature=0.1) if model else get_default_llm()

    return Agent(
        role="QA Automation Engineer",
        goal=(
            "Write and execute an exhaustive test suite that covers happy "
            "paths, edge cases, boundary conditions, and expected exceptions "
            f"for every new or changed function.{goal_addendum}"
        ),
        backstory=(
            "You are a meticulous QA Automation Engineer obsessed with breaking "
            "code. You probe every corner of the implementation using test "
            "frameworks, property-based testing, and test doubles. Your test "
            "files are written so clearly that other engineers read them to "
            "understand what the code is supposed to do. You follow the test "
            "pyramid: many fast unit tests, fewer integration tests, minimal "
            f"end-to-end tests.{backstory_addendum}"
        ),
        tools=tools,
        llm=llm,
        allow_code_execution=True,   # execute tests and confirm green before reporting
        allow_delegation=False,
        verbose=True,
    )
