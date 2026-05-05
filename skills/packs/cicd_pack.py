"""
CI/CD Pipeline Skill Packs
--------------------------
Gives an agent deep expertise in continuous integration and delivery pipelines
across every major platform.

CICD_GITHUB   — GitHub Actions: workflows, reusable actions, environments, secrets
CICD_AZURE    — Azure DevOps Pipelines: YAML, classic, release pipelines, artifacts
CICD_AWS      — AWS CodePipeline / CodeBuild / CodeDeploy: native AWS CI/CD
CICD_JENKINS  — Jenkins: declarative pipelines, Groovy DSL, plugins, shared libraries
CICD_GITLAB   — GitLab CI/CD: .gitlab-ci.yml, runners, environments, packages
CICD_CIRCLE   — CircleCI: orbs, workflows, resource classes, contexts

Best for: Cloud DevOps Specialist
"""
from crewai_tools import ScrapeWebsiteTool

from skills.packs import SkillPack


# ── GitHub Actions ─────────────────────────────────────────────────────────

def _github_actions_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://docs.github.com/en/actions"),
        ScrapeWebsiteTool(website_url="https://docs.github.com/en/actions/using-workflows/reusing-workflows"),
        ScrapeWebsiteTool(website_url="https://docs.github.com/en/actions/security-guides/encrypted-secrets"),
        ScrapeWebsiteTool(website_url="https://github.com/marketplace?type=actions"),
    ]


CICD_GITHUB = SkillPack(
    name="cicd_github",
    description="GitHub Actions: workflows, reusable actions, environments, OIDC, secrets.",
    tools_factory=_github_actions_tools,
    backstory_addendum=(
        "You are an expert in GitHub Actions. You write DRY, reusable workflows "
        "using composite actions and reusable workflow calls. You use OIDC "
        "federated identity to authenticate to cloud providers without storing "
        "long-lived credentials. You set up matrix builds, manual approval gates, "
        "environment-scoped secrets, concurrency controls, and self-hosted runners. "
        "You reference official GitHub Marketplace actions by pinned SHA."
    ),
    goal_addendum="Write production-grade GitHub Actions workflows with OIDC and reusable patterns.",
)


# ── Azure DevOps Pipelines ─────────────────────────────────────────────────

def _azure_devops_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://learn.microsoft.com/en-us/azure/devops/pipelines/"),
        ScrapeWebsiteTool(website_url="https://learn.microsoft.com/en-us/azure/devops/pipelines/yaml-schema/"),
        ScrapeWebsiteTool(website_url="https://learn.microsoft.com/en-us/azure/devops/pipelines/library/"),
        ScrapeWebsiteTool(website_url="https://learn.microsoft.com/en-us/azure/devops/artifacts/"),
    ]


CICD_AZURE = SkillPack(
    name="cicd_azure",
    description="Azure DevOps Pipelines: YAML schema, stages, environments, artifacts, variable groups.",
    tools_factory=_azure_devops_tools,
    backstory_addendum=(
        "You are an expert in Azure DevOps Pipelines. You author multi-stage YAML "
        "pipelines with deployment jobs, environments, and approval gates. You "
        "configure variable groups backed by Azure Key Vault, use service connections "
        "for cloud deployments, publish to Azure Artifacts feeds, and implement "
        "blue/green and rolling update strategies. You know both YAML and classic "
        "release pipelines and can migrate between them."
    ),
    goal_addendum="Write multi-stage Azure DevOps YAML pipelines with approval gates and Key Vault integration.",
)


# ── AWS CodePipeline / CodeBuild / CodeDeploy ──────────────────────────────

def _aws_codepipeline_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://docs.aws.amazon.com/codepipeline/"),
        ScrapeWebsiteTool(website_url="https://docs.aws.amazon.com/codebuild/"),
        ScrapeWebsiteTool(website_url="https://docs.aws.amazon.com/codedeploy/"),
        ScrapeWebsiteTool(website_url="https://docs.aws.amazon.com/codeartifact/"),
    ]


