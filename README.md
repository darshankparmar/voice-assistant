# Voice Assistant

This is an example voice assistant using [LiveKit](https://www.livekit.io/), [AssemblyAI](http://bit.ly/46oN8MT), and either [OpenAI](https://www.openai.com/) or [Groq](https://groq.com/).

To set up the project, create a file `.env` in the root directory with the following environment variables:

```
LIVEKIT_URL=...
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...
ASSEMBLYAI_API_KEY=...
OPENAI_API_KEY=...  # Required if using OpenAI
GROQ_API_KEY=...    # Required if using Groq
PROVIDER=openai     # Choose: "openai" or "groq" (default: openai)
```

## Important: Groq Model Terms Acceptance

If you choose to use Groq, you need to accept the terms for the Groq models used:

1. **TTS Model**: Visit [Groq Console - PlayAI TTS](https://console.groq.com/playground?model=playai-tts) and accept the terms for the `playai-tts` model
2. **LLM Model**: The `llama3-8b-8192` model should work without additional terms acceptance, but if you encounter similar errors, check the [Groq Console](https://console.groq.com/) for any required terms acceptance

## Usage

This project uses [`uv`](https://docs.astral.sh/uv/). You can run the assistant by executing the following commands:

### Download required files (first time only):
```
$ uv run python main.py download-files
```

### Run the voice assistant:

**Using OpenAI (default):**
```
$ uv run python main.py console
```

**Using Groq:**
```
$ set PROVIDER=groq && uv run python main.py console
```

**Using OpenAI explicitly:**
```
$ set PROVIDER=openai && uv run python main.py console
```

## Provider Comparison

| Feature | OpenAI | Groq |
|---------|--------|------|
| **LLM Model** | GPT-4o-mini | Llama3-8b-8192 |
| **TTS Voice** | Alloy | Arista-PlayAI |
| **Speed** | Standard | Very Fast |
| **Cost** | Higher | Lower |
| **Terms Required** | No | Yes (for TTS) |
