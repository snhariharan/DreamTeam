"""
Principal Code Reviewer
-----------------------
Critically reviews all code output against requirements and coding standards,
then writes a formal PASS / FAIL report to disk.

Core skills (crewai_tools):
  - Read both old and new source files for diff-style comparison
  - Browse directory structure to verify scope of changes
  - Live web search for security advisories and best-practice violations
  - JSON / plain-text config validation
  - Code documentation reference checks
  - Write formal review report to disk

Flexible configuration:
  model       — override the LLM (any model string; provider auto-detected)
  skill_packs — inject domain skill bundles, e.g. SECURITY, API

Recommended skill packs: SECURITY | API | DATABASE

MCP-augmented (optional — injected via extra_tools):
  - GitHub MCP     : inspect PR history, compare against community standards
  - Brave Search   : CVE database lookups, security-advisory research
"""
from __future__ import annotations

from crewai import Agent

from config.settings import get_llm, get_reviewer_llm
from skills.filesystem     import read_file, write_file, read_dir
from skills.web_research   import get_web_search
from skills.config_parsing import get_json_search, get_txt_search
from skills.docs_search    import get_code_docs


def create_reviewer(
    model:       str | None = None,
    extra_tools: list | None = None,
    skill_packs: list | None = None,
) -> Agent:
    """
    Factory: returns a fully configured Principal Reviewer agent.

    Args:
        model:       LLM model name string override.
                     Uses the profile default when None.
        extra_tools: Additional BaseTool instances (e.g. from MCP servers).
        skill_packs: Domain SkillPack instances to inject (e.g. [SECURITY]).
    """
    # ── Base tool set ────────────────────────────────────────────────────
    tools = [
        read_dir,              # Compare file structure before and after
        read_file,             # Read both original and new source files
        get_web_search(),      # Verify security advisories and best practices
        get_code_docs(),       # Confirm library API usage is correct
        get_json_search(),     # Validate JSON config changes
        get_txt_search(),      # Read and validate YAML / plain-text configs
        write_file,            # Write the formal review report to disk
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
    llm = get_llm(model, temperature=0.1) if model else get_reviewer_llm()

    return Agent(
        role="Principal Code Reviewer",
        goal=(
            "Critically review the Developer's output against the original "
            "requirements and existing coding standards. Produce a clear "
            f"PASS or FAIL verdict with actionable, line-specific findings.{goal_addendum}"
        ),
        backstory=(
            "You are a Principal Engineer who has performed thousands of "
            "high-stakes code reviews. You check for correctness, security "
            "vulnerabilities, performance anti-patterns, and style inconsistencies. "
            "You cross-reference the implementation against the task list, look for "
            "missing edge-case handling, scan for hardcoded secrets, and verify that "
            "the code style matches existing conventions. You never rubber-stamp — "
            f"you only approve code that is genuinely production-ready.{backstory_addendum}"
        ),
        tools=tools,
        llm=llm,
        allow_delegation=False,
        verbose=True,
    )
