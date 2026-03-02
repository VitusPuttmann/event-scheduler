"""
Helper function for logging LLM calls
"""

from typing import TypedDict, Optional, Any


class LLMCallEvent(TypedDict, total=False):
    provider: str
    messages: Any
    output: Any
    attempts: int
    node: str
    timestamp: str
    request_id: str


def log_llmcall(
    provider: Optional[str] = None,
    messages: Optional[Any] = None,
    output: Optional[Any] = None,
    attempts: Optional[int] = None,
    node: Optional[str] = None,
    timestamp: Optional[str] = None,
    request_id: Optional[str] = None
) -> LLMCallEvent:
    log_llm_call: LLMCallEvent = {}

    if provider is not None:
        log_llm_call["provider"] = provider
    if messages is not None:
        log_llm_call["messages"] = messages
    if output is not None:
        log_llm_call["output"] = output
    if attempts is not None:
        log_llm_call["attempts"] = attempts
    if node is not None:
        log_llm_call["node"] = node
    if timestamp is not None:
        log_llm_call["timestamp"] = timestamp
    if request_id is not None:
        log_llm_call["request_id"] = request_id

    return log_llm_call
