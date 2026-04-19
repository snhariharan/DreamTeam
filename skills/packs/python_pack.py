"""
Python Skill Pack
-----------------
Gives an agent deep Python expertise:
  • Python 3 official documentation
  • PyPI package index browsing
  • PEP index (language proposals and standards)
  • Real-world Python patterns via GitHub

Best for: Senior Developer, QA Tester
"""
from crewai_tools import ScrapeWebsiteTool

from skills.packs import SkillPack


def _python_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://docs.python.org/3/"),
        ScrapeWebsiteTool(website_url="https://pypi.org/"),
        ScrapeWebsiteTool(website_url="https://peps.python.org/"),
        ScrapeWebsiteTool(website_url="https://realpython.com/"),
    ]


PYTHON = SkillPack(
    name="python",
    description="Python 3 docs, PyPI, PEPs, and best practices.",
    tools_factory=_python_tools,
    backstory_addendum=(
        "You are an expert Python 3 engineer. You know the standard library "
        "inside-out, follow PEP 8 / PEP 257 style, and use type hints "
        "(PEP 484) everywhere. You prefer idiomatic Python: list comprehensions, "
        "context managers, dataclasses, and async/await over callbacks. "
        "You are familiar with popular libraries: FastAPI, SQLAlchemy, Pydantic, "
        "pytest, and the scientific stack (NumPy, Pandas)."
    ),
    goal_addendum="Apply Python best practices (PEP 8, type hints, idiomatic patterns) throughout.",
)
