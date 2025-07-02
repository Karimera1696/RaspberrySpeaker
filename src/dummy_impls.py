import asyncio

from .interfaces import ChatModel, SpeechToText, TextToSpeech


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
