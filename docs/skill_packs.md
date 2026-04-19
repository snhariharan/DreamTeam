# Skill Packs Reference

Skill packs are domain-specific bundles that extend any agent with:
- **Documentation tools** — pre-configured scrapers pointing at official docs
- **Backstory expertise** — domain knowledge injected into the agent's prompt

Mix and match packs freely across agents.

---

## Import

```python
from skills.packs import (
    # Language
    PYTHON, JAVA, KOTLIN, NODEJS, TYPESCRIPT, RUST, GO,
    # Cloud
    CLOUD_AWS, CLOUD_GCP, CLOUD_AZURE,
    # Data
    DATABASE, NOSQL,
    # Design
    API, GRAPHQL,
    # Quality
    SECURITY, TESTING,
)
```

---

## Language Packs

### `PYTHON`
**Best for:** Senior Developer, QA Tester

| Item | Detail |
|---|---|
| Documentation | Python 3 official docs, PyPI, PEPs, Real Python |
| Expertise | PEP 8 / 257, type hints (PEP 484), idiomatic Python |
| Key libraries | FastAPI, SQLAlchemy, Pydantic, pytest, NumPy, Pandas |

```python
"developer": [PYTHON]
"tester":    [TESTING, PYTHON]
```

---

### `JAVA`
**Best for:** Senior Developer, QA Tester

| Item | Detail |
|---|---|
| Documentation | Oracle Java SE docs, Maven Central, Spring, JUnit 5 |
| Expertise | SOLID, Clean Code, modern Java (records, sealed, pattern matching, virtual threads) |
| Key libraries | Spring Boot, Hibernate, Jackson, JUnit 5, Mockito |

```python
"developer": [JAVA]
```

---

### `KOTLIN`
**Best for:** Senior Developer

| Item | Detail |
|---|---|
| Documentation | Kotlin official docs, Ktor, Gradle, Coroutines guide |
| Expertise | Null safety, data classes, sealed classes, extension functions, coroutines |
| Key libraries | Ktor, Kotlinx.serialization, Coroutines |

```python
"developer": [KOTLIN]
```

---

### `NODEJS`
**Best for:** Senior Developer

| Item | Detail |
|---|---|
| Documentation | Node.js official docs, npm registry, Fastify, Express |
| Expertise | Event loop, non-blocking I/O, streams, async/await, ESM |
| Key frameworks | Fastify, Express, NestJS |

```python
"developer": [NODEJS]
```

---

### `TYPESCRIPT`
**Best for:** Senior Developer, Principal Reviewer

| Item | Detail |
|---|---|
| Documentation | TypeScript official docs, tsconfig reference, type challenges |
| Expertise | Strict mode, generics, utility types, no `any` |

```python
"developer": [NODEJS, TYPESCRIPT]
```

---

### `RUST`
**Best for:** Senior Developer

| Item | Detail |
|---|---|
| Documentation | The Rust Book, docs.rs, Tokio tutorial, Actix-web docs |
| Expertise | Ownership, borrowing, lifetimes, Result/Option, zero-cost abstractions |
| Key libraries | Tokio, Actix-web, Serde, Clap |

```python
"developer": [RUST]
```

---

### `GO`
**Best for:** Senior Developer

| Item | Detail |
|---|---|
| Documentation | Go official docs, pkg.go.dev, Go blog, Gin docs |
| Expertise | Goroutines, channels, explicit errors, table-driven tests, small focused packages |
| Key frameworks | Gin, Echo, standard `net/http` |

```python
"developer": [GO]
```

---

## Cloud Packs

### `CLOUD_AWS`
**Best for:** Solution Architect, Cloud DevOps Specialist

| Item | Detail |
|---|---|
| Documentation | AWS docs, CDK v2 guide, Terraform AWS provider, Well-Architected Framework, AWS Blog |
| Expertise | AWS Solutions Architect Professional, EC2/ECS/EKS/Lambda/S3/RDS/DynamoDB/SQS/SNS/CloudFront/IAM/VPC/CDK |
| IaC | Terraform, CDK |

```python
"architect": [CLOUD_AWS, API]
"devops":    [CLOUD_AWS]
```

---

### `CLOUD_GCP`
**Best for:** Solution Architect, Cloud DevOps Specialist

