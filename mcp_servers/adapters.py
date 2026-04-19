"""
MCP Adapter utilities
---------------------
Manages the lifecycle of MCP server subprocesses and distributes their
tools to agents by role name.

Each MCP server runs as a Node.js child process launched via npx.
All servers are started before any agent is created and shut down
cleanly when the crew finishes (via ExitStack).

Servers that fail to start are silently skipped — the agency degrades
gracefully when Node.js is unavailable or API keys are missing.

Tool-role mapping
-----------------
  GitHub MCP       → architect, developer, reviewer, tester
  Brave Search MCP → architect, reviewer, devops
  Filesystem MCP   → developer, devops
"""
from contextlib import ExitStack

from crewai_tools import MCPServerAdapter

from mcp_servers.servers import GITHUB_SERVER, BRAVE_SEARCH_SERVER, FILESYSTEM_SERVER


def _safe_attach(stack: ExitStack, server_params, label: str) -> list:
    """
    Try to start an MCP server inside an ExitStack context.

    Returns the server's tool list on success, or an empty list if the
    server cannot be reached (missing Node.js, bad API key, etc.).

    Args:
        stack:         Active ExitStack to register the adapter lifetime.
        server_params: StdioServerParameters describing the MCP server.
        label:         Human-readable name used in console output.
    """
    try:
        adapter = stack.enter_context(MCPServerAdapter(server_params))
        tools = list(adapter.tools)
        print(f"  ✅  {label}: {len(tools)} tool(s) loaded")
        return tools
    except Exception as exc:
        print(f"  ⚠️   {label}: skipped — {exc}")
        return []


def run_with_mcp_tools(callback):
    """
    Start all configured MCP servers, distribute their tools by role,
    then invoke ``callback(tools_by_role)``.

    All server subprocesses are shut down on exit — whether the callback
    succeeds or raises an exception.

    Args:
        callback: A callable that receives ``tools_by_role`` (dict[str, list])
                  and returns the crew result.  The crew *must* be kicked off
                  inside this callback while the MCP processes are still alive.

    Role keys in tools_by_role:
        "architect", "developer", "reviewer", "tester", "devops"

    Returns:
        Whatever ``callback`` returns (typically the crew's final result).

    Example::

        def run(mcp_tools):
            architect = create_architect(extra_tools=mcp_tools["architect"])
            ...
            return crew.kickoff(inputs=inputs)

        result = run_with_mcp_tools(run)
    """
    print("\n🔌 Connecting to MCP servers...")

    with ExitStack() as stack:
        # ── Start servers ────────────────────────────────────────────────────
        github_tools = _safe_attach(stack, GITHUB_SERVER,       "GitHub MCP      ")
        brave_tools  = _safe_attach(stack, BRAVE_SEARCH_SERVER, "Brave Search MCP")
        fs_tools     = _safe_attach(stack, FILESYSTEM_SERVER,   "Filesystem MCP  ")

        # ── Distribute tools by role ─────────────────────────────────────────
        tools_by_role: dict[str, list] = {
            # Research patterns, find reference implementations, read library source
            "architect": [*github_tools, *brave_tools],
            # Look up library examples, read external code, bulk file operations
            "developer": [*github_tools, *fs_tools],
            # Check PRs, verify security advisories, CVE research
            "reviewer":  [*github_tools, *brave_tools],
            # Find test patterns used in similar open-source projects
            "tester":    [*github_tools],
            # Cloud provider docs, security announcements, monorepo traversal
            "devops":    [*brave_tools, *fs_tools],
        }

        total = sum(len(v) for v in tools_by_role.values())
        print(f"🔌 MCP ready — {total} tool slot(s) distributed across roles\n")

        return callback(tools_by_role)
