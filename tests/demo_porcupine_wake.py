import asyncio

from src.audio.stream import AudioStream
from src.wake.porcupine_wake import PorcupineWakeWordDetector


async def main() -> None:
    """Porcupine operation check code."""
    stream = AudioStream()
    detector = PorcupineWakeWordDetector(stream)

    print("Starting audio stream and noise sampler...")

    async def run_stream() -> None:
        asyncio.create_task(stream.run())

    async def test_detection() -> None:
        print("Listening for wake word... (low volume sounds should be ignored)")
        print("Try speaking 'Zundamon' to test detection")
        await detector.wait_for_wake()
        print("Wake word detected! Test completed.")

    # Run all components concurrently
    await asyncio.gather(run_stream(), test_detection())


if __name__ == "__main__":
    asyncio.run(main())
