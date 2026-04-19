"""
Language Skill Packs — Node.js / TypeScript, Rust, Go
------------------------------------------------------
Additional server-side language skill packs for polyglot teams.

NODEJS     — Node.js runtime, npm ecosystem, Express / Fastify
TYPESCRIPT — TypeScript type system, tsconfig, utility types
RUST       — Rust ownership model, Tokio, Actix-web, Cargo
GO         — Go idioms, goroutines, net/http, database/sql

Best for: Senior Developer, Solution Architect
"""
from crewai_tools import ScrapeWebsiteTool

from skills.packs import SkillPack


# ── Node.js ───────────────────────────────────────────────────────────────

def _nodejs_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://nodejs.org/en/docs/"),
        ScrapeWebsiteTool(website_url="https://www.npmjs.com/"),
        ScrapeWebsiteTool(website_url="https://fastify.dev/docs/"),
        ScrapeWebsiteTool(website_url="https://expressjs.com/en/guide/"),
    ]


NODEJS = SkillPack(
    name="nodejs",
    description="Node.js runtime, npm ecosystem, Express, Fastify.",
    tools_factory=_nodejs_tools,
    backstory_addendum=(
        "You are a Node.js expert. You understand the event loop, "
        "non-blocking I/O, streams, and the npm ecosystem. You write "
        "async/await code without callback hell, use Fastify or Express "
        "for HTTP servers, and manage dependencies with care for security "
        "and bundle size. You prefer ESM over CommonJS in modern projects."
    ),
    goal_addendum="Write modern Node.js with async/await, ESM, and proper error handling.",
)


# ── TypeScript ────────────────────────────────────────────────────────────

def _typescript_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://www.typescriptlang.org/docs/"),
        ScrapeWebsiteTool(website_url="https://www.typescriptlang.org/tsconfig/"),
        ScrapeWebsiteTool(website_url="https://github.com/type-challenges/type-challenges"),
    ]


TYPESCRIPT = SkillPack(
    name="typescript",
    description="TypeScript strict mode, utility types, tsconfig best practices.",
    tools_factory=_typescript_tools,
    backstory_addendum=(
        "You are a TypeScript expert. You always use strict mode, write "
        "precise generic types, and leverage utility types (Partial, Readonly, "
        "Pick, Omit, ReturnType, Parameters). You avoid `any` and prefer "
        "type guards and discriminated unions. You structure tsconfig.json "
        "for maximum type safety and optimal build performance."
    ),
    goal_addendum="Use TypeScript strict mode, precise generics, and no `any` types.",
)


# ── Rust ──────────────────────────────────────────────────────────────────

def _rust_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://doc.rust-lang.org/book/"),
        ScrapeWebsiteTool(website_url="https://docs.rs/"),
        ScrapeWebsiteTool(website_url="https://tokio.rs/tokio/tutorial"),
        ScrapeWebsiteTool(website_url="https://actix.rs/docs/"),
    ]


RUST = SkillPack(
    name="rust",
    description="Rust ownership, Tokio async runtime, Actix-web, Cargo.",
    tools_factory=_rust_tools,
    backstory_addendum=(
        "You are a Rust engineer who deeply understands ownership, borrowing, "
        "and lifetimes. You write zero-cost abstraction code with Result/Option "
        "error handling (no panics in library code), use Tokio for async I/O, "
        "and Actix-web for HTTP services. You are comfortable with trait objects, "
        "iterators, macros, and Cargo workspaces."
    ),
    goal_addendum="Write safe, zero-cost Rust with proper ownership and Result error handling.",
)


# ── Go ────────────────────────────────────────────────────────────────────

def _go_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://go.dev/doc/"),
        ScrapeWebsiteTool(website_url="https://pkg.go.dev/"),
        ScrapeWebsiteTool(website_url="https://go.dev/blog/"),
        ScrapeWebsiteTool(website_url="https://github.com/gin-gonic/gin"),
    ]


GO = SkillPack(
    name="go",
    description="Go idioms, goroutines, net/http, pkg.go.dev, Gin framework.",
    tools_factory=_go_tools,
    backstory_addendum=(
        "You are a Go engineer who writes simple, readable, idiomatic Go. "
        "You use goroutines and channels for concurrency (never raw mutexes "
        "unless necessary), handle errors explicitly (no panics in libraries), "
        "and structure code into small, focused packages. You use the standard "
        "library `net/http` or Gin for HTTP services and write table-driven tests."
    ),
    goal_addendum="Write idiomatic Go: explicit errors, goroutines, table-driven tests.",
)
