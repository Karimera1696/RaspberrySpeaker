import numpy as np
import pvporcupine

from ..audio import AudioStream, NoiseSampler
from ..interfaces import WakeWordDetector
from ..settings import settings


class PorcupineWakeWordDetector(WakeWordDetector):
    """Porcupine wake word detector implementation."""
    _stream: AudioStream
    _noise_sampler: NoiseSampler
    _porcupine: pvporcupine.Porcupine
    _stream_sample_rate: int
    _porcupine_sample_rate: int

    def __init__(self, stream: AudioStream, noise_sampler: NoiseSampler) -> None:
        """Initialize Porcupine wake word detector.
        
        Args:
            stream: Audio stream to listen for wake words.
            noise_sampler: Noise sampler for filtering out noise.
            
        Raises:
            RuntimeError: If PORCUPINE_ACCESS_KEY is not set.
        """
        self._stream = stream
        self._noise_sampler = noise_sampler

        if not settings.PORCUPINE_ACCESS_KEY:
            raise RuntimeError("PORCUPINE_ACCESS_KEY not set in environment")

        self._porcupine = pvporcupine.create(
            access_key=settings.PORCUPINE_ACCESS_KEY,
            model_path=str(settings.PORCUPINE_MODEL_PATH),
            keyword_paths=[str(settings.PORCUPINE_KEYWORD_PATH)],
        )
        self._stream_sample_rate = stream._sample_rate
        self._porcupine_sample_rate = self._porcupine.sample_rate

        print(f"[Porcupine] Expected sample rate: {self._porcupine_sample_rate}")
        print(f"[AudioStream] Using sample rate: {self._stream_sample_rate}")

        if self._stream_sample_rate != self._porcupine_sample_rate:
            print(
                f"[Warning] Sample rate mismatch! Conversion needed: "
                f"{self._stream_sample_rate} > {self._porcupine_sample_rate}"
            )

    def _resample_frame(self, frame: np.ndarray) -> np.ndarray:
        """Resample audio frame for Porcupine compatibility."""
        print(f"resampling frame: {frame.shape}")
        if self._stream_sample_rate == self._porcupine_sample_rate:
            return frame

        # Simple decimation/interpolation for common cases
        ratio = self._stream_sample_rate / self._porcupine_sample_rate
        if ratio == int(ratio):
            # Decimation: skip samples for downsampling
            step = int(ratio)
            return frame[::step]
        else:
            # Linear interpolation for complex ratios
            target_length = int(len(frame) / ratio)
            indices = np.linspace(0, len(frame) - 1, target_length, dtype=int)
            return frame[indices]

    async def wait_for_wake(self) -> None:
        """Wait for wake word detection."""
        queue = self._stream.subscribe()
        async for frame in self._stream.frames(queue):
            frame_max = int(np.max(np.abs(frame)))

            if frame_max < self._noise_sampler.current_threshold():
                continue

            # Resample frame if sample rates don't match
            resampled_frame = self._resample_frame(frame)

            if len(resampled_frame) == self._porcupine.frame_length:
                keyword_index = self._porcupine.process(resampled_frame)
                if keyword_index >= 0:
                    print("Detected")
                    break
