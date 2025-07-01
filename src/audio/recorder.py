from __future__ import annotations


class Recorder:
    """Record until silence (or timeout) and return a WAV blob.

    Workflow
    --------
    1. Collect frames from `AudioStream.frames()`
    2. Stop when
       * peak < `NoiseSampler.current_threshold()` lasts
         `SILENCE_DURATION` seconds, or
       * `MAX_RECORD_DURATION` is exceeded
    3. Concatenate to WAV bytes and return.

    Parameters
    ----------
    stream : AudioStream
    noise  : NoiseSampler
    """

    async def record_until_silence(
        self, timeout: float | None = None
    ) -> bytes:  # noqa: D401
        pass
