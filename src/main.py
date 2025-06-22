import asyncio

from dummy_impls import DummyChatModel, DummySpeechToText, DummyTextToSpeech
from interfaces import ChatModel, SpeechToText, TextToSpeech, WakeWordDetector
from wake.dummy_wake import DummyWakeWordDetector


async def pipeline(
    wake: WakeWordDetector,
    stt: SpeechToText,
    chat: ChatModel,
    tts: TextToSpeech,
) -> None:
    while True:
        # ① Wake Word 待機
        await wake.wait_for_wake()

        # ② ダミー録音した音声バイト（今回は空バイトでOK）
        audio: bytes = b"dummy audio"
        print("[Pipeline] 録音データ受領 (長さ:", len(audio), "バイト)")

        # ③ STT（文字起こし）
        text = await stt.transcribe(audio)
        print("[Pipeline] 認識結果:", text)

        # ④ LLM 応答生成
        resp = await chat.generate(text)
        print("[Pipeline] LLM 応答:", resp)

        # ⑤ TTS 合成
        audio_out = await tts.synthesize(resp)
        print("[Pipeline] TTS 出力 (バイト長:", len(audio_out), ")")

        # ⑥ ループを続けるか確認（今回はずっとループ）
        print("[Pipeline] 次の Wake Word を待ちます...\n")


async def main() -> None:
    wake_impl = DummyWakeWordDetector()
    stt_impl = DummySpeechToText()
    chat_impl = DummyChatModel()
    tts_impl = DummyTextToSpeech()

    # pipeline を起動（このままだと無限ループなので Ctrl+C で止します）
    await pipeline(wake_impl, stt_impl, chat_impl, tts_impl)


if __name__ == "__main__":
    asyncio.run(main())
