"""
MCP Server parameter definitions
---------------------------------
Each constant is a StdioServerParameters object that describes how to
launch a specific MCP server as a child subprocess via npx.

Available servers
-----------------
GITHUB_SERVER        — repo operations, PR/issue management, code search
BRAVE_SEARCH_SERVER  — privacy-respecting real-time web search
FILESYSTEM_SERVER    — advanced file traversal and bulk file operations

Prerequisites
-------------
  • Node.js ≥ 18 installed  (https://nodejs.org)
  • npm packages are auto-installed on first use via `npx -y`
  • Set environment variables:
      GITHUB_TOKEN    — https://github.com/settings/tokens  (repo scope)
      BRAVE_API_KEY   — https://brave.com/search/api/  (free tier available)
"""
import os
from mcp import StdioServerParameters

# ── GitHub MCP ────────────────────────────────────────────────────────────────
# Source:  https://github.com/modelcontextprotocol/servers/tree/main/src/github
#
# Key tools provided:
#   list_repos, get_file_contents, create_or_update_file, search_repositories,
#   search_code, search_issues, create_pull_request, get_issue, list_commits
#
# Used by: Architect, Developer, Reviewer, Tester
GITHUB_SERVER = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-github"],
    env={
        **os.environ,
        "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN", ""),
    },
)

# ── Brave Search MCP ──────────────────────────────────────────────────────────
# Source:  https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search
#
# Key tools provided:
#   brave_web_search, brave_local_search
#
# Used by: Architect, Reviewer, DevOps
BRAVE_SEARCH_SERVER = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-brave-search"],
    env={
        **os.environ,
        "BRAVE_API_KEY": os.getenv("BRAVE_API_KEY", ""),
    },
)

# ── Filesystem MCP ────────────────────────────────────────────────────────────
# Source:  https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem
#
# Key tools provided:
#   read_file, read_multiple_files, write_file, edit_file, create_directory,
#   list_directory, directory_tree, move_file, search_files, get_file_info
#
# The "." argument restricts access to the current working directory (safe).
#
# Used by: Developer, DevOps
FILESYSTEM_SERVER = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "."],
    env=os.environ.copy(),
)
