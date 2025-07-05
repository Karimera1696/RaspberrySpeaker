import asyncio

from src.audio.noise import NoiseSampler
from src.audio.stream import AudioStream
from src.wake.porcupine_wake import PorcupineWakeWordDetector


async def main() -> None:
    """Porcupine operation check code."""
    stream = AudioStream()
    noise_sampler = NoiseSampler(stream)
    detector = PorcupineWakeWordDetector(stream, noise_sampler)

    print("Starting audio stream and noise sampler...")

    async def run_stream() -> None:
        asyncio.create_task(stream.run())

    async def run_noise_sampler() -> None:
        asyncio.create_task(noise_sampler.start())

    async def test_detection() -> None:
        print("Listening for wake word... (low volume sounds should be ignored)")
        print("Try speaking 'Zundamon' to test detection")
        await detector.wait_for_wake()
        print("Wake word detected! Test completed.")

    # Run all components concurrently
    await asyncio.gather(run_stream(), run_noise_sampler(), test_detection())


if __name__ == "__main__":
    asyncio.run(main())
