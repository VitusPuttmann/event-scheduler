"""
Tools for the LangGraph application.
"""

import os
import time

from tavily import TavilyClient

from langchain_core.tools import tool


class ToolLimiter:
    def __init__(self, max_calls: int = 1):
        self.remaining = max_calls

    def allow(self) -> bool:
        if self.remaining <= 0:
            return False
        
        self.remaining -= 1
        
        return True


limiter = ToolLimiter(max_calls=3)


@tool
def search_web(url: str) -> str:
    """
    Web search for event details subpages via Tavily.
    """
    
    if not limiter.allow():
        return ""


    client = TavilyClient(os.environ["TAVILY_API_KEY"])
    
    response = client.search(
        query=url,
        max_results=1,
        include_answer=False,
        include_raw_content=True,
    )

    print("--------------------")    # LOCAL DEBUDDING MESSAGE - REMOVE
    print("----- WEB SEARCH EXECUTED")    # LOCAL DEBUDDING MESSAGE - REMOVE
    print("--------------------")    # LOCAL DEBUDDING MESSAGE - REMOVE

    time.sleep(5)

    result = "".join(
        entry["raw_content"]
        for entry in response["results"]
        if "raw_content" in entry
    )

    return result
