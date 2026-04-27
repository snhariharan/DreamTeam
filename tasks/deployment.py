"""
Deployment Task — assigned to the Cloud DevOps Specialist.

The DevOps engineer detects the deployment target from the Architect's plan
and writes the appropriate production-ready delivery artefacts to disk.
"""
from crewai import Task


def create_deployment_task(devops) -> Task:
    return Task(
        description=(
            "Read the Architect's implementation plan to determine the "
            "deployment target, then produce the appropriate production-ready "
            "delivery artefacts.\n\n"
            "If the deployment target is Docker / containerised service:\n"
            "  1. Dockerfile (multi-stage)\n"
            "     - Stage 1 (builder): install deps, compile, run unit tests\n"
            "     - Stage 2 (runtime): copy only the artefacts needed\n"
            "     - HEALTHCHECK instruction and non-root user\n"
            "  2. docker-compose.yml — app + required backing services\n"
            "     - Secrets via environment variables, hot-reload volume mounts\n\n"
            "If the deployment target is Kubernetes / Helm:\n"
            "  1. Helm chart under ./charts/<app-name>/\n"
            "     - deployment.yaml, service.yaml, ingress.yaml, hpa.yaml\n"
            "     - values.yaml with sensible defaults\n"
            "  2. kustomize overlay for staging + production if appropriate\n\n"
            "If the deployment target is Terraform / IaC:\n"
            "  1. Terraform module under ./infra/\n"
            "     - main.tf, variables.tf, outputs.tf, versions.tf\n"
            "     - Remote state backend block (S3+DynamoDB / GCS / Azure Blob)\n\n"
            "For all targets — also produce a CI/CD pipeline:\n"
            "  .github/workflows/deploy.yml\n"
            "  - Trigger: push to main\n"
            "  - Steps: checkout → lint → test → build → push/plan → deploy\n"
            "  - GitHub Actions secrets for all credentials\n"
            "  - Manual approval gate before production deploy\n\n"
            "Save all artefacts to the project root or conventional subdirectories."
        ),
        expected_output=(
            "Delivery artefacts written to disk appropriate for the detected "
            "deployment target (Docker + Compose, Helm chart, or Terraform module) "
            "plus .github/workflows/deploy.yml.\n"
            "Each file must be production-ready with inline comments."
        ),
        agent=devops,
    )

