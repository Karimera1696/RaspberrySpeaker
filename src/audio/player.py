import asyncio

import numpy as np
import sounddevice as sd

from .device import AudioDevice


class AudioPlayer:
    """Audio player for real-time playback."""

    _device: AudioDevice
    _queue: asyncio.Queue[np.ndarray]
    _is_playing: bool

    def __init__(self, device: AudioDevice | None = None) -> None:
        """Initialize audio player.

        Args:
            device: Output device. If None, uses AudioDevice.default().
        """
        self._device = device or AudioDevice.default_output()
        self._queue = asyncio.Queue(maxsize=100)
        self._is_playing = False

    async def play_audio(self, audio_data: np.ndarray) -> None:
        """Queue audio data for playback.

        Args:
            audio_data: Audio data as numpy array.
        """
        try:
            self._queue.put_nowait(audio_data)
        except asyncio.QueueFull:
            # Drop oldest frame if queue is full
            try:
                self._queue.get_nowait()
                self._queue.put_nowait(audio_data)
            except asyncio.QueueEmpty:
                pass

    async def start(self) -> None:
        """Start the audio playback loop."""
        if self._is_playing:
            return

        self._is_playing = True
        asyncio.create_task(self._playback_loop())

    async def stop(self) -> None:
        """Stop audio playback."""
        self._is_playing = False

    async def _playback_loop(self) -> None:
        """Main playback loop."""
        current_frame: np.ndarray | None = None

        def _cb(outdata: np.ndarray, _frames: int, _time: float, _status: sd.CallbackFlags) -> None:
            nonlocal current_frame
            try:
                if current_frame is None or current_frame.shape[1] == 0:
                    # Get next frame from queue
                    try:
                        current_frame = self._queue.get_nowait()
                    except asyncio.QueueEmpty:
                        # No audio data available, output silence
                        outdata.fill(0)
                        return

                # Fill output buffer using reshape approach like reference code
                if current_frame is not None:
                    print(f"[PLAYER] Input: {current_frame.shape}, Output needed: {outdata.shape}")
                    outdata[:] = current_frame.reshape(outdata.shape)
                    current_frame = None

            except Exception as e:
                print(f"Audio playback error: {e}")
                outdata.fill(0)

        try:
            with sd.OutputStream(
                samplerate=48000,  # Fixed to match OpenAI Realtime API
                channels=2,
                dtype="int16",
                blocksize=960,
                callback=_cb,
                device=self._device.id,
            ):
                while self._is_playing:
                    await asyncio.sleep(1)
        except Exception as e:
            print(f"Audio output stream error: {e}")
        finally:
            self._is_playing = False
