"""
Deployment Task — assigned to the Cloud DevOps Specialist.

The DevOps engineer writes a Dockerfile, docker-compose.yml, and a GitHub
Actions CI/CD pipeline to the project root.
"""
from crewai import Task


def create_deployment_task(devops) -> Task:
    return Task(
        description=(
            "Inspect {source_directory} and produce three production-ready files:\n\n"
            "1. **Dockerfile** (multi-stage, minimise final image size)\n"
            "   - Stage 1 (builder) : install deps, run tests\n"
            "   - Stage 2 (runtime) : copy only the artefacts needed\n"
            "   - Add a HEALTHCHECK instruction\n"
            "   - Run as a non-root user\n\n"
            "2. **docker-compose.yml** (local development)\n"
            "   - App service + any required backing services (DB, cache)\n"
            "   - Inject all secrets via environment variables\n"
            "   - Include volume mounts for hot-reload\n\n"
            "3. **.github/workflows/deploy.yml** (CI/CD pipeline)\n"
            "   - Trigger: push to main\n"
            "   - Steps: checkout → lint → test → build image → push to registry → deploy\n"
            "   - Use GitHub Actions secrets for all credentials\n"
            "   - Add a manual approval gate before production deploy\n\n"
            "Save all three files to the project root."
        ),
        expected_output=(
            "Three files written to disk:\n"
            "  • Dockerfile\n"
            "  • docker-compose.yml\n"
            "  • .github/workflows/deploy.yml\n"
            "Each file must be production-ready and include inline comments."
        ),
        agent=devops,
    )