CICD_AWS = SkillPack(
    name="cicd_aws",
    description="AWS CodePipeline, CodeBuild, CodeDeploy, CodeArtifact — native AWS CI/CD.",
    tools_factory=_aws_codepipeline_tools,
    backstory_addendum=(
        "You are an expert in the AWS Developer Tools suite. You build pipelines "
        "using CodePipeline (source → build → test → deploy stages), write "
        "buildspec.yml for CodeBuild, configure CodeDeploy appspec.yml for "
        "EC2/ECS/Lambda blue-green deployments, and publish artifacts to "
        "CodeArtifact. You use IAM roles with least-privilege access, encrypt "
        "pipeline artifacts with KMS, and trigger pipelines from S3, GitHub, "
        "or CodeCommit source actions."
    ),
    goal_addendum="Build AWS-native CI/CD pipelines using CodePipeline, CodeBuild, and CodeDeploy.",
)


# ── Jenkins ───────────────────────────────────────────────────────────────

def _jenkins_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://www.jenkins.io/doc/book/pipeline/"),
        ScrapeWebsiteTool(website_url="https://www.jenkins.io/doc/book/pipeline/shared-libraries/"),
        ScrapeWebsiteTool(website_url="https://www.jenkins.io/doc/pipeline/steps/"),
        ScrapeWebsiteTool(website_url="https://plugins.jenkins.io/"),
    ]


CICD_JENKINS = SkillPack(
    name="cicd_jenkins",
    description="Jenkins declarative pipelines, Groovy DSL, shared libraries, plugin ecosystem.",
    tools_factory=_jenkins_tools,
    backstory_addendum=(
        "You are a Jenkins expert with deep knowledge of Declarative and Scripted "
        "Pipeline syntax. You write Jenkinsfiles using stages, agents, post conditions, "
        "and parallel execution. You build shared libraries in Groovy to eliminate "
        "duplication across pipelines. You configure credentials securely using "
        "Jenkins Credentials Store, use the Blue Ocean UI for visibility, and "
        "integrate with Docker, Kubernetes agents, SonarQube, and Nexus. You "
        "migrate legacy freestyle jobs to modern declarative pipelines."
    ),
    goal_addendum="Write Declarative Jenkinsfiles using shared libraries and secure credentials management.",
)


# ── GitLab CI/CD ──────────────────────────────────────────────────────────

def _gitlab_ci_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://docs.gitlab.com/ee/ci/"),
        ScrapeWebsiteTool(website_url="https://docs.gitlab.com/ee/ci/yaml/"),
        ScrapeWebsiteTool(website_url="https://docs.gitlab.com/ee/ci/runners/"),
        ScrapeWebsiteTool(website_url="https://docs.gitlab.com/ee/user/packages/"),
    ]


CICD_GITLAB = SkillPack(
    name="cicd_gitlab",
    description="GitLab CI/CD: .gitlab-ci.yml, runners, environments, packages, DAST/SAST.",
    tools_factory=_gitlab_ci_tools,
    backstory_addendum=(
        "You are an expert in GitLab CI/CD. You write .gitlab-ci.yml files using "
        "stages, rules, needs (DAG), environments, and protected variables. You "
        "configure GitLab Runners (shared, group, and project-level) with Docker "
        "or Kubernetes executors. You use GitLab Packages for container and package "
        "registry, Auto DevOps for convention-driven pipelines, and built-in SAST, "
        "DAST, and dependency scanning templates."
    ),
    goal_addendum="Write .gitlab-ci.yml pipelines using DAG needs, environments, and built-in security scans.",
)


# ── CircleCI ──────────────────────────────────────────────────────────────

def _circleci_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://circleci.com/docs/"),
        ScrapeWebsiteTool(website_url="https://circleci.com/docs/configuration-reference/"),
        ScrapeWebsiteTool(website_url="https://circleci.com/developer/orbs"),
    ]


CICD_CIRCLE = SkillPack(
    name="cicd_circle",
    description="CircleCI: orbs, workflows, resource classes, contexts, test splitting.",
    tools_factory=_circleci_tools,
    backstory_addendum=(
        "You are a CircleCI expert. You write config.yml files using workflows, "
        "jobs, and orbs for DRY reusable pipeline components. You optimise build "
        "times using parallelism, test splitting, and intelligent layer caching. "
        "You scope secrets to contexts, use resource classes matching workload "
        "requirements, and set up approval jobs for production deployments."
    ),
    goal_addendum="Write CircleCI config.yml using orbs, contexts, and parallelism for fast builds.",
)
