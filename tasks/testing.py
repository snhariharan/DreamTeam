"""
Testing Task — assigned to the QA Automation Engineer.

The Tester writes and executes a complete PyTest suite, saving all test
files under {source_directory}/tests/ and confirming they are green.
"""
from crewai import Task


def create_testing_task(tester) -> Task:
    return Task(
        description=(
            "Write and execute a complete test suite for all new or modified "
            "code in {source_directory}/.\n\n"
            "Step 1 — Detect the stack:\n"
            "  Read {source_directory} and the Architect's implementation plan "
            "to identify the primary language and test framework "
            "(e.g. pytest for Python, Jest/Vitest for TypeScript/React, "
            "JUnit 5 for Java/Kotlin, sbt test for Scala, go test for Go).\n\n"
            "Step 2 — Write the tests using the detected framework:\n"
            "  • Happy paths     (expected / normal behaviour)\n"
            "  • Edge cases      (empty inputs, None/null, zero, max values)\n"
            "  • Boundary values (off-by-one, type coercions)\n"
            "  • Expected exceptions / error states\n\n"
            "Rules:\n"
            "  1. Save all test files under {source_directory}/tests/ "
            "(or the conventional location for the detected language).\n"
            "  2. Use fixtures, parametrize / data providers where appropriate.\n"
            "  3. Mock ALL external I/O (network calls, DB queries, filesystem).\n"
            "  4. Execute the tests and confirm every test passes.\n"
            "  5. Write a test summary to ./test_results.md with format:\n"
            "       TEST RESULT: PASS   or   TEST RESULT: FAIL\n"
            "     followed by a table of test name → status."
        ),
        expected_output=(
            "Test files saved to {source_directory}/tests/ (or equivalent).\n"
            "./test_results.md written to disk.\n"
            "Must open with: TEST RESULT: PASS  or  TEST RESULT: FAIL\n"
            "Followed by a table: test name | status."
        ),
        agent=tester,
    )
