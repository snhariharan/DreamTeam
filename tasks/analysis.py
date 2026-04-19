"""
Analysis Task — assigned to the Solution Architect.

The Architect reads the task list and the existing codebase, researches
any required libraries or APIs, and produces a detailed implementation plan.
"""
from crewai import Task


def create_analysis_task(architect) -> Task:
    return Task(
        description=(
            "Read the task list at {task_file}.\n"
            "Explore the entire codebase in {source_directory}.\n"
            "Research any external libraries or APIs that will be needed.\n\n"
            "Produce a detailed technical implementation plan covering:\n"
            "  • Files to create or modify (with full relative paths)\n"
            "  • New function / class signatures with type hints\n"
            "  • Data model changes (schemas, DB migrations)\n"
            "  • External dependencies to add (package name + version)\n"
            "  • Potential risks and suggested mitigations"
        ),
        expected_output=(
            "A Markdown implementation plan with these sections:\n"
            "## Summary\n"
            "## Files to Change\n"
            "## New Functions / Classes\n"
            "## Data Model Changes\n"
            "## Dependencies\n"
            "## Risks & Mitigations"
        ),
        agent=architect,
    )
