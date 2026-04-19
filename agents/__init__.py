"""
Agents package
--------------
Factory functions for each team member in the DreamTeam agency.

Each factory accepts an optional `extra_tools` list so that MCP-sourced
tools can be injected at runtime without changing agent definitions.

Usage:
    from agents.architect import create_architect
    agent = create_architect(extra_tools=[some_mcp_tool, ...])
"""
