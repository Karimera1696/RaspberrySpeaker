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
    async def connect(self, ephemeral_key: str) -> None:
        """Establish WebRTC connection with ephemeral API key.

        Args:
            ephemeral_key: 60-second temporary authentication key.
        """
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        """Close WebRTC connection and cleanup resources."""
        ...

    @abstractmethod
    async def configure_session(
        self,
        voice: str | None = None,
        temperature: float | None = None,
        system_message: str | None = None,
    ) -> None:
        """Configure session parameters via data channel.

        Args:
            voice: AI voice selection.
            temperature: Response randomness (0.0-1.0).
            system_message: System instructions.
        """
        ...

    @abstractmethod
    async def start_audio_stream(self, audio_stream: AsyncIterator[bytes]) -> None:
        """Start audio streaming via WebRTC peer connection.

        Args:
            audio_stream: Stream of audio chunks (PCM 16-bit, 24kHz, mono).
        """
        ...

    @abstractmethod
    def listen_audio_responses(self) -> AsyncIterator[bytes]:
        """Listen for streaming audio responses.

        Yields:
            Audio response chunks for real-time playback.
        """
        ...

    @abstractmethod
    def listen_events(self) -> AsyncIterator[dict[str, Any]]:
        """Listen for data channel events.

        Yields:
            Event messages including transcripts and function calls.
        """
        ...

    @abstractmethod
    async def send_event(self, event: dict[str, Any]) -> None:
        """Send event via data channel.

        Args:
            event: Event message to send to OpenAI.
        """
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
