"""
Cloud Skill Packs
-----------------
Gives an agent deep cloud provider expertise for AWS, GCP, and Azure.

CLOUD_AWS   — Amazon Web Services: EC2, S3, Lambda, RDS, EKS, IAM, CDK
CLOUD_GCP   — Google Cloud Platform: GKE, Cloud Run, BigQuery, Pub/Sub, Vertex AI
CLOUD_AZURE — Microsoft Azure: AKS, Functions, Cosmos DB, Azure DevOps, Entra ID

Best for: Solution Architect, Cloud DevOps Specialist
"""
from crewai_tools import ScrapeWebsiteTool

from skills.packs import SkillPack


# ── AWS ───────────────────────────────────────────────────────────────────

def _aws_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://docs.aws.amazon.com/"),
        ScrapeWebsiteTool(website_url="https://docs.aws.amazon.com/cdk/v2/guide/"),
        ScrapeWebsiteTool(website_url="https://registry.terraform.io/providers/hashicorp/aws/"),
        ScrapeWebsiteTool(website_url="https://aws.amazon.com/architecture/well-architected/"),
        ScrapeWebsiteTool(website_url="https://aws.amazon.com/blogs/aws/"),
        ScrapeWebsiteTool(website_url="https://docs.aws.amazon.com/eks/latest/userguide/"),
        ScrapeWebsiteTool(website_url="https://docs.aws.amazon.com/lambda/latest/dg/"),
        ScrapeWebsiteTool(website_url="https://docs.aws.amazon.com/IAM/latest/UserGuide/"),
    ]


CLOUD_AWS = SkillPack(
    name="cloud_aws",
    description=(
        "AWS docs, CDK v2, Terraform AWS provider, Well-Architected Framework, "
        "EKS, Lambda, IAM least-privilege."
    ),
    tools_factory=_aws_tools,
    backstory_addendum=(
        "You hold AWS Solutions Architect Professional and DevOps Engineer Professional "
        "certifications. You design cost-optimised, highly available architectures using "
        "AWS-native services: EC2/ECS/EKS, Lambda, S3, RDS/Aurora, DynamoDB, "
        "SQS/SNS/EventBridge, CloudFront, Route53, IAM, VPC, and AWS CDK v2 / "
        "CloudFormation. You apply all five pillars of the AWS Well-Architected Framework. "
        "You write Terraform for infrastructure-as-code, pin provider versions, use "
        "remote state in S3+DynamoDB, and apply OIDC for keyless CI/CD credentials. "
        "You enforce least-privilege IAM policies, enable GuardDuty/SecurityHub, use "
        "AWS Secrets Manager (never plain env vars), and apply SCPs in AWS Organizations."
    ),
    goal_addendum=(
        "Design AWS-native solutions following the Well-Architected Framework with "
        "least-privilege IAM, Terraform IaC, and OIDC-based CI/CD credentials."
    ),
)


# ── GCP ───────────────────────────────────────────────────────────────────

def _gcp_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://cloud.google.com/docs"),
        ScrapeWebsiteTool(website_url="https://cloud.google.com/architecture"),
        ScrapeWebsiteTool(website_url="https://registry.terraform.io/providers/hashicorp/google/"),
        ScrapeWebsiteTool(website_url="https://cloud.google.com/blog/"),
        ScrapeWebsiteTool(website_url="https://cloud.google.com/kubernetes-engine/docs"),
        ScrapeWebsiteTool(website_url="https://cloud.google.com/run/docs"),
        ScrapeWebsiteTool(website_url="https://cloud.google.com/iam/docs"),
    ]


CLOUD_GCP = SkillPack(
    name="cloud_gcp",
    description=(
        "GCP docs, GKE, Cloud Run, Vertex AI, BigQuery, Pub/Sub, "
        "Terraform GCP provider, Workload Identity Federation."
    ),
    tools_factory=_gcp_tools,
    backstory_addendum=(
        "You are a GCP Professional Cloud Architect and DevOps Engineer. You design "
        "solutions using GKE Autopilot, Cloud Run, Cloud Functions 2nd gen, "
        "BigQuery, Pub/Sub, Spanner, Firestore, Vertex AI, and Cloud IAM. "
        "You use Terraform (google provider) or Google Cloud Deployment Manager for "
        "infrastructure-as-code, and Cloud Build or GitHub Actions with Workload "
        "Identity Federation (no service account keys) for CI/CD. You structure "
        "projects with a resource hierarchy (org → folders → projects), apply "
        "VPC Service Controls for data exfiltration prevention, use Binary "
        "Authorization for container image verification, and follow Google Cloud's "
        "security foundations blueprint."
    ),
    goal_addendum=(
        "Design GCP-native solutions following Google Cloud architecture best "
        "practices with Workload Identity Federation and VPC Service Controls."
    ),
)


# ── Azure ─────────────────────────────────────────────────────────────────

def _azure_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://learn.microsoft.com/en-us/azure/"),
        ScrapeWebsiteTool(website_url="https://learn.microsoft.com/en-us/azure/architecture/"),
        ScrapeWebsiteTool(website_url="https://registry.terraform.io/providers/hashicorp/azurerm/"),
        ScrapeWebsiteTool(website_url="https://devblogs.microsoft.com/azure-sdk/"),
        ScrapeWebsiteTool(website_url="https://learn.microsoft.com/en-us/azure/aks/"),
        ScrapeWebsiteTool(website_url="https://learn.microsoft.com/en-us/azure/azure-functions/"),
        ScrapeWebsiteTool(website_url="https://learn.microsoft.com/en-us/azure/key-vault/"),
        ScrapeWebsiteTool(website_url="https://learn.microsoft.com/en-us/security/benchmark/azure/"),
    ]


CLOUD_AZURE = SkillPack(
    name="cloud_azure",
    description=(
        "Azure docs, AKS, Functions, Cosmos DB, Key Vault, Entra ID, "
        "Terraform AzureRM, Azure Security Benchmark, Managed Identity."
    ),
    tools_factory=_azure_tools,
    backstory_addendum=(
        "You are a Microsoft Certified Azure Solutions Architect Expert and "
        "DevOps Engineer Expert. You design solutions using AKS, Azure Functions, "
        "Container Apps, App Service, Azure SQL / Cosmos DB, Service Bus / "
        "Event Hubs, API Management, Azure CDN / Front Door, Entra ID (OIDC / "
        "OAuth 2.0), Key Vault, and Azure Monitor / Log Analytics. You use Terraform "
        "(AzureRM provider) or Bicep for infrastructure-as-code. You enforce "
        "Managed Identity (no client secrets), Azure RBAC least privilege, private "
        "endpoints for all data services, customer-managed keys in Key Vault, and "
        "Microsoft Defender for Cloud recommendations. You follow the Azure "
        "Well-Architected Framework and the Azure Security Benchmark."
    ),
    goal_addendum=(
        "Design Azure-native solutions with Managed Identity, private endpoints, "
        "Key Vault secrets, and Terraform IaC following the Azure Well-Architected "
        "Framework."
    ),
)
