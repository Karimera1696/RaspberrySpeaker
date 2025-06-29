import asyncio

from interfaces import WakeWordDetector


class PorcupineWakeWordDetector(WakeWordDetector):
    async def wait_for_wake(self) -> None:
        await asyncio.sleep(1)
        print("[DummyWake] Wake Word 検出！")
