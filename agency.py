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
import argparse
import os
import sys
import textwrap

from dotenv import load_dotenv
from crewai import Crew, Process

# Load API keys from .env (copy .env.example → .env and fill in your keys)
load_dotenv()

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
#   Backend   → PYTHON, JAVA, KOTLIN, SCALA, NODEJS, TYPESCRIPT, RUST, GO
#   Frontend  → REACT, ANGULAR
#   Cloud     → CLOUD_AWS, CLOUD_GCP, CLOUD_AZURE
#   Data      → DATABASE, NOSQL
#   Design    → API, GRAPHQL
#   Quality   → SECURITY, TESTING
#   Container → DOCKER
#   Platform  → KUBERNETES, TERRAFORM, OBSERVABILITY

from skills.packs import (          # noqa: E402
    # ── Backend language packs
    PYTHON, JAVA, KOTLIN, SCALA,
    NODEJS, TYPESCRIPT,
    RUST, GO,
    # ── Frontend packs
    REACT, ANGULAR,
    # ── Cloud packs (all three major providers)
    CLOUD_AWS, CLOUD_GCP, CLOUD_AZURE,
    # ── Data packs
    DATABASE, NOSQL,
    # ── Design packs
    API, GRAPHQL,
    # ── Quality packs
    SECURITY, TESTING,
    # ── CI/CD pipeline packs
    CICD_GITHUB, CICD_AZURE, CICD_AWS,
    CICD_JENKINS, CICD_GITLAB, CICD_CIRCLE,
    # ── Container / platform packs
    DOCKER, KUBERNETES, TERRAFORM, OBSERVABILITY,
)

# Shared bundles — import once, reference by role below
_FULL_BACKEND  = [PYTHON, JAVA, KOTLIN, SCALA, NODEJS, TYPESCRIPT, RUST, GO]
_FULL_FRONTEND = [REACT, ANGULAR]
_FULL_STACK    = [*_FULL_BACKEND, *_FULL_FRONTEND]
_FULL_CLOUD    = [CLOUD_AWS, CLOUD_GCP, CLOUD_AZURE]
_FULL_DATA     = [DATABASE, NOSQL]
_FULL_API      = [API, GRAPHQL]
_FULL_CICD     = [CICD_GITHUB, CICD_AZURE, CICD_AWS, CICD_JENKINS, CICD_GITLAB, CICD_CIRCLE]
_FULL_IaC      = [KUBERNETES, TERRAFORM]           # Infrastructure-as-code

