"""
Senior Software Engineer
------------------------
Implements the Architect's plan by writing clean, production-ready code
and persisting every change to disk.

Core skills (crewai_tools):
  - Read directory trees and source files before editing
  - Write / create source files to disk
  - Semantic code documentation search
  - Web search for syntax help or edge-case solutions
  - Inspect JSON / plain-text config files

Flexible configuration:
  model       — override the LLM (any model string; provider auto-detected)
  skill_packs — inject domain skill bundles, e.g. PYTHON, JAVA, DATABASE

Recommended skill packs: PYTHON | JAVA | KOTLIN | NODEJS | TYPESCRIPT |
                          RUST | GO | DATABASE | NOSQL | API

MCP-augmented (optional — injected via extra_tools):
  - GitHub MCP     : look up library examples, read external source code
  - Filesystem MCP : advanced file traversal and bulk file operations
"""
from __future__ import annotations

from crewai import Agent

from config.settings import get_llm, get_developer_llm
from skills.filesystem     import read_file, write_file, read_dir
from skills.web_research   import get_web_search
from skills.config_parsing import get_json_search, get_txt_search
from skills.docs_search    import get_code_docs


def create_developer(
    model:       str | None = None,
    extra_tools: list | None = None,
    skill_packs: list | None = None,
) -> Agent:
    """
    Factory: returns a fully configured Senior Developer agent.

    Args:
        model:       LLM model name string override (e.g. "gpt-4o", "codellama").
                     Uses the profile default when None.
        extra_tools: Additional BaseTool instances (e.g. from MCP servers).
        skill_packs: Domain SkillPack instances to inject
                     (e.g. [PYTHON, DATABASE]).
    """
    # ── Base tool set ────────────────────────────────────────────────────
    tools = [
        read_dir,              # Survey the project layout before touching anything
        read_file,             # Read existing files to maintain compatibility
        write_file,            # Persist every new or modified source file to disk
        get_code_docs(),       # Look up library APIs without leaving the workflow
        get_web_search(),      # Search for solutions, patterns, or syntax help
        get_json_search(),     # Inspect package.json, API specs, config files
        get_txt_search(),      # Read YAML / plain-text config files
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
    llm = get_llm(model, temperature=0.1) if model else get_developer_llm()

    return Agent(
        role="Senior Software Engineer",
        goal=(
            "Implement the Architect's plan by writing clean, tested, "
            "production-ready code. Follow SOLID principles, keep functions "
            "small, add type hints and docstrings, and never break existing "
            f"behaviour.{goal_addendum}"
        ),
        backstory=(
            "You are a 10x Senior Engineer with deep expertise in Python, "
            "REST APIs, async programming, SQL/NoSQL databases, and cloud SDKs. "
            "You write DRY, self-documenting code with type hints and clear "
            "docstrings. You always read existing files before modifying them, "
            "validate configs against their schemas, and confirm correctness "
            "before handing off. You treat the codebase like a shared resource "
            f"that future engineers will maintain.{backstory_addendum}"
        ),
        tools=tools,
        llm=llm,
        allow_code_execution=True,   # run snippets to verify logic before writing
        allow_delegation=False,
        verbose=True,
    )
