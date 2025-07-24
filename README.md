# Voice Assistant

This is an example voice assistant using [LiveKit](https://www.livekit.io/), [AssemblyAI](http://bit.ly/46oN8MT), and [OpenAI](https://www.openai.com/).

To set up the project, create a file `.env` in the root directory with the following environment variables:

```
LIVEKIT_URL=...
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...
ASSEMBLYAI_API_KEY=...
OPENAI_API_KEY=...
```

This project uses [`uv`](https://docs.astral.sh/uv/). You can run the assistant by executing the following commands:

```
$ uv run python main.py download-files
$ uv run python main.py console
```
