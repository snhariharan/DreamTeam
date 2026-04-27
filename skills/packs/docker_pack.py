"""
Docker Skill Pack
-----------------
Gives an agent production-grade Docker expertise:
  • Dockerfile authoring (multi-stage, minimal attack surface)
  • Docker Compose for local multi-service stacks
  • OCI image best practices (layer caching, BuildKit, distroless)
  • Container security (non-root, read-only rootfs, image scanning)
  • Container registries: Docker Hub, Amazon ECR, Google Artifact Registry,
    Azure Container Registry

Best for: Cloud DevOps Specialist, Senior Developer
"""
from crewai_tools import ScrapeWebsiteTool

from skills.packs import SkillPack


def _docker_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://docs.docker.com/build/"),
        ScrapeWebsiteTool(website_url="https://docs.docker.com/compose/"),
        ScrapeWebsiteTool(website_url="https://docs.docker.com/build/building/multi-stage/"),
        ScrapeWebsiteTool(website_url="https://docs.docker.com/develop/security-best-practices/"),
        ScrapeWebsiteTool(website_url="https://docs.docker.com/build/cache/"),
        ScrapeWebsiteTool(website_url="https://github.com/GoogleContainerTools/distroless"),
        ScrapeWebsiteTool(website_url="https://docs.docker.com/scout/"),
    ]


DOCKER = SkillPack(
    name="docker",
    description=(
        "Dockerfile multi-stage builds, BuildKit cache mounts, Docker Compose, "
        "distroless / slim base images, container security scanning (Docker Scout)."
    ),
    tools_factory=_docker_tools,
    backstory_addendum=(
        "You are a container expert. You write production Dockerfiles that follow "
        "every best practice: multi-stage builds to keep final images small, "
        "BuildKit cache mounts (--mount=type=cache) to accelerate layer "
        "reconstruction, a dedicated non-root runtime user (useradd / adduser), "
        "read-only root filesystem where possible, and a HEALTHCHECK with a "
        "meaningful check interval. You choose base images deliberately — "
        "distroless (gcr.io/distroless) for zero-shell security, debian-slim "
        "when a shell is unavoidable, and alpine only when libc compatibility "
        "is confirmed. You pin every base image to a specific digest (not just "
        "a mutable tag) for reproducibility. You write Docker Compose files for "
        "local development with named volumes for databases, environment-variable-"
        "injected secrets (no hardcoded values), and healthcheck dependencies "
        "(depends_on: condition: service_healthy). You run Docker Scout or Trivy "
        "scans in CI and block builds on HIGH/CRITICAL CVEs. You push to ECR, "
        "Artifact Registry, or Azure Container Registry using OIDC (no long-lived "
        "registry credentials in CI secrets)."
    ),
    goal_addendum=(
        "Write minimal multi-stage Dockerfiles with non-root users, pinned digests, "
        "BuildKit cache mounts, and Docker Compose for local dev."
    ),
)
