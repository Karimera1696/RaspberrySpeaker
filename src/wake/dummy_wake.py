import asyncio
import random

from interfaces import WakeWordDetector


class DummyWakeWordDetector(WakeWordDetector):
    async def wait_for_wake(self) -> None:
        await asyncio.sleep(random.uniform(0.5, 1.5))
        print("[DummyWake] Wake Word 検出！")
