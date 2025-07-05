import asyncio
from collections.abc import AsyncIterator

import numpy as np
import sounddevice as sd

from .device import AudioDevice


class AudioStream:
    """Async microphone reader."""

    _subscribers: list[asyncio.Queue[np.ndarray]]
    _device: AudioDevice
    _rate: int
    _chunk: int

    def __init__(
        self,
        *,
        device: AudioDevice | None = None,
        chunk: int = 512,
    ) -> None:
        """Create stream.

        Args:
            device: Input device. If None, uses AudioDevice.default().
            chunk: Block size in samples.
        """
        self._device = device or AudioDevice.default()
        self._rate = self._device.sample_rate
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

        def _cb(indata: np.ndarray, _frames: int, _time: float, _status: sd.CallbackFlags) -> None:
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
            samplerate=self._rate,
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
