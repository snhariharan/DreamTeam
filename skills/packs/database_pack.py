"""
Database Skill Packs
--------------------
Domain expertise for relational and NoSQL databases.

DATABASE — PostgreSQL, MySQL, SQLite, SQLAlchemy, migrations
NOSQL    — MongoDB, Redis, DynamoDB, Cassandra, data modelling

Best for: Senior Developer, Solution Architect
"""
from crewai_tools import ScrapeWebsiteTool

from skills.packs import SkillPack


def _database_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://www.postgresql.org/docs/"),
        ScrapeWebsiteTool(website_url="https://dev.mysql.com/doc/"),
        ScrapeWebsiteTool(website_url="https://docs.sqlalchemy.org/"),
        ScrapeWebsiteTool(website_url="https://alembic.sqlalchemy.org/en/latest/"),
        ScrapeWebsiteTool(website_url="https://www.prisma.io/docs/"),
    ]


def _nosql_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://www.mongodb.com/docs/"),
        ScrapeWebsiteTool(website_url="https://redis.io/docs/"),
        ScrapeWebsiteTool(website_url="https://docs.aws.amazon.com/amazondynamodb/"),
        ScrapeWebsiteTool(website_url="https://cassandra.apache.org/doc/"),
        ScrapeWebsiteTool(website_url="https://www.elastic.co/guide/"),
    ]


DATABASE = SkillPack(
    name="database",
    description="PostgreSQL, MySQL, SQLAlchemy, Alembic, Prisma expertise.",
    tools_factory=_database_tools,
    backstory_addendum=(
        "You are a database expert with deep knowledge of relational databases "
        "(PostgreSQL, MySQL, SQLite). You design normalised schemas, write "
        "efficient SQL with proper indexing, and use SQLAlchemy or Prisma ORM "
        "for type-safe queries. You manage schema migrations with Alembic or "
        "Flyway, and understand transaction isolation levels, connection pooling, "
        "and query plan analysis (EXPLAIN ANALYZE)."
    ),
    goal_addendum="Design efficient, normalised database schemas with proper indexing and migrations.",
)

NOSQL = SkillPack(
    name="nosql",
    description="MongoDB, Redis, DynamoDB, Cassandra, Elasticsearch expertise.",
    tools_factory=_nosql_tools,
    backstory_addendum=(
        "You are a NoSQL database specialist. You choose the right store for "
        "the use case: document (MongoDB), key-value/cache (Redis), wide-column "
        "(Cassandra), managed key-value at scale (DynamoDB), or full-text search "
        "(Elasticsearch). You design data models for each store's access patterns, "
        "handle eventual consistency, and configure appropriate indexes and TTLs."
    ),
    goal_addendum="Choose the appropriate NoSQL store and model data for its access patterns.",
)
