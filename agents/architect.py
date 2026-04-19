"""
Solution Architect
------------------
Reads the codebase and external documentation, then produces a precise
technical implementation plan before any code is written.

Core skills (crewai_tools):
  - Browse directory trees and read source files
  - Live web search and page scraping
  - Semantic GitHub repository search
  - JSON / XML / plain-text config inspection
  - Code documentation search

Flexible configuration:
  model       — override the LLM (any model string; provider auto-detected)
  skill_packs — inject domain skill bundles, e.g. CLOUD_AWS, API, GRAPHQL

Recommended skill packs: CLOUD_AWS | CLOUD_GCP | CLOUD_AZURE | API | GRAPHQL

MCP-augmented (optional — injected via extra_tools):
  - GitHub MCP   : clone repos, read PR diffs, search issues & code
  - Brave Search : privacy-respecting research queries and CVE lookups
"""
from __future__ import annotations

from crewai import Agent

from config.settings import get_llm, get_architect_llm
from skills.filesystem     import read_file, read_dir
from skills.web_research   import get_web_search, get_web_scrape, get_github_search
from skills.config_parsing import get_json_search, get_txt_search, get_xml_search
from skills.docs_search    import get_code_docs


def create_architect(
    model:       str | None = None,
    extra_tools: list | None = None,
    skill_packs: list | None = None,
) -> Agent:
    """
    Factory: returns a fully configured Solution Architect agent.

    Args:
        model:       LLM model name string override (e.g. "gpt-4o",
                     "claude-3-5-sonnet-20241022", "gemini-1.5-pro").
                     Uses the profile default when None.
        extra_tools: Additional BaseTool instances (e.g. from MCP servers).
        skill_packs: Domain SkillPack instances to inject
                     (e.g. [CLOUD_AWS, API]).
    """
    # ── Base tool set ────────────────────────────────────────────────────
    tools = [
        read_dir,                # Understand project structure end-to-end
        read_file,               # Deep-read any source file before planning
        get_web_search(),        # Research best practices, libraries, RFCs
        get_web_scrape(),        # Pull content directly from documentation URLs
        get_github_search(),     # Find canonical reference implementations
        get_code_docs(),         # Semantic search inside existing code docs
        get_json_search(),       # Inspect openapi specs, package.json
        get_txt_search(),        # Read YAML / plain-text config files
        get_xml_search(),        # Inspect XML configuration files
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
    llm = get_llm(model, temperature=0.2) if model else get_architect_llm()

    return Agent(
        role="Solution Architect",
        goal=(
            "Analyse the existing codebase and authoritative external documentation, "
            "then produce a precise, file-level technical implementation plan that is "
            f"safe, scalable, and fully backwards-compatible.{goal_addendum}"
        ),
        backstory=(
            "You are a Staff-level Solution Architect with 15 years of experience "
            "designing distributed systems across cloud and on-premises environments. "
            "You are fluent in REST, GraphQL, event-driven architecture, DDD, and "
            "microservices patterns. You never begin a plan without reading every "
            "relevant file, querying authoritative documentation, and reasoning "
            "carefully about backward compatibility. Your implementation plans are "
            f"so detailed that a senior engineer can execute them without ambiguity.{backstory_addendum}"
        ),
        tools=tools,
        llm=llm,
        allow_delegation=False,
        verbose=True,
    )
