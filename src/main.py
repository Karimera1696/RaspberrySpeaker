import asyncio

from src.audio import AudioStream
from src.dev.dummy_impls import (
    DummyChatModel,
    DummySpeechToText,
    DummyTextToSpeech,
    DummyWakeWordDetector,
)
from src.interfaces import WakeWordDetector
from src.pipeline import SmartSpeakerPipeline
from src.settings import settings
from src.wake.porcupine_wake import PorcupineWakeWordDetector


async def main() -> None:
    """Main entry point."""
    # Initialize the wake word detector
    use_real_wake = settings.PORCUPINE_ACCESS_KEY is not None

    wake_impl: WakeWordDetector
    if use_real_wake:
        print("[Main] Using real Porcupine wake word detector")
        stream = AudioStream()
        wake_impl = PorcupineWakeWordDetector(stream)
    else:
        print("[Main] Using dummy wake word detector")
        wake_impl = DummyWakeWordDetector()

    stt_impl = DummySpeechToText()
    chat_impl = DummyChatModel()
    tts_impl = DummyTextToSpeech()

    pipeline = SmartSpeakerPipeline(
        wake=wake_impl,
        stt=stt_impl,
        chat=chat_impl,
        tts=tts_impl,
    )

    while True:
        # Wake word detection
        await wake_impl.wait_for_wake()

        # Dummy audio input
        audio: bytes = b"dummy audio"
        print("[Pipeline] Recorded data received (length:", len(audio), "byte)")

        # Run one cycle
        audio_out = await pipeline.run_one_cycle(audio)
        print("[Pipeline] TTS output (byte length:", len(audio_out), ")")

        # Wait for the next wake word
        print("[Pipeline] Wait for the next Wake Word...\n")


if __name__ == "__main__":
    asyncio.run(main())
