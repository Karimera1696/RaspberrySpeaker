import asyncio

import numpy as np

from src.audio.stream import AudioStream


async def main() -> None:
    stream = AudioStream(sample_rate=44100)  # デフォルト設定で開く
    # 背景でマイク取り込みを開始
    asyncio.create_task(stream.run())
    count = 0
    queue = stream.subscribe()
    async for frame in stream.frames(queue):
        # オーディオフレームの統計情報を計算
        rms = np.sqrt(np.mean(frame.astype(np.float32) ** 2))  # RMS音量
        peak = np.max(np.abs(frame))  # ピーク値
        mean_abs = np.mean(np.abs(frame))  # 平均絶対値

        print(
            f"[Demo] Frame #{count}: len={len(frame)}, "
            f"RMS={rms:.1f}, Peak={peak}, AvgAbs={mean_abs:.1f}"
        )
        count += 1
        if count >= 10:
            break


if __name__ == "__main__":
    asyncio.run(main())
