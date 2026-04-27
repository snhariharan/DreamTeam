"""
Terraform / IaC Skill Pack
--------------------------
Gives an agent infrastructure-as-code expertise across all major providers:
  • Terraform (HCL) core language, modules, and state management
  • Terraform Registry — provider and module references
  • OpenTofu (open-source Terraform fork) compatibility
  • Pulumi — SDK-based IaC for Python / TypeScript / Go
  • Terragrunt — DRY configuration wrapper
  • CDK for Terraform (CDKTF) integration patterns

Best for: Cloud DevOps Specialist, Solution Architect
"""
from crewai_tools import ScrapeWebsiteTool

from skills.packs import SkillPack


def _terraform_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://developer.hashicorp.com/terraform/docs"),
        ScrapeWebsiteTool(website_url="https://developer.hashicorp.com/terraform/language"),
        ScrapeWebsiteTool(website_url="https://developer.hashicorp.com/terraform/tutorials/"),
        ScrapeWebsiteTool(website_url="https://registry.terraform.io/"),
        ScrapeWebsiteTool(website_url="https://opentofu.org/docs/"),
        ScrapeWebsiteTool(website_url="https://www.pulumi.com/docs/"),
        ScrapeWebsiteTool(website_url="https://terragrunt.gruntwork.io/docs/"),
    ]


TERRAFORM = SkillPack(
    name="terraform",
    description=(
        "Terraform HCL, Terraform Registry, OpenTofu, Pulumi SDK IaC, "
        "Terragrunt DRY configs, remote state management."
    ),
    tools_factory=_terraform_tools,
    backstory_addendum=(
        "You are a HashiCorp Certified Terraform Associate with extensive IaC "
        "expertise across AWS, GCP, and Azure. You write modular, reusable "
        "Terraform HCL following the standard module structure (main.tf, "
        "variables.tf, outputs.tf, versions.tf). You manage remote state with "
        "S3/GCS/Azure Blob backends and state locking via DynamoDB or equivalent. "
        "You use workspaces for environment isolation, apply least-privilege provider "
        "credentials via OIDC (no long-lived keys), and always run `terraform plan` "
        "before `apply`. You are familiar with Terragrunt for DRY configurations "
        "across environments and Pulumi as an alternative SDK-first approach. "
        "You enforce input variable validation blocks, use `moved` blocks for "
        "safe refactors, and pin provider versions with `~>` constraints. "
        "You write complete resource dependency graphs and avoid hardcoded values."
    ),
    goal_addendum=(
        "Write modular, DRY Terraform HCL with remote state, variable validation, "
        "pinned provider versions, and least-privilege OIDC credentials."
    ),
)
