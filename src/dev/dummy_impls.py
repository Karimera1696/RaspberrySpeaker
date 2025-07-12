from ..interfaces import ChatModel, SpeechToText, TextToSpeech, WakeWordDetector


class DummyWakeWordDetector(WakeWordDetector):
    """Dummy wakeword implementation for testing."""

    async def wait_for_wake(self) -> None:
        """Wait for wake word detection (dummy)."""
        print("[DummyWakeWordDetector] Waiting for wake word...")
        return None


class DummySpeechToText(SpeechToText):
    """Dummy speech-to-text implementation for testing."""

    async def transcribe(self, _audio_bytes: bytes) -> str:
        """Transcribe audio bytes to text (dummy)."""
        print("[DummySpeechToText] Transcribing audio...")
        return "Dummy transcription result"


class DummyChatModel(ChatModel):
    """Dummy chat model implementation for testing."""

    async def generate(self, prompt: str) -> str:
        """Generate AI response from prompt (dummy)."""
        print(f"[DummyChatModel] Generating response for: {prompt}")
        return f"Dummy response: Reply to '{prompt}'"


class DummyTextToSpeech(TextToSpeech):
    """Dummy text-to-speech implementation for testing."""

    async def synthesize(self, text: str) -> bytes:
        """Synthesize text to speech audio (dummy)."""
        print(f"[DummyTextToSpeech] Synthesizing text: {text}")
        return text.encode("utf-8")
