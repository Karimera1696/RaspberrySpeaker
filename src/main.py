import asyncio

import numpy as np

from src.audio import AudioStream, NoiseSampler, Recorder
from src.dev.dummy_impls import (
    DummyChatModel,
    DummySpeechToText,
    DummyTextToSpeech,
)
from src.pipeline import SmartSpeakerPipeline
from src.wake.porcupine_wake import PorcupineWakeWordDetector


async def main() -> None:
    """Main entry point."""
    # Initialize the wake word detector

    stream = AudioStream()
    noise = NoiseSampler(stream)
    recorder = Recorder(stream, noise)
    wake_impl = PorcupineWakeWordDetector(stream)
    stt_impl = DummySpeechToText()
    chat_impl = DummyChatModel()
    tts_impl = DummyTextToSpeech()

    pipeline = SmartSpeakerPipeline(
        stt=stt_impl,
        chat=chat_impl,
        tts=tts_impl,
    )

    # Start background tasks
    stream_task = asyncio.create_task(stream.run())
    noise_task = asyncio.create_task(noise.start())

    try:
        while True:
            # Wake word detection
            print("--- [Pipeline] Starting a new cycle ---")
            print("[Pipeline] Waiting for the wake word...")
            await wake_impl.wait_for_wake()
            print("[Pipeline] Wake word detected!")

            # Dummy audio input
            frames: list[np.ndarray] = await recorder.record_until_silence()
            print("[Pipeline] Recorded data received (frame count:", len(frames), ")")

            # Run one cycle
            # audio_out = await pipeline.run_one_cycle(audio)
            # print("[Pipeline] TTS output (byte length:", len(audio_out), ")")

            # Wait for the next wake word
            print("[Pipeline] Wait for the next Wake Word...")
            print("--- [Pipeline] Cycle completed ---")
            print()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        # Clean up background tasks
        print("Cancelling background tasks...")
        stream_task.cancel()
        noise_task.cancel()

        # Wait for tasks to complete cancellation
        try:
            await stream_task
        except asyncio.CancelledError:
            pass

        try:
            await noise_task
        except asyncio.CancelledError:
            pass

        print("Cleanup complete.")


if __name__ == "__main__":
    asyncio.run(main())
