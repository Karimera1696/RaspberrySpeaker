import asyncio

from src.audio import AudioStream, NoiseSampler
from src.realtime.realtime import OpenAIRealtimeAPIWrapper
from src.wake.porcupine_wake import PorcupineWakeWordDetector


async def main() -> None:
    """Main entry point."""
    # Initialize components
    stream = AudioStream()
    noise = NoiseSampler(stream)
    wake_detector = PorcupineWakeWordDetector(stream)
    realtime_client = OpenAIRealtimeAPIWrapper(stream)

    # Start background tasks
    stream_task = asyncio.create_task(stream.run())
    noise_task = asyncio.create_task(noise.start())

    try:
        while True:
            # Wake word detection
            print("--- [Realtime] Starting a new cycle ---")
            print("[Realtime] Waiting for the wake word...")
            await wake_detector.wait_for_wake()
            print("[Realtime] Wake word detected!")

            # Connect to Realtime API - handles conversation until completion internally
            await realtime_client.connect(audio_enabled=True)

            # Wait for the next wake word
            print("[Realtime] Wait for the next Wake Word...")
            print("--- [Realtime] Cycle completed ---")
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
