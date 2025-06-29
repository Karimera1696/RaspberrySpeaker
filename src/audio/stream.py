import asyncio
from collections.abc import AsyncIterator

import numpy as np
import sounddevice as sd

from settings import settings


class AudioStream:
    """Asynchronous microphone reader.

    Opens a `sounddevice.InputStream`, pushes each audio block
    (int16-PCM, mono) into an internal `asyncio.Queue`, and lets
    callers consume the blocks via `async for frame in stream.frames()`.

    Parameters
    ----------
    sample_rate : int, default settings.SAMPLE_RATE
        Requested device sample-rate (Hz).
    chunk : int, default 512
        Block size in samples.

    Notes
    -----
    *Responsibility*: **capture only**.  No resampling, no VAD.
    """

    _queue: asyncio.Queue[np.ndarray]
    _sample_rate: int
    _chunk: int

    def __init__(self, sample_rate: int | None = None, chunk: int = 512):
        self._sample_rate = sample_rate or settings.SAMPLE_RATE
        self._chunk = chunk
        self._queue = asyncio.Queue(maxsize=20)

    async def run(self) -> None:
        loop = asyncio.get_running_loop()

        def _cb(indata: np.ndarray, frames: int, time: float, status: sd.CallbackFlags) -> None:
            frame = indata.flatten().copy()
            try:
                loop.call_soon_threadsafe(self._queue.put_nowait, frame)
            except asyncio.QueueFull:
                _ = self._queue.get_nowait()
                loop.call_soon_threadsafe(self._queue.put_nowait, frame)

        with sd.InputStream(
            samplerate=self._sample_rate,
            channels=1,
            dtype="int16",
            blocksize=self._chunk,
            callback=_cb,
        ):
            while True:
                await asyncio.sleep(1)  # keep stream alive

    async def frames(self) -> AsyncIterator[np.ndarray]:
        while True:
            frame = await self._queue.get()
            yield frame
