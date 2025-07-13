"""Audio processing utilities."""

from __future__ import annotations

import numpy as np


def calculate_rms(frame: np.ndarray) -> float:
    """Calculate RMS (Root Mean Square) level of audio frame.
    
    Args:
        frame: Audio frame data.
        
    Returns:
        RMS level as float.
    """
    return float(np.sqrt(np.mean(frame.astype(np.float64) ** 2)))