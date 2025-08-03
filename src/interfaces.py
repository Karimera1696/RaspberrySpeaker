from abc import ABC, abstractmethod


class WakeWordDetector(ABC):
    """Wake word detector interface."""

    @abstractmethod
    async def wait_for_wake(self) -> None:
        """Wait for wake word detection."""
        ...


class RealtimeAPIClient(ABC):
    """OpenAI Realtime API WebRTC client interface."""

    @abstractmethod
    async def connect(self, audio_enabled: bool) -> None:
        """Establish WebRTC connection."""
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        """Close WebRTC connection and cleanup resources."""
        ...
