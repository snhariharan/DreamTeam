"""
Testing Skill Pack
------------------
Expertise for writing professional automated test suites:
  • pytest best practices, fixtures, and parametrize
  • Hypothesis property-based testing
  • Test doubles: mocking, stubbing, faking
  • TDD / BDD methodologies

Best for: QA Automation Engineer, Senior Developer
"""
from crewai_tools import ScrapeWebsiteTool

from skills.packs import SkillPack


def _testing_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://docs.pytest.org/en/stable/"),
        ScrapeWebsiteTool(website_url="https://hypothesis.readthedocs.io/en/latest/"),
        ScrapeWebsiteTool(website_url="https://docs.python.org/3/library/unittest.mock.html"),
        ScrapeWebsiteTool(website_url="https://martinfowler.com/articles/practical-test-pyramid.html"),
        ScrapeWebsiteTool(website_url="https://testdriven.io/blog/"),
    ]


TESTING = SkillPack(
    name="testing",
    description="pytest, Hypothesis, test doubles, TDD/BDD, test pyramid.",
    tools_factory=_testing_tools,
    backstory_addendum=(
        "You are a testing expert who follows the test pyramid: many unit tests, "
        "fewer integration tests, minimal end-to-end tests. You write pytest "
        "suites using fixtures, conftest.py, and @pytest.mark.parametrize. "
        "You use Hypothesis for property-based testing of edge cases. For test "
        "doubles, you prefer fakes over mocks, and only mock at system boundaries "
        "(network, database, filesystem). You practice TDD (red-green-refactor) "
        "and know the difference between test isolation and test coverage."
    ),
    goal_addendum=(
        "Write tests following the test pyramid: unit tests first, then integration, "
        "then e2e. Use pytest fixtures and Hypothesis for edge cases."
    ),
)
