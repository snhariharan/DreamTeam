"""
Security Skill Pack
--------------------
Gives an agent application security expertise:
  • OWASP Top 10 vulnerabilities
  • NIST Cybersecurity Framework
  • CVE / NVD advisory database
  • SANS secure coding guidelines

Best for: Principal Reviewer, Solution Architect
"""
from crewai_tools import ScrapeWebsiteTool

from skills.packs import SkillPack


def _security_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://owasp.org/www-project-top-ten/"),
        ScrapeWebsiteTool(website_url="https://cheatsheetseries.owasp.org/"),
        ScrapeWebsiteTool(website_url="https://nvd.nist.gov/vuln/search"),
        ScrapeWebsiteTool(website_url="https://www.sans.org/white-papers/"),
        ScrapeWebsiteTool(website_url="https://cwe.mitre.org/data/definitions/"),
    ]


SECURITY = SkillPack(
    name="security",
    description="OWASP Top 10, CVE/NVD, SANS secure coding, CWE references.",
    tools_factory=_security_tools,
    backstory_addendum=(
        "You are an application security expert (CISSP / CEH certified). "
        "You know the OWASP Top 10 by heart: injection, broken auth, "
        "sensitive data exposure, XXE, broken access control, security "
        "misconfiguration, XSS, insecure deserialization, known vulnerabilities, "
        "insufficient logging. You scan code for: hardcoded secrets, SQL injection, "
        "path traversal, SSRF, insecure direct object references, and missing "
        "input validation. You recommend mitigations using the principle of "
        "least privilege, defense in depth, and secure-by-default settings."
    ),
    goal_addendum=(
        "Perform a security-focused review: check for OWASP Top 10 issues, "
        "hardcoded secrets, and missing input validation."
    ),
)
