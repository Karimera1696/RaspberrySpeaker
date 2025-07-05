"""Audio device utilities for detecting optimal sample rates."""

import sounddevice as sd


def get_supported_sample_rate() -> int:
    """Get the default sample rate for the input device."""
    try:
        device = sd.query_devices(sd.default.device[0], kind="input")
        device_rate = int(device["default_samplerate"])

        # Verify the device rate is actually supported
        sd.check_input_settings(device=sd.default.device[0], samplerate=device_rate, channels=1)
        return device_rate
    except Exception:
        raise RuntimeError("Could not determine supported sample rate for input device")
