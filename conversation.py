# conversation.py
import asyncio
from datetime import datetime
from config import BotConfig
from adapters.stt_deepgram import DeepgramSTTAdapter
from adapters.llm_openai import OpenAILLMAdapter
from adapters.tts_openai import OpenAITTSAdapter
from metrics import logger  # Singleton metrics logger

async def stream_conversation(input_stream, output_stream, config: BotConfig):
    """
    Orchestrates a full conversation:
      1. Streams audio from the input stream to Deepgram STT.
      2. Accumulates final transcripts and updates conversation history.
      3. Sends the conversation (plus system prompt) to the LLM and gets a reply.
      4. Converts the LLM reply to speech via TTS and streams the audio to the output.
      5. Ends the conversation if a "goodbye" keyword is detected.
      6. Collects performance metrics.
    """
    # Initialize adapters using configuration values.
    stt_adapter = DeepgramSTTAdapter(api_key=config.stt.api_key)
    llm_adapter = OpenAILLMAdapter(api_key=config.llm.api_key, system_prompt=config.llm.system_prompt)
    tts_adapter = OpenAITTSAdapter(api_key=config.tts.api_key)

    conversation_history = []  # List of messages

    print("ℹ️  Starting conversation stream. Speak into your microphone.")

    # Loop over final transcripts from the STT adapter.
    async for transcript in stt_adapter.stream_transcription(input_stream):
        
        if not transcript.strip():
            # Use this somehow as user stoped speaking here
            # if transcript is empty implies user is not speaking
            # if prev transcript is not empty implies user stopped speaking just now
            continue

        # Check for exit keyword.
        if "goodbye" in transcript.lower():
            print("👋 Goodbye detected. Ending conversation.")
            break

        print(f"🗣️  Final transcript received: {transcript}")
        conversation_history.append({"role": "user", "content": transcript})

        # Pause input to avoid capturing TTS playback.
        input_stream.pause()

        # ===== LLM Metrics =====
        # Start overall LLM timer.
        logger.start("LLM_Complete_Response_Time")
        try:
            reply = await llm_adapter.query(conversation_history)
        except Exception as e:
            print(f"Error querying LLM: {e}")
            input_stream.resume()
            continue
        logger.stop("LLM_Complete_Response_Time")
        print(f"🤖  LLM Reply: {reply}")
        conversation_history.append({"role": "assistant", "content": reply})
        logger.report_metric("LLM_Complete_Response_Time")

        # ===== TTS Metrics =====
        tts_first = False
        try:
            async for audio_chunk in tts_adapter.stream_audio(reply):
                if not tts_first:
                    # Mark the time when TTS outputs its first chunk.
                    # logger.stop("User_Stopped_Speaking_To_TTS_First_Speech")
                    # logger.report_metric("User_Stopped_Speaking_To_TTS_First_Speech")
                    tts_first = True
                output_stream.write(audio_chunk)
        except Exception as e:
            print(f"Error during TTS streaming: {e}")
        
        # Resume input stream after TTS playback.
        input_stream.resume()
        prev_transcript = transcript
