"""
API Skill Packs
---------------
Expertise for designing and implementing HTTP APIs and GraphQL schemas.

API     — REST, OpenAPI 3.1, HTTP standards, API design guidelines
GRAPHQL — GraphQL schema design, resolvers, DataLoader, Apollo

Best for: Solution Architect, Senior Developer
"""
from crewai_tools import ScrapeWebsiteTool

from skills.packs import SkillPack


def _api_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://swagger.io/specification/"),
        ScrapeWebsiteTool(website_url="https://restfulapi.net/"),
        ScrapeWebsiteTool(website_url="https://httpwg.org/specs/"),
        ScrapeWebsiteTool(website_url="https://json-schema.org/understanding-json-schema/"),
        ScrapeWebsiteTool(website_url="https://www.fastapi.tiangolo.com/"),
    ]


def _graphql_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://graphql.org/learn/"),
        ScrapeWebsiteTool(website_url="https://www.apollographql.com/docs/"),
        ScrapeWebsiteTool(website_url="https://strawberry.rocks/docs/"),
        ScrapeWebsiteTool(website_url="https://relay.dev/docs/"),
    ]


API = SkillPack(
    name="api",
    description="REST API design, OpenAPI 3.1, JSON Schema, HTTP standards.",
    tools_factory=_api_tools,
    backstory_addendum=(
        "You are an API design expert. You design RESTful APIs following "
        "Fielding's architectural constraints, use correct HTTP verbs and "
        "status codes, write OpenAPI 3.1 specs, and implement versioning "
        "strategies (URL path, header, content negotiation). You avoid common "
        "anti-patterns (chatty APIs, excessive nesting, inconsistent naming) "
        "and design APIs that are intuitive, discoverable, and backward-compatible."
    ),
    goal_addendum="Design clean, well-documented REST APIs with OpenAPI 3.1 specs.",
)

GRAPHQL = SkillPack(
    name="graphql",
    description="GraphQL schema design, resolvers, DataLoader, Apollo / Strawberry.",
    tools_factory=_graphql_tools,
    backstory_addendum=(
        "You are a GraphQL specialist. You design schema-first APIs with "
        "clear type hierarchies, implement efficient resolvers using DataLoader "
        "to solve the N+1 problem, and apply cursor-based pagination. You know "
        "the trade-offs between GraphQL and REST, and when to use each. "
        "You are familiar with Strawberry (Python), Apollo Server (JS), "
        "and Federation for micro-services."
    ),
    goal_addendum="Design type-safe GraphQL schemas with efficient resolvers and pagination.",
)
