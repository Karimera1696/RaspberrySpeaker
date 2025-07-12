"""Pipeline orchestrating one voice-in → voice-out pass."""

from __future__ import annotations

from src.interfaces import (
    ChatModel,
    SpeechToText,
    TextToSpeech,
    WakeWordDetector,
)


class SmartSpeakerPipeline:
    """Run a single inference cycle from bytes to bytes."""

    def __init__(
        self,
        *,
        wake: WakeWordDetector,
        stt: SpeechToText,
        chat: ChatModel,
        tts: TextToSpeech,
    ) -> None:
        """Initialize the pipeline.

        Args:
        wake: Wake-word detector.
        stt: Speech-to-text engine.
        chat: Language model.
        tts: Text-to-speech engine.
        """
        self._wake = wake
        self._stt = stt
        self._chat = chat
        self._tts = tts

    async def run_one_cycle(self, audio: bytes) -> bytes:
        """Execute one cycle.

        Args:
            audio: Captured audio after the wake word.

        Returns:
            Synthesised reply audio.
        """
        text = await self._stt.transcribe(audio)
        reply = await self._chat.generate(text)
        return await self._tts.synthesize(reply)
