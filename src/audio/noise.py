from __future__ import annotations

import time

import numpy as np

from ..settings import settings
from .stream import AudioStream
from .utils import calculate_rms


class NoiseSampler:
    """Track ambient noise and publish a threshold."""

    _stream: AudioStream
    _threshold: int
    _last_noise_sample_time: float

    def __init__(self, stream: AudioStream) -> None:
        """Initialize noise sampler.

        Args:
            stream: Live PCM audio stream source.
        """
        self._stream = stream
        self._threshold = 0
        self._last_noise_sample_time = 0.0

    async def start(self) -> None:
        """Start noise sampling coroutine."""
        buf: list[float] = []
        queue = self._stream.subscribe()
        async for frame in self._stream.frames(queue):
            rms_level = calculate_rms(frame)
            buf.append(rms_level)
            if time.time() - self._last_noise_sample_time >= settings.NOISE_MEASURE_INTERVAL:
                avg = np.mean(buf)
                self._threshold = int(avg + settings.NOISE_MARGIN)
                print("[Noise] threshold =", self._threshold)
                buf.clear()
                self._last_noise_sample_time = time.time()

    def current_threshold(self) -> int:
        """Get current noise threshold."""
        return self._threshold or 1000  # Default fallback
