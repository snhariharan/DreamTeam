"""
Config parsing skills
---------------------
All tools are exposed as factory functions to avoid eager OPENAI_API_KEY
validation at import time (these tools use OpenAI embeddings for RAG search).

Tools provided:
  JSONSearchTool — semantic search inside .json files
  TXTSearchTool  — search plain-text files (including YAML read as text)
  XMLSearchTool  — search .xml configuration and manifest files

Required:
  OPENAI_API_KEY — used for embedding-based search
"""
from crewai_tools import JSONSearchTool, TXTSearchTool, XMLSearchTool


def get_json_search() -> JSONSearchTool:
    """Semantic search inside any .json file."""
    return JSONSearchTool()


def get_txt_search() -> TXTSearchTool:
    """Search plain-text and YAML files (read as text)."""
    return TXTSearchTool()


def get_xml_search() -> XMLSearchTool:
    """Query any .xml configuration or manifest file."""
    return XMLSearchTool()


# Backwards-compatible aliases pointing to the lazy getters.
json_search = get_json_search
txt_search  = get_txt_search
xml_search  = get_xml_search
