import asyncio
from typing import AsyncIterator
from openai import OpenAI

class OpenAITTSAdapter:
    """
    Adapter for converting text to speech using OpenAI's TTS API.
    """
    def __init__(self, api_key: str, model: str = "tts-1", voice: str = "nova", response_format: str = "wav"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.voice = voice
        self.response_format = response_format

    async def stream_audio(self, text: str) -> AsyncIterator[bytes]:
        """
        Given input text, returns an async iterator yielding chunks of audio data (bytes).
        """
        loop = asyncio.get_running_loop()

        def tts_call():
            return self.client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                input=text,
                response_format=self.response_format,
            )

        response = await loop.run_in_executor(None, tts_call)
        # Wrap the synchronous iterator in an async generator.
        for chunk in response.iter_bytes(chunk_size=1024):
            yield chunk
