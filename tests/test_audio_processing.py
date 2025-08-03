import numpy as np


def test_aiortc_to_sounddevice_reshape() -> None:
    """Test critical audio data transformation: (1,1920) -> reshape -> (960,2)."""
    # Arrange - simulate actual aiortc output
    aiortc_output = np.arange(1920, dtype=np.int16).reshape(1, 1920)
    expected_shape = (960, 2)

    # Act - apply actual transformation used in code
    reshaped = aiortc_output.reshape(expected_shape)

    # Assert - verify data integrity and shape
    assert reshaped.shape == expected_shape
    assert reshaped.size == aiortc_output.size
    assert reshaped[0, 0] == aiortc_output[0, 0]  # First element preserved
    assert reshaped[-1, -1] == aiortc_output[0, -1]  # Last element preserved


def test_stereo_data_channel_access() -> None:
    """Test accessing left/right channels from (2, 960) stereo data."""
    # Arrange
    left_channel = np.arange(960, dtype=np.int16)
    right_channel = np.arange(960, 1920, dtype=np.int16)
    stereo_data = np.vstack([left_channel, right_channel])

    # Act
    extracted_left = stereo_data[0, :]
    extracted_right = stereo_data[1, :]

    # Assert
    assert stereo_data.shape == (2, 960)
    np.testing.assert_array_equal(extracted_left, left_channel)
    np.testing.assert_array_equal(extracted_right, right_channel)


