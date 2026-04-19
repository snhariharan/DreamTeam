"""
Testing Task — assigned to the QA Automation Engineer.

The Tester writes and executes a complete PyTest suite, saving all test
files under {source_directory}/tests/ and confirming they are green.
"""
from crewai import Task


def create_testing_task(tester) -> Task:
    return Task(
        description=(
            "Write a complete PyTest suite for all new or modified code "
            "in {source_directory}/.\n\n"
            "Cover:\n"
            "  • Happy paths     (expected / normal behaviour)\n"
            "  • Edge cases      (empty inputs, None, zero, max values)\n"
            "  • Boundary values (off-by-one, type coercions)\n"
            "  • Expected exceptions (ValueError, HTTPException, etc.)\n\n"
            "Rules:\n"
            "  1. Save all test files under {source_directory}/tests/.\n"
            "  2. Use pytest fixtures and @pytest.mark.parametrize where appropriate.\n"
            "  3. Mock ALL external I/O (network calls, DB queries, filesystem ops).\n"
            "  4. Execute the tests via CodeInterpreter and confirm every test passes."
        ),
        expected_output=(
            "PyTest files saved to {source_directory}/tests/. "
            "A final summary listing every test name and its PASS status."
        ),
        agent=tester,
    )
