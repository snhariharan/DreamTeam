"""
DreamTeam Agency — Main Entry Point
=====================================
Configure your team in Section 1 and Section 2 below, then run:

    python agency.py

Execution flow:
  1. Apply model profile (sets LLM per role)
  2. Connect to MCP servers (GitHub · Brave Search · Filesystem)
  3. Create agents with their crewai skills + domain skill packs + MCP tools
  4. Bind tasks to agents
  5. Kick off the hierarchical crew (manager = profile.manager LLM)
"""
import os

from crewai import Crew, Process

# ──────────────────────────────────────────────────────────────────────────────
# ⚙️  SECTION 1 — CHOOSE A MODEL PROFILE
# ──────────────────────────────────────────────────────────────────────────────
# Pick a pre-built profile, or build a custom one.
#
#   POWER     — Frontier models, best quality, highest cost
#   BALANCED  — Strong quality / cost / speed balance  ← recommended
#   FAST      — Optimised for speed and low cost
#   BUDGET    — Minimum cost models
#   LOCAL     — Ollama local models (no API cost, full privacy)
#
# Custom example:
#   from config.profiles import AgencyProfile
#   PROFILE = AgencyProfile(
#       name="custom", manager="claude-3-5-sonnet-20241022",
#       architect="gemini-1.5-pro", developer="gpt-4o",
#       reviewer="claude-3-5-sonnet-20241022", default="gpt-4o-mini",
#   )

from config.profiles import BALANCED  # noqa: E402  ← change this line to switch profile
PROFILE = BALANCED

# ──────────────────────────────────────────────────────────────────────────────
# ⚙️  SECTION 2 — ASSIGN DOMAIN SKILL PACKS PER AGENT
# ──────────────────────────────────────────────────────────────────────────────
# Import the packs you need and assign them to roles.
# Each pack adds:
#   • Role-specific doc-scraping tools (Python docs, AWS docs, etc.)
#   • Domain expertise injected into the agent's backstory
#
# Available packs:
#   Language  → PYTHON, JAVA, KOTLIN, NODEJS, TYPESCRIPT, RUST, GO
#   Cloud     → CLOUD_AWS, CLOUD_GCP, CLOUD_AZURE
#   Data      → DATABASE, NOSQL
#   Design    → API, GRAPHQL
#   Quality   → SECURITY, TESTING

from skills.packs import (          # noqa: E402
    PYTHON, JAVA,                   # language packs
    CLOUD_AWS, CLOUD_GCP,           # cloud packs
    DATABASE,                       # data packs
    SECURITY,                       # quality packs
    API,                            # design packs
    TESTING,                        # test packs
)

SKILL_ASSIGNMENTS: dict[str, list] = {
    # Solution Architect: AWS cloud design + REST API expertise
    "architect": [CLOUD_AWS, API],

    # Senior Developer: Python + database skills
    "developer": [PYTHON, DATABASE],

    # Principal Reviewer: security-focused review
    "reviewer":  [SECURITY],

    # QA Engineer: testing methodology + Python test frameworks
    "tester":    [TESTING, PYTHON],

    # DevOps: AWS deployment expertise
    "devops":    [CLOUD_AWS],
}

# ──────────────────────────────────────────────────────────────────────────────
# (no further configuration needed below this line)
# ──────────────────────────────────────────────────────────────────────────────

from config.settings import get_llm                   # noqa: E402

from agents.architect import create_architect          # noqa: E402
from agents.developer import create_developer          # noqa: E402
from agents.reviewer  import create_reviewer           # noqa: E402
from agents.tester    import create_tester             # noqa: E402
from agents.devops    import create_devops             # noqa: E402

from tasks.analysis   import create_analysis_task      # noqa: E402
from tasks.coding     import create_coding_task        # noqa: E402
from tasks.review     import create_review_task        # noqa: E402
from tasks.testing    import create_testing_task       # noqa: E402
from tasks.deployment import create_deployment_task    # noqa: E402

from mcp_servers.adapters import run_with_mcp_tools    # noqa: E402


SOURCE_DIRECTORY = "./src"
TASK_FILE        = "./project_tasks.md"


def build_and_run_crew(mcp_tools: dict):
    """
    Build agents + tasks using the active PROFILE, SKILL_ASSIGNMENTS, and
    MCP tools, then kick off the crew.

    This function MUST be called inside the MCP server context (via
    run_with_mcp_tools) so that the MCP subprocess connections remain open
    while the crew is running.

    Args:
        mcp_tools: dict[role_name, list[BaseTool]] — provided by run_with_mcp_tools.
    """
    _packs = SKILL_ASSIGNMENTS

    print(f"🤖  Profile : {PROFILE.name.upper()} — {PROFILE.description}")
    for role, packs in _packs.items():
        if packs:
            names = ", ".join(p.name for p in packs)
            print(f"    {role:<10} skill packs: {names}")
    print()

    # ── Agents ───────────────────────────────────────────────────────────
    architect = create_architect(
        model=PROFILE.architect,
        skill_packs=_packs.get("architect"),
        extra_tools=mcp_tools.get("architect", []),
    )
    developer = create_developer(
        model=PROFILE.developer,
        skill_packs=_packs.get("developer"),
        extra_tools=mcp_tools.get("developer", []),
    )
    reviewer = create_reviewer(
        model=PROFILE.reviewer,
        skill_packs=_packs.get("reviewer"),
        extra_tools=mcp_tools.get("reviewer", []),
    )
    tester = create_tester(
        model=PROFILE.default,
        skill_packs=_packs.get("tester"),
        extra_tools=mcp_tools.get("tester", []),
    )
    devops = create_devops(
        model=PROFILE.default,
        skill_packs=_packs.get("devops"),
        extra_tools=mcp_tools.get("devops", []),
    )

    # ── Tasks (sequential pipeline) ──────────────────────────────────────
    analysis_task   = create_analysis_task(architect)
    coding_task     = create_coding_task(developer)
    review_task     = create_review_task(reviewer)
    testing_task    = create_testing_task(tester)
    deployment_task = create_deployment_task(devops)

    # ── Crew (hierarchical — manager LLM comes from profile) ─────────────
    agency = Crew(
        agents=[architect, developer, reviewer, tester, devops],
        tasks=[
            analysis_task,
            coding_task,
            review_task,
            testing_task,
            deployment_task,
        ],
        process=Process.hierarchical,
        manager_llm=get_llm(PROFILE.manager, temperature=PROFILE.temperature_for("manager")),
        verbose=True,
    )

    return agency.kickoff(
        inputs={
            "task_file":        TASK_FILE,
            "source_directory": SOURCE_DIRECTORY,
        }
    )


if __name__ == "__main__":
    print("🚀  Booting up DreamTeam Multi-Model AI Agency...\n")

    os.makedirs(SOURCE_DIRECTORY, exist_ok=True)
    with open(TASK_FILE, "w") as f:
        f.write('Task 1: Add a /health endpoint that returns {"status": "ok"}.\n')
        f.write("Task 2: Add request-level logging middleware.\n")
        f.write("Task 3: Add JWT authentication to all /api/* routes.\n")

    result = run_with_mcp_tools(build_and_run_crew)

    print("\n========================================")
    print("🏆  FINAL DELIVERABLE")
    print("========================================")
    print(result)