from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Settings singleton
settings: Settings


class Settings(BaseSettings):
    """Global configuration pulled from environment (.env)."""

    # -------- Paths --------
    MODEL_ROOT: Path = Path("models")  # Model directory for porcupine / whisper etc.

    # -------- Audio --------
    SAMPLE_RATE: int = 16_000  # Default recording sample rate
    CHANNELS: int = 1  # 1=mono, 2=stereo

    # -------- Noise Sampler --------
    NOISE_MARGIN: int = 300  # Margin added to peak average
    NOISE_MEASURE_INTERVAL: float = 10.0  # How often to update noise level (seconds)

    # -------- Recorder --------
    SILENCE_DURATION: float = 1.5  # Stop recording after silence (seconds)
    MIN_RECORD_DURATION: float = 3.0  # Minimum recording time (seconds)
    MAX_RECORD_DURATION: float = 10.0  # Maximum recording time (seconds)

    # -------- API Keys --------
    OPENAI_API_KEY: str | None = None
    PORCUPINE_ACCESS_KEY: str | None = None

    # -------- Porcupine Settings --------
    PORCUPINE_MODEL_PATH: Path = MODEL_ROOT / "porcupine" / "acoustic" / "porcupine_params_ja.pv"
    PORCUPINE_KEYWORD_PATH: Path = (
        MODEL_ROOT / "porcupine" / "wakewords" / "Sample_ja_raspberry-pi_v3_0_0.ppn"
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
