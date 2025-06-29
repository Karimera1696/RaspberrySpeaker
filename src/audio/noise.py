from __future__ import annotations

import time

import numpy as np

from settings import settings

from .stream import AudioStream


class NoiseSampler:
    """Track ambient noise and publish a threshold.

    Runs as a background coroutine: every *N* seconds it averages the
    peak amplitude of recent frames and adds `NOISE_MARGIN`.
    `current_threshold()` returns that value for VAD / wake-word checks.

    Parameters
    ----------
    stream : AudioStream
        Live PCM source.
    """

    _stream: AudioStream
    _thr: int
    _last: float

    def __init__(self, stream: AudioStream):
        self._stream = stream
        self._thr = 0
        self._last = 0.0

    async def start(self) -> None:
        buf: list[int] = []
        async for frame in self._stream.frames():
            rms = int(np.max(np.abs(frame)))
            buf.append(rms)
            if time.time() - self._last >= settings.NOISE_MEASURE_INTERVAL:
                avg = int(np.mean(buf))
                self._thr = avg + settings.NOISE_MARGIN
                print("[Noise] thr =", self._thr)
                buf.clear()
                self._last = time.time()

    def current_threshold(self) -> int:
        return self._thr or 6000  # デフォルト保険
