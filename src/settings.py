from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# 設定のシングルトン
settings: Settings


class Settings(BaseSettings):
    """Global configuration pulled from environment (.env)."""

    # -------- Paths --------
    MODEL_ROOT: Path = Path("models")  # porcupine / whisper などのモデル置き場

    # -------- Audio --------
    SAMPLE_RATE: int = 16_000  # デフォルト録音サンプルレート
    CHANNELS: int = 1  # 1=モノラル, 2=ステレオ

    # -------- Noise Sampler --------
    NOISE_MARGIN: int = 2_000  # ピーク平均に足すマージン
    NOISE_MEASURE_INTERVAL: float = 10.0  # 何秒ごとに環境ノイズを更新するか
    NOISE_MEASURE_DURATION: float = 0.3  # 計測に使うサンプル秒数 (未実装)

    # -------- Recorder --------
    SILENCE_DURATION: float = 1.5  # 無音が続いたら録音停止 (秒)
    MAX_RECORD_DURATION: float = 10.0  # 最大録音時間 (秒)

    # -------- API Keys --------
    OPENAI_API_KEY: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
