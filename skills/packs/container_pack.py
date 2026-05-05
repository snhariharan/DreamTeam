"""
Container Skill Packs
---------------------
Gives an agent deep expertise in containerisation and container orchestration.

DOCKER      — Dockerfile authoring, multi-stage builds, Compose, image security
KUBERNETES  — Workload authoring, Helm, RBAC, GitOps (ArgoCD/Flux), Kustomize

Best for: Cloud DevOps Specialist, Solution Architect
"""
from crewai_tools import ScrapeWebsiteTool

from skills.packs import SkillPack


# ── Docker ────────────────────────────────────────────────────────────────

def _docker_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://docs.docker.com/"),
        ScrapeWebsiteTool(website_url="https://docs.docker.com/compose/"),
        ScrapeWebsiteTool(website_url="https://docs.docker.com/build/building/multi-stage/"),
        ScrapeWebsiteTool(website_url="https://docs.docker.com/develop/security-best-practices/"),
        ScrapeWebsiteTool(website_url="https://hub.docker.com/"),
    ]


DOCKER = SkillPack(
    name="docker",
    description="Docker: multi-stage Dockerfiles, Compose, layer caching, image security, registries.",
    tools_factory=_docker_tools,
    backstory_addendum=(
        "You are a Docker expert. You write minimal, multi-stage Dockerfiles that "
        "separate build and runtime stages, use non-root users, pin base image "
        "digests, and include .dockerignore to minimise context size. You optimise "
        "layer order for maximum cache reuse. You write docker-compose.yml files for "
        "local development with named volumes, health checks, and environment "
        "variable injection. You scan images with Trivy or Docker Scout for "
        "vulnerabilities before pushing to a registry (Docker Hub, ECR, GCR, ACR). "
        "You know multi-platform builds (buildx) and the difference between "
        "ENTRYPOINT and CMD."
    ),
    goal_addendum=(
        "Write production-grade multi-stage Dockerfiles and docker-compose.yml "
        "files with health checks, non-root users, and pinned base images."
    ),
)


# ── Kubernetes ────────────────────────────────────────────────────────────

def _kubernetes_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://kubernetes.io/docs/"),
        ScrapeWebsiteTool(website_url="https://helm.sh/docs/"),
        ScrapeWebsiteTool(website_url="https://kustomize.io/"),
        ScrapeWebsiteTool(website_url="https://argo-cd.readthedocs.io/en/stable/"),
        ScrapeWebsiteTool(website_url="https://fluxcd.io/flux/"),
        ScrapeWebsiteTool(website_url="https://kubernetes.io/docs/concepts/security/"),
    ]


KUBERNETES = SkillPack(
    name="kubernetes",
    description="Kubernetes: Deployments, Helm, RBAC, NetworkPolicies, HPA, GitOps (ArgoCD/Flux), Kustomize.",
    tools_factory=_kubernetes_tools,
    backstory_addendum=(
        "You are a Certified Kubernetes Administrator (CKA) and Application "
        "Developer (CKAD). You author production-ready Kubernetes manifests: "
        "Deployments, StatefulSets, Services, Ingress, ConfigMaps, Secrets, "
        "HorizontalPodAutoscaler (HPA), PodDisruptionBudgets, and ResourceQuotas. "
        "You enforce security with RBAC, NetworkPolicies, PodSecurityAdmission, "
        "and Secrets encryption at rest. You package applications with Helm charts "
        "(named templates, values overrides, chart dependencies) and manage "
        "environment differences with Kustomize overlays. You implement GitOps "
        "delivery using ArgoCD or Flux — syncing cluster state from Git. You "
        "configure liveness, readiness, and startup probes, set resource requests "
        "and limits, and use priority classes to protect critical workloads."
    ),
    goal_addendum=(
        "Write production-grade Kubernetes manifests with RBAC, NetworkPolicies, "
        "HPA, and probes. Package with Helm and manage delivery with GitOps."
    ),
)
