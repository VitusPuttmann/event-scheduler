"""
Helper function for logging LLM calls
"""

from typing import TypedDict, Any


class LLMCallEvent(TypedDict, total=False):
    provider: str
    messages: Any
    output: Any
    attempts: int
    node: str
    timestamp: str
    request_id: str


def log_llmcall(
    provider: str,
    messages: Any,
    output: Any,
    attempts: int,
    node: str,
    timestamp: str,
    request_id: str,
) -> LLMCallEvent:
    return LLMCallEvent(
        provider=provider,
        messages=messages,
        output=output,
        attempts=attempts,
        node=node,
        timestamp=timestamp,
        request_id=request_id,
    )
