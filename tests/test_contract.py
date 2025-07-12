import pytest

from src.dev.dummy_impls import (
    DummyChatModel,
    DummySpeechToText,
    DummyTextToSpeech,
    DummyWakeWordDetector,
)
from src.pipeline import SmartSpeakerPipeline


@pytest.mark.asyncio
async def test_pipeline_contract() -> None:
    """Test that the pipeline contract (bytes→str→str→bytes) works end-to-end."""
    # Arrange
    wake = DummyWakeWordDetector()
    stt = DummySpeechToText()
    chat = DummyChatModel()
    tts = DummyTextToSpeech()

    pipeline = SmartSpeakerPipeline(
        wake=wake,
        stt=stt,
        chat=chat,
        tts=tts,
    )

    # Act
    input_audio = b"test audio input"
    output_audio = await pipeline.run_one_cycle(input_audio)

    # Assert
    assert isinstance(output_audio, bytes)
    assert len(output_audio) > 0
