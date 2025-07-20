import asyncio
import io
import wave

import numpy as np
import sounddevice as sd

from src.audio.noise import NoiseSampler
from src.audio.recorder import Recorder
from src.audio.stream import AudioStream


async def play_wav_bytes(wav_data: bytes) -> None:
    """Play WAV audio data using sounddevice.

    Args:
        wav_data: WAV format audio bytes.
    """
    # Parse WAV data
    buffer = io.BytesIO(wav_data)
    with wave.open(buffer, "rb") as wav_file:
        frames = wav_file.readframes(wav_file.getnframes())
        sample_rate = wav_file.getframerate()
        channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()

    # Convert to numpy array for sounddevice
    import numpy as np

    if sample_width == 2:  # 16-bit
        audio_array = np.frombuffer(frames, dtype=np.int16)
    elif sample_width == 4:  # 32-bit
        audio_array = np.frombuffer(frames, dtype=np.int32)
    else:
        raise ValueError(f"Unsupported sample width: {sample_width}")

    if channels == 2:
        audio_array = audio_array.reshape(-1, 2)

    # Play audio
    sd.play(audio_array, samplerate=sample_rate)

    # Wait for playback to complete
    duration = len(audio_array) / sample_rate
    await asyncio.sleep(duration + 0.1)  # Small buffer for completion


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
    await asyncio.sleep(1)

    print("Say something, then be quiet for 1.5 seconds...")
    frame: list[np.ndarray] = await recorder.record_until_silence()
    wav_data = recorder.frames_to_wav(frame)

    if wav_data:
        print(f"Audio recorded ({len(wav_data)} bytes)")

        # Play back the recorded audio
        print("Playing back recorded audio...")
        await play_wav_bytes(wav_data)
        print("Playback complete")
    else:
        print("No audio recorded")


if __name__ == "__main__":
    asyncio.run(main())
