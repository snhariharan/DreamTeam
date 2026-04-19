import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# ── Environment Variables ──────────────────────────────────────────────────
os.environ["OPENAI_API_KEY"]    = os.getenv("OPENAI_API_KEY",    "")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY", "")
os.environ["GOOGLE_API_KEY"]    = os.getenv("GOOGLE_API_KEY",     "")
os.environ["SERPER_API_KEY"]    = os.getenv("SERPER_API_KEY",     "")  # https://serper.dev
os.environ["GITHUB_TOKEN"]      = os.getenv("GITHUB_TOKEN",       "")  # PAT: repo + models:read (Copilot Pro gets higher limits)
os.environ["BRAVE_API_KEY"]     = os.getenv("BRAVE_API_KEY",      "")  # https://brave.com/search/api/

# GitHub Models — OpenAI-compatible endpoint backed by a GitHub PAT
# Supports GPT-4o, Claude, Gemini, Llama, Mistral, Phi, and more
# Requires GITHUB_TOKEN with `models:read` scope (Copilot Pro subscribers get higher rate limits)
_GITHUB_MODELS_ENDPOINT = "https://models.github.ai/inference"
_GITHUB_MODELS_TOKEN    = os.getenv("GITHUB_TOKEN", "")


# ── Universal LLM factory ──────────────────────────────────────────────────

def get_llm(model: str, temperature: float = 0.1):
    """
    Create an LLM instance from a model name string.

    Provider is resolved automatically by model-name prefix:

      gh:<model>                   → GitHub Models API  (OpenAI-compat, uses GITHUB_TOKEN)
                                     e.g. "gh:gpt-4o", "gh:claude-3-7-sonnet-20250219",
                                          "gh:meta-llama/Llama-3.3-70B-Instruct"
      gpt-*, o1-*, o3-*, o4-*     → OpenAI
      claude-*                     → Anthropic
      gemini-*                     → Google Generative AI
      llama*, mistral*, phi*,
        codellama*, deepseek*,
        qwen*, mixtral*, vicuna*,
        orca*, falcon*              → Ollama (local)

    If the prefix is unrecognised, OpenAI is used as the fallback.

    Args:
        model:       Model identifier string (e.g. "gpt-4.1",
                     "claude-sonnet-4-5", "gh:gpt-4o").
        temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative).

    Returns:
        An instantiated LangChain chat model.

    Examples::

        llm = get_llm("gpt-4.1", temperature=0.1)
        llm = get_llm("claude-sonnet-4-5", temperature=0.2)
        llm = get_llm("gemini-2.5-flash")
        llm = get_llm("codellama")                      # Ollama local
        llm = get_llm("gh:gpt-4o")                     # GitHub Models
        llm = get_llm("gh:claude-3-7-sonnet-20250219") # GitHub Models — Claude via Copilot
    """
    m = model.lower()

    # ── GitHub Models (prefix "gh:") ─────────────────────────────────────────
    # All models on the GitHub Models catalogue are served through an
    # OpenAI-compatible endpoint authenticated with a GITHUB_TOKEN.
    # Copilot Pro subscribers enjoy higher rate limits than free-tier users.
    if m.startswith("gh:"):
        model_id = model[3:]   # strip the "gh:" prefix
        return ChatOpenAI(
            model=model_id,
            base_url=_GITHUB_MODELS_ENDPOINT,
            api_key=_GITHUB_MODELS_TOKEN or "none",  # must be non-empty string
            temperature=temperature,
        )

    # ── OpenAI ────────────────────────────────────────────────────────────────
    if any(m.startswith(p) for p in ("gpt-", "o1-", "o3-", "o4-", "o1", "o3")):
        return ChatOpenAI(model=model, temperature=temperature)

    # ── Anthropic ─────────────────────────────────────────────────────────────
    if m.startswith("claude"):
        return ChatAnthropic(model_name=model, temperature=temperature)

    # ── Google ────────────────────────────────────────────────────────────────
    if m.startswith("gemini"):
        return ChatGoogleGenerativeAI(model=model, temperature=temperature)

    # ── Ollama (local) ────────────────────────────────────────────────────────
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

    # ── Unknown prefix → OpenAI fallback ─────────────────────────────────────
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
