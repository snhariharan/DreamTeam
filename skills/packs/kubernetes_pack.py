"""
Kubernetes Skill Pack
---------------------
Gives an agent container orchestration expertise:
  • Kubernetes official docs (workloads, networking, storage, security)
  • Helm chart authoring and chart testing
  • ArgoCD GitOps workflow patterns
  • Istio service mesh (mTLS, traffic management, observability)
  • Kustomize configuration management
  • Kubernetes security (Pod Security Standards, OPA/Gatekeeper)

Best for: Cloud DevOps Specialist, Solution Architect
"""
from crewai_tools import ScrapeWebsiteTool

from skills.packs import SkillPack


def _kubernetes_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://kubernetes.io/docs/"),
        ScrapeWebsiteTool(website_url="https://kubernetes.io/docs/concepts/workloads/"),
        ScrapeWebsiteTool(website_url="https://kubernetes.io/docs/concepts/security/"),
        ScrapeWebsiteTool(website_url="https://helm.sh/docs/"),
        ScrapeWebsiteTool(website_url="https://argo-cd.readthedocs.io/en/stable/"),
        ScrapeWebsiteTool(website_url="https://istio.io/latest/docs/"),
        ScrapeWebsiteTool(website_url="https://kustomize.io/"),
        ScrapeWebsiteTool(website_url="https://kubernetes.io/docs/reference/kubectl/"),
    ]


KUBERNETES = SkillPack(
    name="kubernetes",
    description=(
        "Kubernetes workloads, Helm charts, ArgoCD GitOps, Istio service mesh, "
        "kustomize, Pod Security Standards."
    ),
    tools_factory=_kubernetes_tools,
    backstory_addendum=(
        "You are a Certified Kubernetes Administrator (CKA) and Application Developer "
        "(CKAD). You design production-grade Kubernetes manifests: Deployments, "
        "StatefulSets, DaemonSets, CronJobs, HorizontalPodAutoscalers, "
        "PodDisruptionBudgets, and NetworkPolicies. You write reusable Helm charts "
        "with values overrides, chart hooks, and chart tests. You implement GitOps "
        "workflows with ArgoCD including App-of-Apps patterns and sync waves. You "
        "configure Istio for mTLS, canary traffic splitting, and Envoy-based "
        "observability. You always set resource requests/limits, liveness/readiness/"
        "startup probes, and security contexts (non-root UID, read-only rootfs, "
        "dropped capabilities). You apply Pod Security Standards (restricted profile) "
        "and use OPA/Gatekeeper policies for admission control."
    ),
    goal_addendum=(
        "Produce production-grade Kubernetes manifests and Helm charts with proper "
        "resource limits, probes, security contexts, and NetworkPolicies."
    ),
)
