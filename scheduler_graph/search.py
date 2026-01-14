"""
Define class for web search.
"""

import os
from typing import Any

from tavily import TavilyClient


class SearchClientTavily():
    def __init__(self, api_key: str):
        self.client = TavilyClient(api_key=api_key)
    
    def search(self, query: str) -> dict[str, Any]:
        response = self.client.search(
            query=query,
            max_results=15,
            include_answer=False,
            include_raw_content=False
        )

        return response


class WebSearchClient():
    """
    General client for conducting web searches. Specific service defined as 
    environment variable.
    """

    service_registry = {
        "Tavily": lambda: SearchClientTavily(api_key=os.environ["TAVILY_API_KEY"])
        }

    def __init__(self, service: str):
        self.client = self.service_registry[service]()

    def search(self, query: str) -> dict[str, Any]:
        response = self.client.search(query)

        return response
