import asyncio
from typing import Any, AsyncIterator
from unittest.mock import MagicMock

import numpy as np
import pytest

from src.audio.noise import NoiseSampler
from src.audio.stream import AudioStream


class MockQueue:
    """Mock queue for testing."""

    def __init__(self, items: list[Any]) -> None:
        """Initialize mock queue with items.

        Args:
            items: List of items to iterate over.
        """
        self.items = iter(items)

    def __aiter__(self) -> AsyncIterator[Any]:
        """Return async iterator."""
        return self

    async def __anext__(self) -> np.ndarray:
        """Get next item asynchronously."""
        try:
            return next(self.items)
        except StopIteration:
            raise StopAsyncIteration


@pytest.mark.asyncio
async def test_noise_sampler_basic() -> None:
    """Test that NoiseSampler can be constructed and returns default threshold."""
    # Arrange
    mock_stream = MagicMock(spec=AudioStream)

    # Act
    sampler = NoiseSampler(mock_stream)
    threshold = sampler.current_threshold()

    # Assert
    assert isinstance(threshold, int)
    assert threshold == 1000  # Default fallback


@pytest.mark.asyncio
async def test_noise_sampler_start_runs() -> None:
    """Sanity-check that start() begins and cancels without error."""
    # Arrange
    mock_stream = MagicMock(spec=AudioStream)
    mock_stream.subscribe.return_value = MockQueue([])
    mock_stream.frames.return_value = MockQueue([])

    sampler = NoiseSampler(mock_stream)

    # Act
    task = asyncio.create_task(sampler.start())
    await asyncio.sleep(0.01)  # Give event loop a tick
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        pass

    # Assert
    # If we reached here, the sampler started and stopped cleanly.
    assert True
