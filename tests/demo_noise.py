import asyncio

from src.audio.noise import NoiseSampler
from src.audio.stream import AudioStream


async def main() -> None:
    stream = AudioStream(sample_rate=44100)
    noise = NoiseSampler(stream)

    # AudioStreamを開始（バックグラウンドでマイクキャプチャ）
    asyncio.create_task(stream.run())
    # NoiseSamplerも開始（バックグラウンドでキューを消費）
    asyncio.create_task(noise.start())
    
    await asyncio.sleep(0.1)  # 初期化待ち
    while True:
        print(f"Noise threshold: {noise.current_threshold()}")
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
