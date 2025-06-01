import asyncio

from interfaces import ChatModel, SpeechToText, TextToSpeech, WakeWordDetector


# ダミー実装は後で作りますが、今は type hint として使うだけ
async def pipeline(
    wake: WakeWordDetector,
    stt: SpeechToText,
    chat: ChatModel,
    tts: TextToSpeech,
) -> None:
    # ここで await wake.wait_for_wake() が呼べることが保証される
    await wake.wait_for_wake()
    text = await stt.transcribe(b"dummy")
    resp = await chat.generate(text)
    audio = await tts.synthesize(resp)
    print("一連の流れが動きました")


async def main() -> None:
    # いまは実装クラスを渡せないので、None にキャストしておく例
    # （後で本物のクラスを作成して差し替えます）
    await pipeline(
        wake=None,  # type: ignore
        stt=None,  # type: ignore
        chat=None,  # type: ignore
        tts=None,  # type: ignore
    )


if __name__ == "__main__":
    asyncio.run(main())
