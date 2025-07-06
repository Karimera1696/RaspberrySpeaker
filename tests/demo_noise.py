import asyncio

import numpy as np

from src.audio.noise import NoiseSampler
from src.audio.stream import AudioStream


async def main() -> None:
    """Noise sampler operation check code."""
    stream = AudioStream()
    noise = NoiseSampler(stream)

    # Start Audio stream (mic capture in the background)
    asyncio.create_task(stream.run())
    # Noise sampler starts
    asyncio.create_task(noise.start())

    queue = stream.subscribe()
    async for frame in stream.frames(queue):
        max_value = np.max(np.abs(frame))
        if noise.current_threshold() < max_value:
            print("Voice detected!")
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())
