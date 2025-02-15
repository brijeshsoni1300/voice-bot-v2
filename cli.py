# cli.py
import argparse
import asyncio
from config import STTConfig, TTSConfig, LLMConfig, setup_bot
from conversation import stream_conversation
from streams.input_stream import create_input_stream
from streams.output_stream import create_output_stream
from metrics import logger

def parse_args():
    parser = argparse.ArgumentParser(
        description="Voice Bot CLI: Stream conversation using Deepgram STT and OpenAI LLM/TTS."
    )
    parser.add_argument("--dp-key", required=True, help="Deepgram API key")
    parser.add_argument("--ooi-key", required=True, help="OpenAI API key (for LLM and TTS)")
    return parser.parse_args()

async def main():
    args = parse_args()

    # Create configuration objects.
    stt_config = STTConfig(engine="deepgram", api_key=args.dp_key)
    tts_config = TTSConfig(engine="openai", api_key=args.ooi_key)
    llm_config = LLMConfig(
        engine="openai",
        api_key=args.ooi_key,
        system_prompt="Answer in less then 15 words\n\n"
    )

    # Setup the bot configuration context.
    bot_config = setup_bot(stt_config, tts_config, llm_config)

    # Create the audio input and output streams.
    # (Adjust sample rates and chunk sizes as needed.)
    input_stream = create_input_stream(sample_rate=16000, chunk_size=8000)
    output_stream = create_output_stream(sample_rate=24000)
    
    # Start the conversation.
    await stream_conversation(input_stream, output_stream, bot_config)


if __name__ == "__main__":
    asyncio.run(main())
