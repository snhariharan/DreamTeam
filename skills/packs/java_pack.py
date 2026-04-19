"""
Java & Kotlin Skill Packs
--------------------------
Gives an agent deep JVM-ecosystem expertise.

JAVA:   Java SE / EE docs, Maven Central, Spring Framework.
KOTLIN: Kotlin docs, Gradle, Ktor, Coroutines.

Best for: Senior Developer, QA Tester
"""
from crewai_tools import ScrapeWebsiteTool

from skills.packs import SkillPack


def _java_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://docs.oracle.com/en/java/"),
        ScrapeWebsiteTool(website_url="https://central.sonatype.com/"),
        ScrapeWebsiteTool(website_url="https://spring.io/docs"),
        ScrapeWebsiteTool(website_url="https://maven.apache.org/guides/"),
        ScrapeWebsiteTool(website_url="https://junit.org/junit5/docs/current/user-guide/"),
    ]


def _kotlin_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://kotlinlang.org/docs/"),
        ScrapeWebsiteTool(website_url="https://ktor.io/docs/"),
        ScrapeWebsiteTool(website_url="https://gradle.org/guides/"),
        ScrapeWebsiteTool(website_url="https://kotlinlang.org/docs/coroutines-guide.html"),
    ]


JAVA = SkillPack(
    name="java",
    description="Java SE/EE docs, Spring, Maven, JUnit expertise.",
    tools_factory=_java_tools,
    backstory_addendum=(
        "You are an expert Java engineer with deep knowledge of the JVM, "
        "Java SE and EE APIs, Spring Boot, Maven/Gradle build systems, and "
        "JUnit 5 testing. You follow Clean Code and SOLID principles, prefer "
        "immutable data, and use modern Java features (records, sealed classes, "
        "pattern matching, streams, and virtual threads from Project Loom)."
    ),
    goal_addendum="Apply Java best practices: SOLID, Clean Code, modern Java features.",
)

KOTLIN = SkillPack(
    name="kotlin",
    description="Kotlin docs, Ktor, Gradle, and Coroutines expertise.",
    tools_factory=_kotlin_tools,
    backstory_addendum=(
        "You are an expert Kotlin engineer. You write idiomatic Kotlin: "
        "leveraging null safety, data classes, sealed classes, extension "
        "functions, and coroutines for structured concurrency. You are "
        "familiar with Ktor for server-side development and Kotlinx.serialization."
    ),
    goal_addendum="Write idiomatic Kotlin with null safety and coroutines.",
)
