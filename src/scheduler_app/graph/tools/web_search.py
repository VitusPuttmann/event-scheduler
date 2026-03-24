"""
Tools for searching the web.
"""

from langchain_core.tools import tool

from scheduler_app.infra.tavily import tavily_search
from scheduler_app.utils.rate_limit import limiter


@tool
def search_web(query: str) -> str:
    """
    Web search via Tavily.
    """

    if not limiter.allow():
        return ""

    return tavily_search(query=query, max_results=1)
