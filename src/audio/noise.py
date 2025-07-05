from __future__ import annotations

import time

import numpy as np

from ..settings import settings
from .stream import AudioStream


class NoiseSampler:
    """Track ambient noise and publish a threshold."""

    _stream: AudioStream
    _thr: int
    _last: float

    def __init__(self, stream: AudioStream) -> None:
        """Initialize noise sampler.
        
        Args:
            stream: Live PCM audio stream source.
        """
        self._stream = stream
        self._thr = 0
        self._last = 0.0

    async def start(self) -> None:
        """Start noise sampling coroutine."""
        buf: list[int] = []
        queue = self._stream.subscribe()
        async for frame in self._stream.frames(queue):
            rms = int(np.max(np.abs(frame)))
            buf.append(rms)
            if time.time() - self._last >= settings.NOISE_MEASURE_INTERVAL:
                avg = int(np.mean(buf))
                self._thr = avg + settings.NOISE_MARGIN
                print("[Noise] thr =", self._thr)
                buf.clear()
                self._last = time.time()

    def current_threshold(self) -> int:
        """Get current noise threshold."""
        return self._thr or 6000  # Default fallback
