import asyncio

from src.audio.noise import NoiseSampler
from src.audio.recorder import Recorder
from src.audio.stream import AudioStream


async def main() -> None:
    """Recorder operation check code."""
    # Components setup
    stream = AudioStream()
    noise = NoiseSampler(stream)
    recorder = Recorder(stream, noise)

    # Start background tasks
    asyncio.create_task(stream.run())
    asyncio.create_task(noise.start())

    # Wait for noise calibration
    print("Calibrating noise level...")
    await asyncio.sleep(2)

    print("Say something, then be quiet for 1.5 seconds...")
    wav_data = await recorder.record_until_silence()

    if wav_data:
        # Save to file for testing
        with open("recorded_audio.wav", "wb") as f:
            f.write(wav_data)
        print(f"Audio saved to recorded_audio.wav ({len(wav_data)} bytes)")
    else:
        print("No audio recorded")


if __name__ == "__main__":
    asyncio.run(main())
