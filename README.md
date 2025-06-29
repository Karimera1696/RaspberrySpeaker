# SmartSpeaker2

Local smart-speaker pipeline: Wake-word → STT → LLM → Home Assistant (MCP) → TTS.

## Quick Start
```bash
git clone https://github.com/Karimera1696/SmartSpeaker2
cp .env.example .env   # fill HOSTs / tokens
poetry install
poetry run python -m smartspeaker2
```

## Architecture
```
[Mic] → Porcupine → Whisper → OpenAI (functions) → MCP Client → HA → Voicevox
```

## Roadmap
* [x] Dummy pipeline (PoC)
* [ ] Porcupine integration   ← Now
* [ ] MCP server docs
* [ ] Docker compose (dev)