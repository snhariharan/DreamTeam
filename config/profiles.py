"""
Model Profiles
--------------
Pre-built LLM configurations for each role in the agency.
Pick a profile in agency.py to change the entire team's model lineup.

Available profiles:
  POWER     — Frontier models, best quality, highest cost
  BALANCED  — Strong quality/cost/speed balance (recommended default)
  FAST      — Optimised for speed and low cost, good for iteration
  BUDGET    — Minimum cost models, suitable for experimentation
  LOCAL     — Ollama local models, no API costs, full privacy

Custom profiles:
  Instantiate AgencyProfile directly and pass it to build_and_run_crew().

Usage in agency.py::

    from config.profiles import BALANCED
    PROFILE = BALANCED

    # Or fully custom:
    from config.profiles import AgencyProfile
    PROFILE = AgencyProfile(
        name="custom",
        manager="claude-3-5-sonnet-20241022",
        architect="gemini-1.5-pro",
        developer="gpt-4o",
        reviewer="claude-3-5-sonnet-20241022",
        default="gpt-4o-mini",
    )
"""
from dataclasses import dataclass, field


@dataclass
class AgencyProfile:
    """
    Maps each agent role to a specific LLM model string.

    Model names are resolved to the correct provider by get_llm()
    in config/settings.py using prefix matching.

    Attributes:
        name:         Human-readable label shown in startup output.
        description:  One-line summary of the profile's trade-offs.
        manager:      Model for the hierarchical crew manager.
        architect:    Model for the Solution Architect.
        developer:    Model for the Senior Developer.
        reviewer:     Model for the Principal Reviewer.
        default:      Fallback model for Tester and DevOps.
        temperatures: Optional per-role temperature overrides.
                      Keys: "manager" | "architect" | "developer" |
                            "reviewer" | "tester" | "devops"
    """
    name:         str
    description:  str
    manager:      str
    architect:    str
    developer:    str
    reviewer:     str
    default:      str
    temperatures: dict = field(default_factory=dict)

    def temperature_for(self, role: str) -> float:
        """Return the temperature for a given role, with sensible defaults."""
        defaults = {
            "manager":   0.2,
            "architect": 0.2,
            "developer": 0.1,
            "reviewer":  0.1,
            "tester":    0.1,
            "devops":    0.2,
        }
        return self.temperatures.get(role, defaults.get(role, 0.1))


# ── Pre-built profiles ─────────────────────────────────────────────────────

POWER = AgencyProfile(
    name="power",
    description="Frontier models — maximum quality, highest cost.",
    manager="claude-3-opus-20240229",
    architect="gemini-1.5-pro",
    developer="gpt-4o",
    reviewer="claude-3-5-sonnet-20241022",
    default="gpt-4o",
)

BALANCED = AgencyProfile(
    name="balanced",
    description="Strong quality / cost / speed balance. Recommended default.",
    manager="claude-3-5-sonnet-20241022",
    architect="gemini-1.5-flash",
    developer="gpt-4o",
    reviewer="claude-3-5-sonnet-20241022",
    default="gpt-4o-mini",
)

FAST = AgencyProfile(
    name="fast",
    description="Optimised for speed and low latency. Great for rapid iteration.",
    manager="claude-3-haiku-20240307",
    architect="gemini-1.5-flash",
    developer="gpt-4o-mini",
    reviewer="claude-3-haiku-20240307",
    default="gpt-4o-mini",
)

BUDGET = AgencyProfile(
    name="budget",
    description="Minimum cost. Use for experiments and non-critical tasks.",
    manager="gpt-4o-mini",
    architect="gemini-1.5-flash",
    developer="gpt-4o-mini",
    reviewer="gpt-4o-mini",
    default="gpt-3.5-turbo",
)

# ── Local / Ollama profiles ────────────────────────────────────────────────
# Three tiers based on available GPU / RAM.
# Run `ollama pull <model>` for every model name used in a profile.
#
# Hardware guide:
#   LOCAL_QUALITY  — 32 GB+ RAM / 24 GB+ VRAM  (70B models)
#   LOCAL_BALANCED — 16 GB RAM  / 12 GB VRAM   (14B models)  ← default LOCAL alias
#   LOCAL_FAST     —  8 GB RAM  /  6 GB VRAM   (7B / 3B models)

LOCAL_QUALITY = AgencyProfile(
    name="local_quality",
    description="High-quality Ollama models (70B). Requires 32 GB+ RAM / 24 GB+ VRAM.",
    manager="llama3.1:70b",        # Best reasoning for orchestration
    architect="llama3.1:70b",      # Long-context planning
    developer="qwen2.5-coder:32b", # State-of-the-art local code model
    reviewer="llama3.1:70b",       # Sharp critical analysis
    default="mistral:7b",          # Fast fallback for tester & devops
)

LOCAL_BALANCED = AgencyProfile(
    name="local_balanced",
    description="Balanced Ollama models (14B). Requires 16 GB RAM / 12 GB VRAM.",
    manager="llama3.1:8b",         # Solid orchestration on consumer hardware
    architect="mistral:7b",        # Good reasoning, low memory footprint
    developer="qwen2.5-coder:14b", # Best code model in the 14B class
    reviewer="llama3.1:8b",        # Critical without huge RAM needs
    default="phi3:medium",         # Fast 14B for tester & devops
)

LOCAL_FAST = AgencyProfile(
    name="local_fast",
    description="Fast Ollama models (7B / 3B). Runs on 8 GB RAM / 6 GB VRAM.",
    manager="mistral:7b",          # Quick, capable manager
    architect="mistral:7b",        # Reasonable planner at 7B
    developer="qwen2.5-coder:7b",  # Best 7B code model
    reviewer="mistral:7b",         # Decent reviewer
    default="phi3:mini",           # 3.8B — fastest, lowest RAM
)

# Alias — LOCAL points to the balanced tier (most common laptop setup)
LOCAL = LOCAL_BALANCED

