"""SmartSpeaker2 source package."""

from .interfaces import RealtimeAPIClient, WakeWordDetector
from .settings import Settings

__all__ = ["WakeWordDetector", "RealtimeAPIClient", "Settings"]