SKILL_ASSIGNMENTS: dict[str, list] = {
    # Solution Architect — understands any codebase (to plan), all clouds
    # (to choose the right service), IaC, CI/CD and observability.
    "architect": [
        *_FULL_BACKEND,     # read and plan around any backend language
        *_FULL_FRONTEND,    # understand existing React / Angular code
        *_FULL_CLOUD,       # cloud-agnostic service selection
        *_FULL_DATA,        # SQL and NoSQL data model design
        *_FULL_API,         # REST and GraphQL endpoint design
        *_FULL_IaC,         # Kubernetes + Terraform planning
        SECURITY,           # secure-by-design architecture
        OBSERVABILITY,      # design metrics, traces, and alerting
    ],

    # Senior Developer — writes code in the detected stack.
    # Language packs give broad backstory; cloud SDKs reached via web search.
    # Trimming cloud packs here saves ~18 tool slots per agent.
    "developer": [
        *_FULL_BACKEND,     # implement in whichever backend language is detected
        *_FULL_FRONTEND,    # implement React / Angular when required
        *_FULL_DATA,        # ORM / query / migration expertise
        *_FULL_API,         # REST and GraphQL implementation
        DOCKER,             # write multi-stage Dockerfiles and Compose stacks
        OBSERVABILITY,      # instrument with OTel, add Prometheus /metrics
    ],

    # Principal Reviewer — widest view to catch cross-cutting issues.
    # Full stack + cloud + security + CI/CD pipeline review — this is the quality gate.
    "reviewer": [
        *_FULL_BACKEND,     # review any backend language
        *_FULL_FRONTEND,    # review React / Angular code
        *_FULL_CLOUD,       # spot cloud-specific misconfiguration
        *_FULL_DATA,        # catch schema, query, and migration issues
        *_FULL_API,         # verify REST/GraphQL contract correctness
        *_FULL_IaC,         # review Terraform / Kubernetes manifests
        DOCKER,             # review Dockerfile security and layer efficiency
        SECURITY,           # OWASP / CVE / SANS secure-code review
        OBSERVABILITY,      # verify instrumentation quality
        CICD_GITHUB,        # catch insecure workflow patterns (e.g. script injection)
    ],

    # QA Automation Engineer — writes tests, not infrastructure.
    # No cloud-provider or IaC packs: cuts ~24 tool slots, reduces noise.
    "tester": [
        *_FULL_BACKEND,     # write pytest, JUnit, go test, etc.
        *_FULL_FRONTEND,    # write Vitest, Jest, Cypress for UI
        *_FULL_API,         # contract tests for REST and GraphQL
        TESTING,            # TDD/BDD patterns, Hypothesis, mutation testing
    ],

    # Cloud DevOps Specialist — packages and deploys across all platforms.
    # Full CI/CD + IaC + container coverage for any pipeline platform.
    "devops": [
        *_FULL_BACKEND,     # package any backend runtime in Docker correctly
        *_FULL_CLOUD,       # deploy to AWS, GCP, or Azure
        *_FULL_DATA,        # configure managed DB instances and backups
        *_FULL_IaC,         # write Terraform modules + Helm charts
        *_FULL_CICD,        # GitHub Actions, Azure DevOps, AWS CodePipeline, Jenkins, GitLab CI, CircleCI
        DOCKER,             # multi-stage Dockerfiles, registries (ECR/GAR/ACR)
        SECURITY,           # least-privilege IAM, OIDC, secrets management
        OBSERVABILITY,      # deploy OTel Collector, Prometheus, Grafana stack
    ],
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
from tasks.fix        import create_fix_task           # noqa: E402

from mcp_servers.adapters import run_with_mcp_tools    # noqa: E402


SOURCE_DIRECTORY  = "./src"
TASK_FILE         = "./project_tasks.md"
REVIEW_REPORT     = "./review_report.md"
TEST_RESULTS      = "./test_results.md"
MAX_REVIEW_CYCLES = 2   # Developer gets up to 2 attempts to pass the Reviewer


def _read_verdict() -> str:
    """Return 'PASS', 'FAIL', or 'UNKNOWN' based on review_report.md contents."""
    if not os.path.exists(REVIEW_REPORT):
        return "UNKNOWN"
    with open(REVIEW_REPORT) as fh:
        content = fh.read()
    if "VERDICT: PASS" in content:
        return "PASS"
    if "VERDICT: FAIL" in content:
        return "FAIL"
    return "UNKNOWN"


def _read_test_verdict() -> str:
    """Return 'PASS', 'FAIL', or 'UNKNOWN' based on test_results.md contents."""
    if not os.path.exists(TEST_RESULTS):
        return "UNKNOWN"
    with open(TEST_RESULTS) as fh:
        content = fh.read()
    if "TEST RESULT: PASS" in content:
        return "PASS"
    if "TEST RESULT: FAIL" in content:
        return "FAIL"
    return "UNKNOWN"


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

    inputs = {
        "task_file":        TASK_FILE,
        "source_directory": SOURCE_DIRECTORY,
    }

    # ── Phase 1: Architect → Developer → Reviewer (with retry) ───────────
    # Run analysis + coding + review in a hierarchical crew.
    # If the Reviewer returns VERDICT: FAIL the Developer gets another attempt
    # (up to MAX_REVIEW_CYCLES total) before proceeding to testing/deployment.
    analysis_task = create_analysis_task(architect)
    coding_task   = create_coding_task(developer)
    review_task   = create_review_task(reviewer)

    review_crew = Crew(
        agents=[architect, developer, reviewer],
        tasks=[analysis_task, coding_task, review_task],
        process=Process.hierarchical,
        manager_llm=get_llm(PROFILE.manager, temperature=PROFILE.temperature_for("manager")),
        verbose=True,
    )

    result = review_crew.kickoff(inputs=inputs)

    # ── Review retry loop ─────────────────────────────────────────────────
    for cycle in range(1, MAX_REVIEW_CYCLES):
        verdict = _read_verdict()
        if verdict != "FAIL":
            break
        print(
            f"\n⚠️  Review cycle {cycle}/{MAX_REVIEW_CYCLES - 1}: "
            f"VERDICT: FAIL — Developer re-addressing findings...\n"
        )
        fix_task        = create_fix_task(developer)
        re_review_task  = create_review_task(reviewer)
        fix_crew = Crew(
            agents=[developer, reviewer],
            tasks=[fix_task, re_review_task],
            process=Process.sequential,
            verbose=True,
        )
        result = fix_crew.kickoff(inputs=inputs)

    final_verdict = _read_verdict()
    print(f"\n{'✅' if final_verdict == 'PASS' else '⚠️ '}  Final review verdict: {final_verdict}\n")

    # ── Guard: skip Phase 2 if code never passed review ──────────────────
    if final_verdict == "FAIL":
        print(
            "❌  Code did not pass review after all retry cycles.\n"
            "    Fix the issues in review_report.md and re-run agency.py.\n"
            "    Skipping test and deployment phases."
        )
        return result

    # ── Phase 2a: Tester ─────────────────────────────────────────────────
    testing_task = create_testing_task(tester)
    tester_crew = Crew(
        agents=[tester],
        tasks=[testing_task],
        process=Process.sequential,
        verbose=True,
    )
    tester_crew.kickoff(inputs=inputs)

    # ── Guard: skip deployment if tests are red ───────────────────────────
    test_verdict = _read_test_verdict()
    print(f"\n{'✅' if test_verdict == 'PASS' else '❌ '}  Test verdict: {test_verdict}\n")

    if test_verdict == "FAIL":
        print(
            "❌  Tests did not pass — skipping deployment.\n"
            "    Check test_results.md for failing test details."
        )
        return result

    # ── Phase 2b: DevOps (only runs after green tests) ────────────────────
    deployment_task = create_deployment_task(devops)
    devops_crew = Crew(
        agents=[devops],
        tasks=[deployment_task],
        process=Process.sequential,
        verbose=True,
    )

    return devops_crew.kickoff(inputs=inputs)


_DEMO_TASK = textwrap.dedent("""\
    Task 1: Add a /health endpoint that returns {"status": "ok"}.
    Task 2: Add request-level logging middleware.
    Task 3: Add JWT authentication to all /api/* routes.
""").strip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="DreamTeam — run the multi-agent AI software crew.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Usage examples
            --------------
            # Describe the task inline:
            python agency.py --task "Build a REST API for a todo list in FastAPI with PostgreSQL."

            # Use a task file you prepared in advance:
            python agency.py --task-file ./my_tasks.md

            # Edit project_tasks.md first, then run without flags:
            python agency.py
        """),
    )
    parser.add_argument(
        "--task", "-t",
        metavar="DESCRIPTION",
        help="One-line (or multi-line quoted) task description.",
    )
    parser.add_argument(
        "--task-file", "-f",
        metavar="PATH",
        default=TASK_FILE,
        help=f"Path to a Markdown task file (default: {TASK_FILE}).",
    )
    args = parser.parse_args()

    os.makedirs(SOURCE_DIRECTORY, exist_ok=True)

    # Priority: --task flag > existing task file > demo task
    if args.task:
        with open(TASK_FILE, "w") as fh:
            fh.write(args.task.strip() + "\n")
        print(f"📋  Task written to {TASK_FILE}")
    elif args.task_file != TASK_FILE and os.path.exists(args.task_file):
        import shutil
        shutil.copy(args.task_file, TASK_FILE)
        print(f"📋  Task file copied from {args.task_file}")
    elif os.path.exists(TASK_FILE):
        print(f"📋  Using existing task file: {TASK_FILE}")
    else:
        # First run with no arguments — create a demo task so the crew can start
        with open(TASK_FILE, "w") as fh:
            fh.write(_DEMO_TASK + "\n")
        print(
            f"📋  No task specified — created demo task in {TASK_FILE}\n"
            f"     Edit that file or pass --task \"..\" to run your own task.\n"
        )

    print("🚀  Booting up DreamTeam Multi-Model AI Agency...\n")

    # Validate that at least one API key is set before wasting time on MCP startup
    _keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY"]
    if not any(os.getenv(k) for k in _keys):
        print(
            "❌  No AI provider API key found.\n"
            "    Set at least one of: OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY\n"
            "    Copy .env.example → .env and fill in your keys, then re-run.",
            file=sys.stderr,
        )
        sys.exit(1)

    result = run_with_mcp_tools(build_and_run_crew)

    print("\n========================================")
    print("🏆  FINAL DELIVERABLE")
    print("========================================")
    print(result)