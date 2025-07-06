from typing import Protocol


class WakeWordDetector(Protocol):
    """Wake word detector protocol."""
    
    async def wait_for_wake(self) -> None:
        """Wait for wake word detection."""
        ...


class SpeechToText(Protocol):
    """Speech-to-text protocol."""
    
    async def transcribe(self, audio_bytes: bytes) -> str:
        """Transcribe audio bytes to text.
        
        Args:
            audio_bytes: Raw audio data (PCM or WAV format).
            
        Returns:
            Transcribed text.
        """
        ...


class ChatModel(Protocol):
    """Chat model protocol."""
    
    async def generate(self, prompt: str) -> str:
        """Generate AI response from prompt.
        
        Args:
            prompt: Input text prompt.
            
        Returns:
            AI-generated text response.
        """
        ...


class TextToSpeech(Protocol):
    """Text-to-speech protocol."""
    
    async def synthesize(self, text: str) -> bytes:
        """Synthesize text to speech audio.
        
        Args:
            text: Text to synthesize.
            
        Returns:
            Synthesized audio data (PCM or WAV format).
        """
        ...
