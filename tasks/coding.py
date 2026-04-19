"""
Coding Task — assigned to the Senior Developer.

The Developer implements the Architect's plan, reading existing files
before touching them and persisting every change to disk via FileWriterTool.
"""
from crewai import Task


def create_coding_task(developer) -> Task:
    return Task(
        description=(
            "Using the Architect's implementation plan, implement all required "
            "code changes inside {source_directory}.\n\n"
            "Rules:\n"
            "  1. Read every existing file before modifying it.\n"
            "  2. Execute snippets with the CodeInterpreter to validate logic.\n"
            "  3. Use FileWriterTool to persist every new or modified file.\n"
            "  4. Do NOT change files that are not in the implementation plan.\n"
            "  5. Add type hints and docstrings to every new function or class."
        ),
        expected_output=(
            "All source files written to disk. "
            "A concise summary listing each file path and the changes made."
        ),
        agent=developer,
    )
