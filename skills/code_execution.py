"""
Code execution skills
---------------------
Sandboxed code execution is not available as a standalone crewai_tools import
in the current package version. Instead, the developer and tester agents use
a combination of:

  • FileWriterTool  — write a script to disk
  • SerperDevTool   — look up runtime errors or debugging patterns
  • FileReadTool    — read test output files

The crewai `CodeInterpreterTool` is available via the AWS Bedrock toolkit
(crewai_tools.aws.bedrock.code_interpreter) for users on that platform.
For local development, agents are instructed to write code to disk and
describe expected outputs rather than executing live.

This module intentionally exports nothing so imports from other skill
modules remain unchanged. If you add a code execution backend later,
expose it as `run_code` here.
"""

# Placeholder — no cross-platform CodeInterpreterTool in this crewai_tools version.
# Agents that previously used run_code will fall back to FileWriterTool + SerperDevTool.
run_code = None
