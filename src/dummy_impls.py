import asyncio

from .interfaces import ChatModel, SpeechToText, TextToSpeech


class DummySpeechToText(SpeechToText):
    """Dummy speech-to-text implementation for testing."""
    async def transcribe(self, _audio_bytes: bytes) -> str:
        """Transcribe audio bytes to text (dummy)."""
        await asyncio.sleep(0.2)
        return "Dummy transcription result"


class DummyChatModel(ChatModel):
    """Dummy chat model implementation for testing."""
    async def generate(self, prompt: str) -> str:
        """Generate AI response from prompt (dummy)."""
        await asyncio.sleep(0.5)
        return f"Dummy response: Reply to '{prompt}'"


class DummyTextToSpeech(TextToSpeech):
    """Dummy text-to-speech implementation for testing."""
    async def synthesize(self, text: str) -> bytes:
        """Synthesize text to speech audio (dummy)."""
        await asyncio.sleep(0.3)
        return text.encode("utf-8")
