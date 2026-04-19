"""
MCP Servers package
-------------------
Configures and manages connections to Model Context Protocol (MCP) servers
that extend agents with external capabilities beyond the built-in crewai tools.

Bundled servers:
  • GitHub MCP      — repository operations, PR / issue management
  • Brave Search    — privacy-respecting real-time web search
  • Filesystem MCP  — advanced file traversal for large monorepos

Prerequisites:
  • Node.js ≥ 18  (https://nodejs.org)  — MCP servers launch via npx
  • Set these environment variables:
      GITHUB_TOKEN    — https://github.com/settings/tokens  (repo scope)
      BRAVE_API_KEY   — https://brave.com/search/api/  (free tier available)
"""
