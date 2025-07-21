from abc import ABC, abstractmethod
from typing import Any, AsyncIterator


class WakeWordDetector(ABC):
    """Wake word detector interface."""

    @abstractmethod
    async def wait_for_wake(self) -> None:
        """Wait for wake word detection."""
        ...


class SpeechToText(ABC):
    """Speech-to-text interface."""

    @abstractmethod
    async def transcribe(self, audio_bytes: bytes) -> str:
        """Transcribe audio bytes to text.

        Args:
            audio_bytes: Raw audio data (PCM or WAV format).

        Returns:
            Transcribed text.
        """
        ...


class ChatModel(ABC):
    """Chat model interface."""

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Generate AI response from prompt.

        Args:
            prompt: Input text prompt.

        Returns:
            AI-generated text response.
        """
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


class TextToSpeech(ABC):
    """Text-to-speech interface."""

    @abstractmethod
    async def synthesize(self, text: str) -> bytes:
        """Synthesize text to speech audio.

        Args:
            text: Text to synthesize.

        Returns:
            Synthesized audio data (PCM or WAV format).
        """
        ...
