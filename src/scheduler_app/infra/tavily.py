"""
Tavily client.
"""

import os
import time
from typing import Optional

from tavily import TavilyClient


def tavily_search(
    query: str,
    *,
    max_results: int = 1,
    include_answer: bool = False,
    include_raw_content: bool = True,
    sleep_seconds: float = 5.0,
    api_key: Optional[str] = None
) -> str:
    client = TavilyClient(api_key or os.environ["TAVILY_API_KEY"])

    try:
        response = client.search(
            query=query,
            max_results=max_results,
            include_answer=include_answer,
            include_raw_content=include_raw_content,
        )

        if sleep_seconds:
            time.sleep(sleep_seconds)

    except Exception as exc:
        print(f"Tavily search failed: {exc}")
        return ""

    result = "".join(
        entry["raw_content"]
        for entry in response["results"]
        if "raw_content" in entry
    )

    return result
