# SmartSpeaker2 – Responsibility Map

| Layer / Dir   | Python module / class                 | Single responsibility                                |
|---------------|---------------------------------------|-----------------------------------------------------|
| **audio**     | `audio.stream.AudioStream`            | マイク入力 → `asyncio.Queue` へ PCM フレームを送る  |
|               | `audio.noise.NoiseSampler`            | 周囲ノイズを一定間隔で計測し、しきい値 (dBFS) を保持 |
|               | `audio.recorder.Recorder`             | Wake 後の音声を録音し、無音 or timeout で WAV を返す |
| **wake**      | `wake.porcupine.PorcupineWakeDetector`| しきい値以上のフレームのみ Porcupine に渡し Wake 判定 |
| **vad**       | `vad.rms_vad.RMSVAD` (内部 util)      | RMS で有音/無音を判定（Recorder から呼ばれる）       |
| **stt**       | `stt.openai_whisper.OpenAIWhisperSTT` | WAV → 文字列 (OpenAI Whisper API)                   |
| **chat**      | `chat.openai_chat.OpenAIChatModel`    | プロンプト → 応答テキスト                           |
| **tts**       | `tts.openai_tts.OpenAITTS`            | テキスト → PCM24k バイト列                          |
| **pipeline**  | `pipeline.SmartSpeakerPipeline`       | 上記コンポを協調実行する orchestrator               |
