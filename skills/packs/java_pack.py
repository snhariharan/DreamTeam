"""
Java, Kotlin & Scala Skill Packs
---------------------------------
Gives an agent deep JVM-ecosystem expertise.

JAVA:   Java 21 LTS, Spring Boot 3, Spring Cloud, Maven/Gradle, Quarkus, JUnit 5
KOTLIN: Kotlin 2.x, Ktor, Coroutines, Exposed ORM, kotlinx.serialization, Gradle DSL
SCALA:  Scala 3, Cats Effect / ZIO functional programming, Akka / Pekko, sbt

Best for: Senior Developer, QA Automation Engineer, Solution Architect
"""
from crewai_tools import ScrapeWebsiteTool

from skills.packs import SkillPack


# ── Java ──────────────────────────────────────────────────────────────────

def _java_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://docs.oracle.com/en/java/javase/21/"),
        ScrapeWebsiteTool(website_url="https://central.sonatype.com/"),
        ScrapeWebsiteTool(website_url="https://docs.spring.io/spring-boot/docs/current/reference/html/"),
        ScrapeWebsiteTool(website_url="https://spring.io/projects/spring-cloud"),
        ScrapeWebsiteTool(website_url="https://maven.apache.org/guides/"),
        ScrapeWebsiteTool(website_url="https://docs.gradle.org/current/userguide/userguide.html"),
        ScrapeWebsiteTool(website_url="https://junit.org/junit5/docs/current/user-guide/"),
        ScrapeWebsiteTool(website_url="https://quarkus.io/guides/"),
        ScrapeWebsiteTool(website_url="https://www.baeldung.com/"),
    ]


JAVA = SkillPack(
    name="java",
    description=(
        "Java 21 LTS, Spring Boot 3, Spring Cloud (Config, Gateway, Feign, "
        "Resilience4j), Quarkus native, Maven/Gradle, JUnit 5 / Mockito / "
        "Testcontainers."
    ),
    tools_factory=_java_tools,
    backstory_addendum=(
        "You are an expert Java 21 engineer. You leverage modern JVM features: "
        "virtual threads (Project Loom) for high-throughput non-blocking I/O, "
        "records and sealed classes for immutable domain modelling, pattern "
        "matching in switch expressions, and text blocks. You build cloud-native "
        "microservices with Spring Boot 3: auto-configuration, Spring Data JPA / "
        "R2DBC, Spring Security with OAuth 2.0/OIDC, Spring Actuator for health "
        "endpoints, and Spring Cloud for distributed system concerns — Config "
        "Server, Gateway (reactive), OpenFeign clients, and Circuit Breaker with "
        "Resilience4j. For ultra-low startup times you use Quarkus with GraalVM "
        "native image compilation. You build with Maven multi-module projects or "
        "Gradle convention plugins for DRY build logic. You write unit tests with "
        "JUnit 5 and Mockito, integration tests with Testcontainers (real DB in "
        "Docker per test run), and mutation tests with PIT."
    ),
    goal_addendum=(
        "Apply Java 21 (virtual threads, records, sealed classes), Spring Boot 3 "
        "/ Spring Cloud microservices, and Testcontainers integration tests."
    ),
)


# ── Kotlin ────────────────────────────────────────────────────────────────

def _kotlin_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://kotlinlang.org/docs/"),
        ScrapeWebsiteTool(website_url="https://ktor.io/docs/"),
        ScrapeWebsiteTool(website_url="https://docs.gradle.org/current/userguide/userguide.html"),
        ScrapeWebsiteTool(website_url="https://kotlinlang.org/docs/coroutines-guide.html"),
        ScrapeWebsiteTool(website_url="https://github.com/JetBrains/Exposed"),
        ScrapeWebsiteTool(website_url="https://kotlin.github.io/kotlinx.serialization/"),
    ]


KOTLIN = SkillPack(
    name="kotlin",
    description=(
        "Kotlin 2.x, Ktor async HTTP server, Coroutines / Flow, "
        "Exposed ORM, kotlinx.serialization, Gradle Kotlin DSL."
    ),
    tools_factory=_kotlin_tools,
    backstory_addendum=(
        "You are an expert Kotlin 2.x engineer. You write idiomatic Kotlin: "
        "null-safe code without !!, data classes and value classes for domain "
        "modelling, sealed hierarchies for exhaustive when expressions, extension "
        "functions for clean DSL APIs, and structured coroutines (suspend "
        "functions, Flow, channels) for async code without callback hell. You "
        "build HTTP services with Ktor (routing DSL, content negotiation, "
        "authentication plugins), query databases with Exposed ORM, and "
        "serialise data with kotlinx.serialization. You use Gradle with the "
        "Kotlin DSL (build.gradle.kts) and version catalogs (libs.versions.toml). "
        "You also work with Spring Boot when the team uses it, treating "
        "Kotlin null safety and coroutines as first-class in that context."
    ),
    goal_addendum=(
        "Write idiomatic Kotlin 2.x: null safety, coroutines/Flow, "
        "Ktor HTTP services, Exposed ORM, Gradle Kotlin DSL."
    ),
)


# ── Scala ─────────────────────────────────────────────────────────────────

def _scala_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://docs.scala-lang.org/"),
        ScrapeWebsiteTool(website_url="https://scala3book.com/"),
        ScrapeWebsiteTool(website_url="https://typelevel.org/cats/"),
        ScrapeWebsiteTool(website_url="https://zio.dev/overview/getting-started"),
        ScrapeWebsiteTool(website_url="https://doc.akka.io/docs/akka/current/"),
        ScrapeWebsiteTool(website_url="https://www.scala-sbt.org/1.x/docs/"),
    ]


SCALA = SkillPack(
    name="scala",
    description=(
        "Scala 3, Cats / Cats Effect functional IO, ZIO 2 structured concurrency, "
        "Akka / Pekko actors and streams, sbt."
    ),
    tools_factory=_scala_tools,
    backstory_addendum=(
        "You are a Scala 3 engineer skilled in both OOP and pure functional "
        "programming. You use Scala 3 features: enums, opaque types, extension "
        "methods, given/using instances, and union/intersection types. You write "
        "type-safe functional code with Cats and Cats Effect for referentially "
        "transparent IO, Resource management, and concurrent primitives "
        "(Ref, Deferred, Semaphore). For greenfield services you prefer ZIO 2 "
        "for structured concurrency, ZLayer dependency injection, and built-in "
        "observability. For actor-based distributed systems you use Akka / Pekko "
        "(clustering, persistence, streams, HTTP). You build with sbt and publish "
        "artefacts to Sonatype Central or GitHub Packages."
    ),
    goal_addendum=(
        "Write Scala 3 with Cats Effect or ZIO 2 for type-safe functional IO, "
        "proper resource management, and structured concurrency."
    ),
)
