from dotenv import load_dotenv
import os
from livekit import agents
from livekit.agents import Agent, AgentSession, RoomInputOptions, tokenize
from livekit.plugins import (
    assemblyai,
    noise_cancellation,
    groq,
    openai,
    silero,
)

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice AI assistant.")


def get_llm_provider(provider: str):
    """Get LLM provider based on user choice"""
    if provider.lower() == "groq":
        return groq.LLM(model="llama3-8b-8192")
    else:  # default to openai
        return openai.LLM(model="gpt-4o-mini")


def get_tts_provider(provider: str):
    """Get TTS provider based on user choice"""
    if provider.lower() == "groq":
        return groq.TTS()
    else:  # default to openai
        return openai.TTS(voice="alloy")


async def entrypoint(ctx: agents.JobContext):
    # Get provider from environment variable or use default
    provider = os.getenv("PROVIDER", "openai").lower()
    
    # We'll use the selected provider's Text To Speech (TTS) service
    tts = agents.tts.StreamAdapter(
        tts=get_tts_provider(provider),
        sentence_tokenizer=tokenize.basic.SentenceTokenizer(),
    )

    # We'll use AssemblyAI's Speech To Text (STT) service to transform
    # our voice into text.
    stt = assemblyai.STT(
        end_of_turn_confidence_threshold=0.7,
        min_end_of_turn_silence_when_confident=160,
        max_turn_silence=2400,
    )

    # We'll use Silero's Voice Activity Detector (VAD) service to determine
    # whether an audio signal contains human speech or not.
    vad = silero.VAD.load()

    # We'll use the selected provider's LLM as the assistant
    llm = get_llm_provider(provider)

    # We'll use AssemblyAI's turn detection capabilities to determine when
    # we stop speaking and it's the assistant's turn.
    turn_detection = "stt"

    session = AgentSession(
        tts=tts,
        stt=stt,
        vad=vad,
        llm=llm,
        turn_detection=turn_detection,
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
