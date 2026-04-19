"""
Review Task — assigned to the Principal Code Reviewer.

The Reviewer compares the Developer's code against the original requirements
and writes a PASS / FAIL report to ./review_report.md.
"""
from crewai import Task


def create_review_task(reviewer) -> Task:
    return Task(
        description=(
            "Review the code produced by the Developer against:\n"
            "  • Original requirements in {task_file}\n"
            "  • The Architect's implementation plan\n"
            "  • Existing code conventions in {source_directory}\n\n"
            "Check for:\n"
            "  - Correctness     (does it fulfil the requirements?)\n"
            "  - Security        (no hardcoded secrets, no injection vectors)\n"
            "  - Performance     (no N+1 queries, no blocking I/O in async code)\n"
            "  - Style           (consistent with the existing codebase)\n"
            "  - Edge cases      (missing error handling, None checks, etc.)\n\n"
            "Write the full review report to ./review_report.md."
        ),
        expected_output=(
            "review_report.md saved to disk.\n"
            "Must open with a clear verdict line:\n"
            "  VERDICT: PASS   or   VERDICT: FAIL\n"
            "Followed by specific, line-number-referenced findings."
        ),
        agent=reviewer,
    )
