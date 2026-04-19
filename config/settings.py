import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# ── Environment Variables ──────────────────────────────────────────────────
os.environ["OPENAI_API_KEY"]    = os.getenv("OPENAI_API_KEY",    "")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY", "")
os.environ["GOOGLE_API_KEY"]    = os.getenv("GOOGLE_API_KEY",     "")
os.environ["SERPER_API_KEY"]    = os.getenv("SERPER_API_KEY",     "")  # https://serper.dev
os.environ["GITHUB_TOKEN"]      = os.getenv("GITHUB_TOKEN",       "")  # GitHub PAT (repo scope)
os.environ["BRAVE_API_KEY"]     = os.getenv("BRAVE_API_KEY",      "")  # https://brave.com/search/api/


# ── Universal LLM factory ──────────────────────────────────────────────────

def get_llm(model: str, temperature: float = 0.1):
    """
    Create an LLM instance from a model name string.

    Provider is resolved automatically by model-name prefix:
      gpt-*, o1-*, o3-*            → OpenAI
      claude-*                     → Anthropic
      gemini-*                     → Google Generative AI
      llama*, mistral*, phi*,
        codellama*, deepseek*,
        qwen*, mixtral*            → Ollama (local)

    If the prefix is unrecognised, OpenAI is used as the fallback.

    Args:
        model:       Model identifier string (e.g. "gpt-4o", "claude-3-5-sonnet-20241022").
        temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative).

    Returns:
        An instantiated LangChain chat model.

    Examples::

        llm = get_llm("gpt-4o", temperature=0.1)
        llm = get_llm("claude-3-5-sonnet-20241022", temperature=0.2)
        llm = get_llm("gemini-1.5-pro")
        llm = get_llm("codellama")          # Ollama local
    """
    m = model.lower()

    if any(m.startswith(p) for p in ("gpt-", "o1-", "o3-", "o4-")):
        return ChatOpenAI(model=model, temperature=temperature)

    if m.startswith("claude"):
        return ChatAnthropic(model_name=model, temperature=temperature)

    if m.startswith("gemini"):
        return ChatGoogleGenerativeAI(model=model, temperature=temperature)

    _ollama_prefixes = (
        "llama", "mistral", "phi", "codellama", "deepseek",
        "qwen", "mixtral", "vicuna", "orca",
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
    """Default manager LLM — Claude Opus."""
    return get_llm("claude-3-opus-20240229", temperature=0.2)


def get_architect_llm():
    """Default architect LLM — Gemini 1.5 Pro."""
    return get_llm("gemini-1.5-pro", temperature=0.2)


def get_developer_llm():
    """Default developer LLM — GPT-4o."""
    return get_llm("gpt-4o", temperature=0.1)


def get_reviewer_llm():
    """Default reviewer LLM — Claude Sonnet."""
    return get_llm("claude-3-5-sonnet-20241022", temperature=0.1)


def get_default_llm():
    """Default LLM for tester and devops — GPT-4o."""
    return get_llm("gpt-4o", temperature=0.1)
