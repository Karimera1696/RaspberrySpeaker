from collections import deque
from typing import cast

import numpy as np
import numpy.typing as npt
import pvporcupine
from scipy.signal import resample_poly

from ..audio import AudioStream
from ..interfaces import WakeWordDetector
from ..settings import settings

Int16Array = npt.NDArray[np.int16]


class PorcupineWakeWordDetector(WakeWordDetector):
    """Porcupine wake word detector implementation."""

    _stream: AudioStream
    _porcupine: pvporcupine.Porcupine
    _stream_sample_rate: int
    _porcupine_sample_rate: int
    _buffer: deque[int]

    def __init__(self, stream: AudioStream) -> None:
        """Initialize Porcupine wake word detector.

        Args:
            stream: Audio stream to listen for wake words.

        Raises:
            RuntimeError: If PORCUPINE_ACCESS_KEY is not set.
        """
        self._stream = stream

        if not settings.PORCUPINE_ACCESS_KEY:
            raise RuntimeError("PORCUPINE_ACCESS_KEY not set in environment")

        self._porcupine = pvporcupine.create(
            access_key=settings.PORCUPINE_ACCESS_KEY,
            model_path=str(settings.PORCUPINE_MODEL_PATH),
            keyword_paths=[str(settings.PORCUPINE_KEYWORD_PATH)],
        )
        self._stream_sample_rate = stream._rate
        self._porcupine_sample_rate = self._porcupine.sample_rate
        self._buffer = deque()

    def _resample_frame(self, frame: np.ndarray) -> Int16Array:
        if self._stream_sample_rate == self._porcupine_sample_rate:
            return cast(Int16Array, frame)

        resampled = resample_poly(
            frame,
            self._porcupine_sample_rate,
            self._stream_sample_rate,
        ).astype(np.int16)

        return cast(Int16Array, resampled)

    async def wait_for_wake(self) -> None:
        """Wait for wake word detection."""
        queue = self._stream.subscribe()
        async for frame in self._stream.frames(queue):
            self._buffer.extend(self._resample_frame(frame))

            while len(self._buffer) >= self._porcupine.frame_length:
                chunk = np.array(
                    [self._buffer.popleft() for _ in range(self._porcupine.frame_length)],
                    dtype=np.int16,
                )
                if self._porcupine.process(chunk) >= 0:
                    print("Wake word detected")
                    return
