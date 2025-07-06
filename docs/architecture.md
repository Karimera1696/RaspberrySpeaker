# SmartSpeaker2 – Responsibility Map
※ 各ディレクトリが「単一責務」で分離されていることを示す表。

| Layer / Dir | Module / Class | Single Responsibility |
|-------------|----------------|-----------------------|
| **audio** | `audio.stream.AudioStream` | Capture PCM from the mic and push to **`asyncio.Queue[np.int16]`** |
|           | `audio.noise.NoiseSampler` *(optional)* | Estimate ambient dBFS; currently **not** gating Porcupine |
| **wake**  | `wake.porcupine.PorcupineWakeDetector` | Buffer + resample → feed exactly 512-sample `int16` frames to Porcupine |
| **recorder** | `audio.recorder.Recorder` | Record until silence/timeout; return WAV for STT |
| **stt**   | `stt.openai_whisper.OpenAIWhisperSTT` | WAV → text via OpenAI Whisper |
| **chat**  | `chat.openai_chat.OpenAIChatModel` | Prompt → JSON (**function-call**) |
| **mcp**   | `mcp_client.MCPClient` | Bridge JSON → Home Assistant REST (long-lived token) |
| **tts**   | `tts.voicevox.VoiceVoxTTS` | Text → 24 kHz PCM via VoiceVox |
| **pipeline** | `pipeline.SmartSpeakerPipeline` | Orchestrate the above tasks, manage state & cancellation |
| **cli**   | `cli.main` | `python -m smartspeaker2` entrypoint (argparse) |
