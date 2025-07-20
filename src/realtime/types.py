from dataclasses import dataclass
from typing import Any


@dataclass
class FunctionCall:
    """Parsed function call from Realtime API."""
    name: str
    arguments: dict[str, Any]
    call_id: str


@dataclass
class ConversationResult:
    """Result of a complete Realtime API conversation."""
    audio_data: bytes
    transcript: str
    function_calls: list[FunctionCall] | None = None
    is_interrupted: bool = False
    duration_ms: int | None = None