| Item | Detail |
|---|---|
| Documentation | GCP docs, GCP Architecture Centre, Terraform GCP provider, GCP Blog |
| Expertise | GCP Professional Cloud Architect, GKE/Cloud Run/Cloud Functions/BigQuery/Pub-Sub/Spanner/Vertex AI |
| IaC | Terraform, Deployment Manager |

```python
"architect": [CLOUD_GCP]
```

---

### `CLOUD_AZURE`
**Best for:** Solution Architect, Cloud DevOps Specialist

| Item | Detail |
|---|---|
| Documentation | Azure Learn docs, Azure Architecture Centre, Terraform AzureRM, Azure SDK blog |
| Expertise | Azure Solutions Architect Expert, AKS/Functions/App Service/Cosmos DB/Service Bus/Entra ID/Key Vault |
| IaC | Terraform (AzureRM), Bicep |

```python
"architect": [CLOUD_AZURE]
"devops":    [CLOUD_AZURE]
```

---

## Data Packs

### `DATABASE`
**Best for:** Senior Developer, Solution Architect

| Item | Detail |
|---|---|
| Documentation | PostgreSQL docs, MySQL docs, SQLAlchemy docs, Alembic, Prisma |
| Expertise | Schema normalisation, indexing, EXPLAIN ANALYZE, migrations, connection pooling |
| Key ORMs | SQLAlchemy, Prisma, Peewee |

```python
"developer": [PYTHON, DATABASE]
```

---

### `NOSQL`
**Best for:** Senior Developer, Solution Architect

| Item | Detail |
|---|---|
| Documentation | MongoDB docs, Redis docs, DynamoDB docs, Cassandra docs, Elasticsearch guide |
| Expertise | Document / key-value / wide-column / search store selection, access-pattern modelling, eventual consistency |

```python
"developer": [DATABASE, NOSQL]
```

---

## Design Packs

### `API`
**Best for:** Solution Architect, Senior Developer

| Item | Detail |
|---|---|
| Documentation | OpenAPI 3.1 spec, RESTful API guidelines, HTTP spec, JSON Schema, FastAPI docs |
| Expertise | REST constraints, correct HTTP verbs/status codes, API versioning, OpenAPI 3.1 |

```python
"architect": [CLOUD_AWS, API]
"developer": [PYTHON, API]
```

---

### `GRAPHQL`
**Best for:** Solution Architect, Senior Developer

| Item | Detail |
|---|---|
| Documentation | GraphQL Learn, Apollo docs, Strawberry docs, Relay docs |
| Expertise | Schema-first design, DataLoader (N+1 prevention), cursor-based pagination, Federation |

```python
"architect": [GRAPHQL]
"developer": [PYTHON, GRAPHQL]
```

---

## Quality Packs

### `SECURITY`
**Best for:** Principal Reviewer, Solution Architect

| Item | Detail |
|---|---|
| Documentation | OWASP Top 10, OWASP Cheat Sheet Series, NVD CVE database, SANS white papers, CWE definitions |
| Expertise | Injection, broken auth, SSRF, XSS, path traversal, hardcoded secrets, least-privilege |

```python
"reviewer": [SECURITY]
```

---

### `TESTING`
**Best for:** QA Automation Engineer, Senior Developer

| Item | Detail |
|---|---|
| Documentation | pytest docs, Hypothesis docs, `unittest.mock` docs, Test Pyramid article, TestDriven.io |
| Expertise | Test pyramid, pytest fixtures, `@pytest.mark.parametrize`, Hypothesis property-based testing, test doubles |

```python
"tester": [TESTING, PYTHON]
```

---

## Creating a custom skill pack

```python
# skills/packs/my_pack.py
from crewai_tools import ScrapeWebsiteTool
from skills.packs import SkillPack

def _my_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://docs.my-framework.com/"),
        ScrapeWebsiteTool(website_url="https://api.my-framework.com/"),
    ]

MY_FRAMEWORK = SkillPack(
    name="my_framework",
    description="My framework docs and API reference.",
    tools_factory=_my_tools,
    backstory_addendum=(
        "You are an expert in My Framework. You know its architecture, "
        "best practices, and common pitfalls."
    ),
    goal_addendum="Apply My Framework idioms and design patterns throughout.",
)
```

Then in `agency.py`:
```python
from skills.packs.my_pack import MY_FRAMEWORK
SKILL_ASSIGNMENTS = {"developer": [PYTHON, MY_FRAMEWORK]}
```

See **[extending.md](extending.md)** for more.
