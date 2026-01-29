"""
Helper function for logging LLM calls
"""

from typing import TypedDict, Optional, Any, List


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
        messages: Any = None,
        output: Any = None,
        attempts: Optional[int] = None,
        node: Optional[str] = None,
        timestamp: Optional[str] = None,
        request_id: Optional[str] = None
) -> LLMCallEvent:
    log_llm_call: LLMCallEvent = {
        "provider": provider,
        "messages": messages,
        "output": output,
        "attempts": attempts,
        "node": node,
        "timestamp": timestamp,
        "request_id": request_id
    }

    return log_llm_call
