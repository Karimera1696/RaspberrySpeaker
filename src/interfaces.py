# src/interfaces.py
from typing import Protocol


class WakeWordDetector(Protocol):
    async def wait_for_wake(self) -> None:
        """
        Wake Word が検出されるまで非同期で待機し、
        検出されたら戻ってくる
        """
        ...


class SpeechToText(Protocol):
    async def transcribe(self, audio_bytes: bytes) -> str:
        """
        - audio_bytes: PCM や WAV など生の音声データ（バイト列）
        - 戻り値: 文字起こししたテキスト
        """
        ...


class ChatModel(Protocol):
    async def generate(self, prompt: str) -> str:
        """
        - prompt: いま入力されたテキスト
        - 戻り値: AI が返してきたテキスト応答
        """
        ...


class TextToSpeech(Protocol):
    async def synthesize(self, text: str) -> bytes:
        """
        - text: 返答テキスト
        - 戻り値: 音声合成したバイト列（PCM/WAV等）
        """
        ...
