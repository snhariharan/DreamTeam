"""
Web research skills
-------------------
All tools are exposed as factory functions to avoid eager credential
validation at import time. Call the getter inside agent factories
where credentials are guaranteed to be present.

Tools provided:
  SerperDevTool     — Google-powered real-time search (SERPER_API_KEY)
  ScrapeWebsiteTool — Fetch and parse any public URL
  GithubSearchTool  — Semantic GitHub code/issue search (GITHUB_TOKEN)
  WebsiteSearchTool — Targeted in-site semantic search (OPENAI_API_KEY)

Required environment variables:
  SERPER_API_KEY  — https://serper.dev  (free 2 500 searches/month)
  GITHUB_TOKEN    — https://github.com/settings/tokens  (repo scope)
  OPENAI_API_KEY  — used by WebsiteSearchTool for embeddings
"""
import os
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, GithubSearchTool, WebsiteSearchTool


def get_web_search() -> SerperDevTool:
    """Google-powered real-time search via Serper."""
    return SerperDevTool()


def get_web_scrape() -> ScrapeWebsiteTool:
    """Fetch and parse the full content of any URL."""
    return ScrapeWebsiteTool()


def get_github_search() -> GithubSearchTool:
    """Semantic search across GitHub repos (requires GITHUB_TOKEN)."""
    return GithubSearchTool(gh_token=os.getenv("GITHUB_TOKEN", ""))


def get_website_search() -> WebsiteSearchTool:
    """Targeted in-site semantic search (requires OPENAI_API_KEY for embeddings)."""
    return WebsiteSearchTool()


# Backwards-compatible aliases — constructed lazily at agent build time.
# In agent factories, call the getter (e.g. get_web_search()) rather than
# using these names, so that import-time errors are avoided.
web_search    = get_web_search
web_scrape    = get_web_scrape
github_search = get_github_search
