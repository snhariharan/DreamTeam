import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# ── Environment Variables ──────────────────────────────────────────────────
os.environ["OPENAI_API_KEY"]    = os.getenv("OPENAI_API_KEY",    "")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY", "")
os.environ["GOOGLE_API_KEY"]    = os.getenv("GOOGLE_API_KEY",     "")
os.environ["SERPER_API_KEY"]    = os.getenv("SERPER_API_KEY",     "")  # https://serper.dev
os.environ["GITHUB_TOKEN"]      = os.getenv("GITHUB_TOKEN",       "")  # GitHub PAT (repo + copilot scope)
os.environ["BRAVE_API_KEY"]     = os.getenv("BRAVE_API_KEY",      "")  # https://brave.com/search/api/

# GitHub Copilot API endpoint (OpenAI-compatible)
_COPILOT_BASE_URL = "https://api.githubcopilot.com"


# ── Universal LLM factory ──────────────────────────────────────────────────

def get_llm(model: str, temperature: float = 0.1):
    """
    Create an LLM instance from a model name string.

    Provider is resolved automatically by model-name prefix:
      gpt-*, o1-*, o3-*, o4-*      → OpenAI
      claude-*                      → Anthropic
      gemini-*                      → Google Generative AI
      copilot-*, github-copilot*    → GitHub Copilot (OpenAI-compatible)
                                       Requires GITHUB_TOKEN env var with
                                       'copilot' OAuth scope.
      llama*, mistral*, phi*,
        codellama*, deepseek*,
        qwen*, mixtral*, vicuna*,
        orca*, falcon*              → Ollama (local)

    If the prefix is unrecognised, OpenAI is used as the fallback.

    Args:
        model:       Model identifier string (e.g. "gpt-4o",
                     "claude-sonnet-4-5", "copilot-gpt-4o").
        temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative).

    Returns:
        An instantiated LangChain chat model.

    Examples::

        llm = get_llm("gpt-4.1", temperature=0.1)
        llm = get_llm("claude-sonnet-4-5", temperature=0.2)
        llm = get_llm("gemini-2.5-flash")
        llm = get_llm("copilot-gpt-4o")       # GitHub Copilot
        llm = get_llm("qwen2.5-coder:14b")    # Ollama local
    """
    m = model.lower()

    # GitHub Copilot — uses OpenAI-compatible endpoint with a GitHub token
    if any(m.startswith(p) for p in ("copilot-", "github-copilot")):
        github_token = os.getenv("GITHUB_TOKEN", "")
        if not github_token:
            raise ValueError(
                "GITHUB_TOKEN with 'copilot' scope is required for Copilot models. "
                "Create a token at https://github.com/settings/tokens and export it "
                "as GITHUB_TOKEN."
            )
        # Strip the 'copilot-' prefix to get the underlying model name
        underlying = model[len("copilot-"):] if m.startswith("copilot-") else model
        return ChatOpenAI(
            model=underlying,
            temperature=temperature,
            openai_api_key=github_token,
            openai_api_base=_COPILOT_BASE_URL,
        )

    if any(m.startswith(p) for p in ("gpt-", "o1-", "o3-", "o4-")):
        return ChatOpenAI(model=model, temperature=temperature)

    if m.startswith("claude"):
        return ChatAnthropic(model_name=model, temperature=temperature)

    if m.startswith("gemini"):
        return ChatGoogleGenerativeAI(model=model, temperature=temperature)

    _ollama_prefixes = (
        "llama", "mistral", "phi", "codellama", "deepseek",
        "qwen", "mixtral", "vicuna", "orca", "falcon",
    )
    if any(m.startswith(p) for p in _ollama_prefixes):
        try:
            from langchain_ollama import ChatOllama
        except ImportError:
            from langchain_community.chat_models import ChatOllama  # type: ignore
        return ChatOllama(model=model, temperature=temperature)

    # Unknown prefix — fall back to OpenAI
    return ChatOpenAI(model=model, temperature=temperature)


# ── Role-specific lazy getters (used by agents when no profile is supplied) ─

def get_manager_llm():
    """Default manager LLM — Claude Sonnet 4.5 (strong orchestration, lower cost than Opus)."""
    return get_llm("claude-sonnet-4-5", temperature=0.2)


def get_architect_llm():
    """Default architect LLM — Gemini 2.5 Pro (long context for codebase analysis)."""
    return get_llm("gemini-2.5-pro", temperature=0.2)


def get_developer_llm():
    """Default developer LLM — GPT-4.1 (best coding performance in the GPT-4 family)."""
    return get_llm("gpt-4.1", temperature=0.1)


def get_reviewer_llm():
    """Default reviewer LLM — Claude Sonnet 4.5 (sharp analysis, security focus)."""
    return get_llm("claude-sonnet-4-5", temperature=0.1)


def get_default_llm():
    """Default LLM for tester and devops — GPT-4.1-mini (fast, capable, low cost)."""
    return get_llm("gpt-4.1-mini", temperature=0.1)
