"""
Documentation search skills
----------------------------
All tools are exposed as factory functions to avoid eager OPENAI_API_KEY
validation at import time (these tools use OpenAI embeddings for RAG search).

Tools provided:
  CodeDocsSearchTool — semantic search inside inline code documentation
  MDXSearchTool      — search MDX-based documentation sites

Required:
  OPENAI_API_KEY — used for embedding-based search
"""
from crewai_tools import CodeDocsSearchTool, MDXSearchTool


def get_code_docs() -> CodeDocsSearchTool:
    """Semantic search inside code documentation."""
    return CodeDocsSearchTool()


def get_mdx_docs() -> MDXSearchTool:
    """Search MDX-based documentation files or sites."""
    return MDXSearchTool()


# Backwards-compatible aliases.
code_docs = get_code_docs
mdx_docs  = get_mdx_docs
