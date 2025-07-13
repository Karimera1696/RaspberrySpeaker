from __future__ import annotations

import io
import time
import wave
from collections import deque
from typing import TYPE_CHECKING

import numpy as np

from ..settings import settings
from .utils import calculate_rms

if TYPE_CHECKING:
    from .noise import NoiseSampler
    from .stream import AudioStream


class Recorder:
    """Record until silence (or timeout) and return WAV bytes for STT processing."""

    _stream: AudioStream
    _noise: NoiseSampler
    _rms_window: deque[float]

    def __init__(self, stream: AudioStream, noise: NoiseSampler) -> None:
        """Initialize recorder.

        Args:
            stream: Audio stream source.
            noise: Noise sampler for threshold detection.
        """
        self._stream = stream
        self._noise = noise
        self._rms_window = deque(maxlen=5)

    async def record_until_silence(self, timeout: float | None = None) -> bytes:
        """Record audio until silence is detected or timeout occurs.

        Args:
            timeout: Maximum recording duration in seconds.

        Returns:
            WAV format audio data for STT processing.
        """
        max_duration = timeout or settings.MAX_RECORD_DURATION
        silence_duration = settings.SILENCE_DURATION
        threshold = self._noise.current_threshold()

        frames: list[np.ndarray] = []
        start_time = time.time()
        last_sound_time = start_time

        print(f"[Recorder] Recording... (threshold={threshold}, max={max_duration}s)")

        queue = self._stream.subscribe()
        async for frame in self._stream.frames(queue):
            frames.append(frame)
            current_time = time.time()

            # Check maximum duration
            if current_time - start_time >= max_duration:
                print(f"[Recorder] Stopped: max duration ({max_duration}s) reached")
                break

            # Check audio level using RMS with moving average
            rms_level = calculate_rms(frame)
            self._rms_window.append(rms_level)

            # Use moving average of RMS values
            avg_rms = sum(self._rms_window) / len(self._rms_window)
            if avg_rms > threshold:
                last_sound_time = current_time

            # Check Minimum recording duration
            if current_time - start_time < settings.MIN_RECORD_DURATION:
                continue

            # Check silence duration
            silence_time = current_time - last_sound_time
            if silence_time >= silence_duration:
                print(f"[Recorder] Stopped: silence detected ({silence_time:.1f}s)")
                break

        # Convert frames to WAV bytes
        if not frames:
            print("[Recorder] Warning: No frames recorded")
            return b""

        return self._frames_to_wav(frames)

    def _frames_to_wav(self, frames: list[np.ndarray]) -> bytes:
        """Convert audio frames to WAV format bytes."""
        # Concatenate all frames
        audio_data = np.concatenate(frames)

        # Create WAV file in memory
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self._stream._rate)
            wav_file.writeframes(audio_data.tobytes())

        wav_bytes = buffer.getvalue()
        duration_seconds = len(audio_data) / self._stream._rate
        print(
            f"[Recorder] Created WAV: {len(wav_bytes)} bytes, "
            f"{len(audio_data)} samples, {duration_seconds:.2f}s duration "
            f"@ {self._stream._rate}Hz"
        )
        return wav_bytes
