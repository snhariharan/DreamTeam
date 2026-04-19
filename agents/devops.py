"""
Cloud DevOps Specialist
-----------------------
Packages the application into a production-ready Docker image and creates
fully automated CI/CD pipelines.

Core skills (crewai_tools):
  - Inspect project structure to determine Dockerfile build context
  - Read requirements, entrypoints, and existing config files
  - Write Dockerfile, docker-compose.yml, and CI/CD pipeline YAML to disk
  - Parse and validate plain-text / XML / JSON manifests
  - Web search for cloud provider docs and best practices
  - Scrape official Docker / Kubernetes / GitHub Actions documentation

Flexible configuration:
  model       — override the LLM (any model string; provider auto-detected)
  skill_packs — inject domain skill bundles, e.g. CLOUD_AWS, DATABASE

Recommended skill packs: CLOUD_AWS | CLOUD_GCP | CLOUD_AZURE | DATABASE

MCP-augmented (optional — injected via extra_tools):
  - Brave Search   : cloud provider changelogs and security announcements
  - Filesystem MCP : bulk traversal for multi-service monorepos
"""
from __future__ import annotations

from crewai import Agent

from config.settings import get_llm, get_default_llm
from skills.filesystem     import read_file, write_file, read_dir
from skills.web_research   import get_web_search, get_web_scrape
from skills.config_parsing import get_json_search, get_txt_search, get_xml_search


def create_devops(
    model:       str | None = None,
    extra_tools: list | None = None,
    skill_packs: list | None = None,
) -> Agent:
    """
    Factory: returns a fully configured Cloud DevOps Specialist agent.

    Args:
        model:       LLM model name string override.
                     Uses the profile default when None.
        extra_tools: Additional BaseTool instances (e.g. from MCP servers).
        skill_packs: Domain SkillPack instances to inject
                     (e.g. [CLOUD_AWS]).
    """
    # ── Base tool set ────────────────────────────────────────────────────
    tools = [
        read_dir,              # Inspect project structure for Dockerfile context
        read_file,             # Read requirements, entrypoints, existing configs
        write_file,            # Write Dockerfile, docker-compose.yml, pipeline YAML
        get_txt_search(),      # Read YAML manifests and plain-text configs
        get_xml_search(),      # Parse XML manifests and config files
        get_json_search(),     # Parse package manifests and lock files
        get_web_search(),      # Look up cloud provider docs and best practices
        get_web_scrape(),      # Fetch official Docker / k8s / GH Actions references
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
    llm = get_llm(model, temperature=0.2) if model else get_default_llm()

    return Agent(
        role="Cloud DevOps Specialist",
        goal=(
            "Package the application into a production-ready Docker image and "
            "create an automated CI/CD pipeline that builds, tests, and deploys "
            f"it.{goal_addendum}"
        ),
        backstory=(
            "You are a Cloud DevOps Specialist certified in AWS, GCP, and Azure. "
            "You write minimal, multi-stage Dockerfiles, declarative Kubernetes "
            "manifests, and GitHub Actions / Azure DevOps pipelines. You follow "
            "the 12-factor app methodology, inject all secrets via environment "
            "variables, always add health checks, liveness probes, and rollback "
            "strategies. Security hardening and least-privilege IAM are "
            f"non-negotiable for you.{backstory_addendum}"
        ),
        tools=tools,
        llm=llm,
        allow_delegation=False,
        verbose=True,
    )
