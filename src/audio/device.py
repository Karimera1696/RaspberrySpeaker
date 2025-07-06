from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

import sounddevice as sd


@dataclass(slots=True, frozen=True)
class AudioDevice:
    """Immutable snapshot of an input device."""

    id: int
    name: str
    sample_rate: int
    channels: int

    # Explicitly declare class attributes
    _CACHE: ClassVar[AudioDevice | None] = None

    @classmethod
    def default(cls) -> "AudioDevice":
        """Return lazily-constructed default input device."""
        if cls._CACHE is None:
            dev_id = sd.default.device[0]
            info = sd.query_devices(dev_id, "input")
            rate = int(info["default_samplerate"])

            sd.check_input_settings(device=dev_id, samplerate=rate, channels=1)

            cls._CACHE = cls(
                id=dev_id,
                name=info["name"],
                sample_rate=rate,
                channels=info["max_input_channels"],
            )
        return cls._CACHE
