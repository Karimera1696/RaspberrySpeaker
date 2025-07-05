import asyncio
from collections.abc import AsyncIterator

import numpy as np
import sounddevice as sd

from .device import get_supported_sample_rate


class AudioStream:
    """Asynchronous microphone reader."""

    _subscribers: list[asyncio.Queue[np.ndarray]]
    _sample_rate: int
    _chunk: int

    def __init__(self, sample_rate: int | None = None, chunk: int = 512):
        """Initialize audio stream.
        
        Args:
            sample_rate: Requested device sample-rate (Hz). If None, uses device default.
            chunk: Block size in samples.
        """
        if sample_rate is None:
            self._sample_rate = get_supported_sample_rate()
        else:
            self._sample_rate = sample_rate
        self._chunk = chunk
        self._subscribers = []

    def subscribe(self, maxsize: int = 200) -> "asyncio.Queue[np.ndarray]":
        """Subscribe to audio frames."""
        queue: asyncio.Queue[np.ndarray] = asyncio.Queue(maxsize=maxsize)
        self._subscribers.append(queue)
        return queue

    async def run(self) -> None:
        """Run audio stream capturing."""
        loop = asyncio.get_running_loop()

        def _cb(indata: np.ndarray, frames: int, time: float, status: sd.CallbackFlags) -> None:
            frame = indata.flatten().copy()

            def _enqueue() -> None:
                for queue in list(self._subscribers):
                    try:
                        queue.put_nowait(frame)
                    except asyncio.QueueFull:
                        # Drop oldest frame and add new one
                        try:
                            _ = queue.get_nowait()
                            queue.put_nowait(frame)
                        except asyncio.QueueEmpty:
                            pass  # Queue became empty, ignore

            loop.call_soon_threadsafe(_enqueue)

        with sd.InputStream(
            samplerate=self._sample_rate,
            channels=1,
            dtype="int16",
            blocksize=self._chunk,
            callback=_cb,
        ):
            while True:
                await asyncio.sleep(1)  # Keep stream alive

    async def frames(self, queue: asyncio.Queue[np.ndarray]) -> AsyncIterator[np.ndarray]:
        """Iterate over audio frames from queue."""
        while True:
            frame = await queue.get()
            yield frame
