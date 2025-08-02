from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

import sounddevice as sd


@dataclass(slots=True, frozen=True)
class AudioDevice:
    """Immutable snapshot of an audio device."""

    id: int
    name: str
    sample_rate: int
    channels: int

    # Explicitly declare class attributes
    _INPUT_CACHE: ClassVar[AudioDevice | None] = None
    _OUTPUT_CACHE: ClassVar[AudioDevice | None] = None

    @classmethod
    def default_input(cls) -> "AudioDevice":
        """Return lazily-constructed default input device."""
        if cls._INPUT_CACHE is None:
            dev_id = sd.default.device[0]
            info = sd.query_devices(dev_id, "input")
            rate = int(info["default_samplerate"])

            sd.check_input_settings(device=dev_id, samplerate=rate, channels=1)

            cls._INPUT_CACHE = cls(
                id=dev_id,
                name=info["name"],
                sample_rate=rate,
                channels=1,
            )
        return cls._INPUT_CACHE

    @classmethod
    def default_output(cls) -> "AudioDevice":
        """Return lazily-constructed default output device."""
        if cls._OUTPUT_CACHE is None:
            dev_id = sd.default.device[1]
            info = sd.query_devices(dev_id, "output")
            rate = int(info["default_samplerate"])

            sd.check_output_settings(device=dev_id, samplerate=rate, channels=1)

            cls._OUTPUT_CACHE = cls(
                id=dev_id,
                name=info["name"],
                sample_rate=rate,
                channels=1,
            )
        return cls._OUTPUT_CACHE

    @classmethod
    def default(cls) -> "AudioDevice":
        """Return default input device for backward compatibility."""
        return cls.default_input()
