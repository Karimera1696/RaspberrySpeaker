import asyncio
import fractions
import json
import time
from typing import Any, AsyncIterator

import numpy as np
from aiohttp import ClientError, ClientSession
from aiortc import MediaStreamTrack, RTCPeerConnection
from av import AudioFrame

from ..audio.stream import AudioStream
from ..interfaces import RealtimeAPIClient
from ..settings import settings


class OpenAIRealtimeAPIWrapper(RealtimeAPIClient):
    """OpenAI Realtime API WebRTC client wrapper."""

    _stream: AudioStream
    _pc: RTCPeerConnection | None
    _dc: Any | None
    _start_time: float

    def __init__(self, stream: AudioStream) -> None:
        """Initialize the OpenAI Realtime API wrapper.

        Args:
            stream: AudioStream instance to read audio frames from.

        """
        self._stream = stream
        self._pc = None
        self._dc = None
        self._start_time = 0.0
        print("OpenAI Realtime API wrapper initialized.")

    async def _initialize_api_session(
        self, modalities: list[str] = ["audio", "text"], default_prompt: str = ""
    ) -> str:
        """Fetch a temporary ephemeral key for WebRTC connection.

        Args:
            modalities: List of modalities to enable (e.g., ["audio", "text"]).
            default_prompt: Default prompt for the session.

        Returns:
            str: Ephemeral key for WebRTC connection.
        """
        # Simulate fetching an ephemeral key from OpenAI API
        print("Fetching ephemeral key...")
        url = settings.REALTIME_API_NEW_SESSION_URL
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": settings.REALTIME_MODEL,
            "modalities": modalities,
            "instructions": default_prompt,
        }
        try:
            async with ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return str(data["client_secret"]["value"])
        except ClientError as e:
            raise ConnectionError(f"API request failed: {e}") from e
        except KeyError as e:
            raise ValueError(f"Invalid response format: missing {e}") from e

    async def connect(self, audio_enabled: bool) -> None:
        """Establish WebRTC connection."""
        print("Connecting to OpenAI")
        modalities = ["audio", "text"] if audio_enabled else ["text"]
        ephemeral_key = await self._initialize_api_session(
            modalities, default_prompt="日本語で答えてください"
        )
        print(f"Ephemeral key obtained: {ephemeral_key}")
        self._pc = RTCPeerConnection()

        @self._pc.on("track")
        def on_track(track: MediaStreamTrack) -> None:
            print(f"Track received: {track.kind}")

        self._pc.addTrack(AudioStreamTrack(self._stream))

        self._dc = self._pc.createDataChannel("oai-events")

        @self._dc.on("open")
        def on_open() -> None:
            print("Data channel opened")

        @self._dc.on("message")
        def on_message(message: str) -> None:
            self._handle_message(message, audio_enabled)

        offer = await self._pc.createOffer()
        await self._pc.setLocalDescription(offer)
        print("Local description set")

        # Send SDP offer to OpenAI and get answer
        base_url = settings.REALTIME_API_SIGNALING_URL
        model = settings.REALTIME_MODEL
        url = f"{base_url}?model={model}"
        headers = {
            "Authorization": f"Bearer {ephemeral_key}",
            "Content-Type": "application/sdp",
        }

        try:
            async with ClientSession() as session:
                async with session.post(url, data=offer.sdp, headers=headers) as response:
                    response.raise_for_status()
                    answer_sdp = await response.text()

                    answer = type(
                        "RTCSessionDescription", (), {"type": "answer", "sdp": answer_sdp}
                    )()

                    await self._pc.setRemoteDescription(answer)
                    print("Remote description set successfully")

        except ClientError as e:
            raise ConnectionError(f"SDP exchange failed: {e}") from e

    async def disconnect(self) -> None:
        """Close WebRTC connection and cleanup resources."""
        print("Disconnecting and cleaning up resources.")
        if self._dc:
            self._dc.close()
            self._dc = None
        if self._pc:
            for sender in self._pc.getSenders():
                if sender.track:
                    print(f"Stopping track: {sender.track.kind}")
                    sender.track.stop()
            await self._pc.close()
            self._pc = None

    def _handle_message(self, message: str, audio_enabled: bool) -> None:
        """Handle incoming WebRTC data channel messages."""

        def handle_user_speech_started(_: dict[str, Any]) -> None:
            # ユーザーの発話開始処理
            elapsed = time.perf_counter() - self._start_time if self._start_time > 0 else 0
            print(f"{elapsed:.2f}s User speech started")
            self._start_time = time.perf_counter()

        def handle_response_delta(data: dict[str, Any]) -> None:
            # delta処理
            elapsed = time.perf_counter() - self._start_time if self._start_time > 0 else 0
            print(f"{elapsed:.2f}s Delta: {data.get('delta', '')}")

        def handle_response_done(data: dict[str, Any]) -> None:
            # done処理
            elapsed = time.perf_counter() - self._start_time if self._start_time > 0 else 0
            print(f"{elapsed:.2f}s Done: {data.get('transcript', '')}")
            if not audio_enabled:
                print(f"{elapsed:.2f}s Disconnecting after text response")
                asyncio.create_task(self.disconnect())

        def handle_output_audio_buffer_stopped(_: dict[str, Any]) -> None:
            # 出力オーディオバッファ停止処理
            elapsed = time.perf_counter() - self._start_time if self._start_time > 0 else 0
            print(f"{elapsed:.2f}s Output audio buffer stopped")
            if audio_enabled:
                print(f"{elapsed:.2f}s Disconnecting after audio playback")
                asyncio.create_task(self.disconnect())

        handlers = {
            "input_audio_buffer.speech_started": handle_user_speech_started,
            "response.audio_transcript.delta": handle_response_delta,
            "response.audio_transcript.done": handle_response_done,
            "response.text.delta": handle_response_delta,
            "response.done": handle_response_done,
            "output_audio_buffer.stopped": handle_output_audio_buffer_stopped,
        }
        try:
            data = json.loads(message)
            event_type = data.get("type")
            if event_type in handlers:
                handlers[event_type](data)
            else:
                elapsed = time.perf_counter() - self._start_time if self._start_time > 0 else 0
                print(f"{elapsed:.2f}s Unhandled event type: {event_type}")
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON message: {e}")
        except KeyError as e:
            raise ValueError(f"Invalid response format: missing {e}") from e

    async def configure_session(
        self,
        voice: str | None = None,
        temperature: float | None = None,
        system_message: str | None = None,
    ) -> None:
        """Configure session parameters via data channel."""
        print(
            f"Configuring session - voice: {voice}, temp: {temperature}, system: {system_message}"
        )

    async def start_audio_stream(self, audio_stream: AsyncIterator[bytes]) -> None:
        """Start audio streaming via WebRTC peer connection."""
        print("Starting audio stream.")
        async for audio_chunk in audio_stream:
            print(f"Processing audio chunk: {len(audio_chunk)} bytes")

    def listen_audio_responses(self) -> AsyncIterator[bytes]:
        """Listen for streaming audio responses."""

        async def _generator() -> AsyncIterator[bytes]:
            print("Listening for audio responses.")
            while True:
                yield b"dummy_audio_chunk"

        return _generator()

    def listen_events(self) -> AsyncIterator[dict[str, Any]]:
        """Listen for data channel events."""

        async def _generator() -> AsyncIterator[dict[str, Any]]:
            print("Listening for data channel events.")
            while True:
                yield {"type": "dummy_event", "data": "dummy_data"}

        return _generator()

    async def send_event(self, event: dict[str, Any]) -> None:
        """Send event via data channel."""
        print(f"Sending event: {event}")


class AudioStreamTrack(MediaStreamTrack):
    """Audio stream track for WebRTC."""

    kind: str = "audio"
    _stream: AudioStream
    _queue: asyncio.Queue[np.ndarray]
    _timestamp: int

    def __init__(self, audio_stream: AudioStream) -> None:
        """Initialize audio stream track.

        Args:
            audio_stream: AudioStream instance to read audio frames from.
        """
        super().__init__()
        self._stream = audio_stream
        self._queue = audio_stream.subscribe()
        self._timestamp = 0

    async def recv(self) -> AudioFrame:
        """Receive audio frame from the stream.

        Returns:
            AudioFrame: Audio frame with PCM data.
        """
        # get the next audio data from AudioStream
        audio_data = await self._queue.get()

        frame = AudioFrame(format="s16", layout="mono", samples=len(audio_data))
        frame.planes[0].update(audio_data.tobytes())
        frame.pts = self._timestamp
        frame.sample_rate = self._stream._rate
        frame.time_base = fractions.Fraction(1, self._stream._rate)

        self._timestamp += len(audio_data)
        return frame
