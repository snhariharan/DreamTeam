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
    ]


CLOUD_AWS = SkillPack(
    name="cloud_aws",
    description="AWS docs, CDK, Terraform AWS provider, Well-Architected Framework.",
    tools_factory=_aws_tools,
    backstory_addendum=(
        "You hold AWS Solutions Architect Professional and DevOps Engineer "
        "Professional certifications. You design cost-optimised, highly available "
        "architectures using AWS-native services: EC2, ECS/EKS, Lambda, S3, RDS, "
        "DynamoDB, SQS/SNS, CloudFront, IAM, VPC, and CloudFormation/CDK. "
        "You apply the AWS Well-Architected Framework (operational excellence, "
        "security, reliability, performance, cost). You write Terraform for "
        "infrastructure-as-code."
    ),
    goal_addendum="Design AWS-native solutions following the Well-Architected Framework.",
)


# ── GCP ───────────────────────────────────────────────────────────────────

def _gcp_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://cloud.google.com/docs"),
        ScrapeWebsiteTool(website_url="https://cloud.google.com/architecture"),
        ScrapeWebsiteTool(website_url="https://registry.terraform.io/providers/hashicorp/google/"),
        ScrapeWebsiteTool(website_url="https://cloud.google.com/blog/"),
    ]


CLOUD_GCP = SkillPack(
    name="cloud_gcp",
    description="GCP docs, GKE, Vertex AI, BigQuery, Terraform GCP provider.",
    tools_factory=_gcp_tools,
    backstory_addendum=(
        "You are a GCP Professional Cloud Architect. You design solutions using "
        "GKE, Cloud Run, Cloud Functions, BigQuery, Pub/Sub, Spanner, Firestore, "
        "Vertex AI, and Cloud IAM. You use Terraform or Deployment Manager for "
        "infrastructure-as-code. You follow Google's architecture centre best "
        "practices and apply resource hierarchy, VPC design, and IAM least privilege."
    ),
    goal_addendum="Design GCP-native solutions following Google Cloud architecture best practices.",
)


# ── Azure ─────────────────────────────────────────────────────────────────

def _azure_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://learn.microsoft.com/en-us/azure/"),
        ScrapeWebsiteTool(website_url="https://learn.microsoft.com/en-us/azure/architecture/"),
        ScrapeWebsiteTool(website_url="https://registry.terraform.io/providers/hashicorp/azurerm/"),
        ScrapeWebsiteTool(website_url="https://devblogs.microsoft.com/azure-sdk/"),
    ]


CLOUD_AZURE = SkillPack(
    name="cloud_azure",
    description="Azure docs, AKS, Azure DevOps, Terraform AzureRM provider.",
    tools_factory=_azure_tools,
    backstory_addendum=(
        "You are a Microsoft Certified Azure Solutions Architect Expert. "
        "You design solutions using AKS, Azure Functions, App Service, "
        "Azure SQL, Cosmos DB, Service Bus, Azure DevOps, Entra ID (AAD), "
        "Key Vault, and Azure Monitor. You use Terraform (AzureRM) or Bicep "
        "for infrastructure-as-code, and Azure DevOps or GitHub Actions for CI/CD. "
        "You follow the Azure Well-Architected Framework pillars."
    ),
    goal_addendum="Design Azure-native solutions following the Azure Well-Architected Framework.",
)
