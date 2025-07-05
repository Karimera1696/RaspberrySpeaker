import asyncio
import random

from ..interfaces import WakeWordDetector


class DummyWakeWordDetector(WakeWordDetector):
    """Dummy wake word detector for testing."""
    async def wait_for_wake(self) -> None:
        """Wait for wake word detection (dummy)."""
        await asyncio.sleep(random.uniform(0.5, 1.5))
        print("[DummyWake] Wake Word detected!")
