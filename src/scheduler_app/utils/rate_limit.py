"""
Rate limiter for tool calls.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ToolLimiter:
    max_calls: int = 1

    def __post_init__(self) -> None:
        self.remaining = self.max_calls

    def allow(self) -> bool:
        if self.remaining <= 0:
            return False
        self.remaining -= 1
        return True


limiter = ToolLimiter(max_calls=3)
