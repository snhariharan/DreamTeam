"""
Fix Task — assigned to the Senior Developer.

Used during the review-retry cycle when the Reviewer returns VERDICT: FAIL.
The Developer reads the specific findings and applies targeted corrections
without rewriting unrelated code.
"""
from crewai import Task


def create_fix_task(developer) -> Task:
    return Task(
        description=(
            "Read ./review_report.md carefully.\n"
            "The previous review returned VERDICT: FAIL with specific findings.\n\n"
            "For every finding listed in the report:\n"
            "  1. Identify the exact file path and line number(s) referenced.\n"
            "  2. Read the current content of that file.\n"
            "  3. Apply the minimal, surgical fix that directly addresses the finding.\n"
            "  4. Write only the corrected file(s) back to disk.\n\n"
            "Rules:\n"
            "  • Do NOT modify files that had no findings.\n"
            "  • Do NOT change logic that was not explicitly flagged.\n"
            "  • Do NOT add new features — fix only what was flagged.\n"
            "  • Re-read every file before writing to avoid overwriting "
            "    changes made by another agent."
        ),
        expected_output=(
            "A concise fix summary with one entry per finding:\n"
            "  • Finding: <original finding text>\n"
            "  • File: <path>\n"
            "  • Fix: <one-sentence description of the correction made>\n"
            "Followed by a list of every file written to disk."
        ),
        agent=developer,
    )
