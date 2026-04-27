"""
Skill Packs
-----------
Domain-specific skill bundles that can be mixed into any agent at runtime.

Each SkillPack contains:
  • tools_factory  — lazy callable returning a list of BaseTool instances
  • backstory_addendum — domain expertise injected into the agent's backstory
  • goal_addendum      — extra goal text for the agent

Usage::

    from skills.packs import PYTHON, JAVA, CLOUD_AWS, DATABASE, SECURITY, API, TESTING
    from skills.packs import CLOUD_GCP, CLOUD_AZURE, KOTLIN, NODEJS, RUST, GO

    developer = create_developer(skill_packs=[PYTHON, DATABASE])
    architect = create_architect(skill_packs=[CLOUD_AWS, API])
    reviewer  = create_reviewer (skill_packs=[SECURITY])
    tester    = create_tester   (skill_packs=[TESTING, PYTHON])
    devops    = create_devops   (skill_packs=[CLOUD_AWS])

Registry
--------
Import individual packs by name from this module.
To build a custom pack, instantiate SkillPack directly.
"""
from dataclasses import dataclass, field
from typing import Callable, List


@dataclass
class SkillPack:
    """
    A named bundle of domain-specific tools and backstory context.

    Attributes:
        name:               Short identifier used in logs (e.g. "python").
        description:        One-line description of what this pack adds.
        tools_factory:      A zero-arg callable that returns list[BaseTool].
                            Keep lazy (don't call at module load) to avoid
                            eager credential validation.
        backstory_addendum: Text appended to the agent backstory to communicate
                            domain expertise to the LLM.
        goal_addendum:      Optional text appended to the agent goal.
    """
    name:               str
    description:        str
    tools_factory:      Callable[[], list]
    backstory_addendum: str = ""
    goal_addendum:      str = ""

    def get_tools(self) -> list:
        """Instantiate and return all tools in this pack."""
        return self.tools_factory()

    def __repr__(self) -> str:
        return f"SkillPack({self.name!r})"


# ── Re-export all packs for convenient one-line imports ─────────────────────

from skills.packs.python_pack       import PYTHON                             # noqa: E402
from skills.packs.java_pack         import JAVA, KOTLIN, SCALA                # noqa: E402
from skills.packs.cloud_pack        import CLOUD_AWS, CLOUD_GCP, CLOUD_AZURE  # noqa: E402
from skills.packs.database_pack     import DATABASE, NOSQL                    # noqa: E402
from skills.packs.security_pack     import SECURITY                           # noqa: E402
from skills.packs.api_pack          import API, GRAPHQL                       # noqa: E402
from skills.packs.testing_pack      import TESTING                            # noqa: E402
from skills.packs.language_pack     import NODEJS, RUST, GO, TYPESCRIPT       # noqa: E402
from skills.packs.frontend_pack     import REACT, ANGULAR                     # noqa: E402
from skills.packs.kubernetes_pack   import KUBERNETES                         # noqa: E402
from skills.packs.terraform_pack    import TERRAFORM                          # noqa: E402
from skills.packs.observability_pack import OBSERVABILITY                     # noqa: E402
from skills.packs.docker_pack       import DOCKER                             # noqa: E402

__all__ = [
    "SkillPack",
    # Language packs — backend
    "PYTHON", "JAVA", "KOTLIN", "SCALA",
    "NODEJS", "TYPESCRIPT", "RUST", "GO",
    # Language packs — frontend
    "REACT", "ANGULAR",
    # Cloud provider packs
    "CLOUD_AWS", "CLOUD_GCP", "CLOUD_AZURE",
    # Data packs
    "DATABASE", "NOSQL",
    # Quality packs
    "SECURITY", "TESTING",
    # Design packs
    "API", "GRAPHQL",
    # Infrastructure / platform packs
    "DOCKER", "KUBERNETES", "TERRAFORM", "OBSERVABILITY",
]
