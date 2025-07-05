import asyncio

import numpy as np

from src.audio.noise import NoiseSampler
from src.audio.stream import AudioStream


async def main() -> None:
    """Noise sampler operation check code."""
    stream = AudioStream(sample_rate=44100)
    noise = NoiseSampler(stream)

    # Start Audio stream (mic capture in the background)
    asyncio.create_task(stream.run())
    # Noise sampler starts
    asyncio.create_task(noise.start())

    queue = stream.subscribe()
    async for frame in stream.frames(queue):
        max_value = np.max(np.abs(frame))
        print(f"Frame: {max_value} Noise threshold: {noise.current_threshold()}")
        await asyncio.sleep(0.2)


if __name__ == "__main__":
    asyncio.run(main())
