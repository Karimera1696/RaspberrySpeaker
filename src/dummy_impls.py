import asyncio
import random

from interfaces import ChatModel, SpeechToText, TextToSpeech, WakeWordDetector


# ← ここで Protocol を継承しているので、import は使われていると認識される
class DummyWakeWordDetector(WakeWordDetector):
    async def wait_for_wake(self) -> None:
        await asyncio.sleep(random.uniform(0.5, 1.5))
        print("[DummyWake] Wake Word 検出！")


class DummySpeechToText(SpeechToText):
    async def transcribe(self, audio_bytes: bytes) -> str:
        await asyncio.sleep(0.2)
        return "ダミー認識結果"


class DummyChatModel(ChatModel):
    async def generate(self, prompt: str) -> str:
        await asyncio.sleep(0.5)
        return f"ダミー応答: 『{prompt}』に対する返事"


class DummyTextToSpeech(TextToSpeech):
    async def synthesize(self, text: str) -> bytes:
        await asyncio.sleep(0.3)
        return text.encode("utf-8")
