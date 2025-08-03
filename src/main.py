import asyncio

from src.audio import AudioStream
from src.realtime.realtime import RealtimeSessionManager
from src.wake.porcupine_wake import PorcupineWakeWordDetector


async def main() -> None:
    """Main entry point."""
    # Initialize components
    stream = AudioStream()
    wake_detector = PorcupineWakeWordDetector(stream)

    # Start background tasks
    stream_task = asyncio.create_task(stream.run())

    try:
        while True:
            # Wake word detection
            print("--- [Realtime] Starting a new cycle ---")
            print("[Realtime] Waiting for the wake word...")
            await wake_detector.wait_for_wake()
            print("[Realtime] Wake word detected!")

            # Create Realtime API session
            session = await RealtimeSessionManager.get_session(stream)
            await session.connect(audio_enabled=True)

            # Start the audio player
            await session._player.start()

            # Start streaming audio player
            async def stream_audio_player() -> None:
                """Stream audio from session to player."""
                try:
                    async for audio_chunk in session.get_audio_stream():
                        await session._player.play_audio(audio_chunk)
                except Exception as e:
                    print(f"Audio streaming ended: {e}")

            # Start audio streaming task
            asyncio.create_task(stream_audio_player())

            # Wait for user speech to stop before proceeding to next wake word
            await session.wait_for_speech_stopped()

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

        # Wait for tasks to complete cancellation
        try:
            await stream_task
        except asyncio.CancelledError:
            pass

        print("Cleanup complete.")


if __name__ == "__main__":
    asyncio.run(main())
