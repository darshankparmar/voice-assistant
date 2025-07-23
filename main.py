from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, RoomInputOptions, tokenize
from livekit.plugins import (
    assemblyai,
    noise_cancellation,
    openai,
    silero,
)

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice AI assistant.")


async def entrypoint(ctx: agents.JobContext):
    # We'll use OpenAI's Text To Speech (TTS) servive to transform text
    # into the assistant's voice.
    tts = agents.tts.StreamAdapter(
        tts=openai.TTS(voice="alloy"),
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

    # We'll use OpenAI's GPT-4o-mini as the assistant that will drive the
    # conversation.
    llm = openai.LLM(model="gpt-4o-mini")

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
