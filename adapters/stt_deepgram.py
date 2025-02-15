import asyncio
import json
import websockets
from typing import AsyncIterator
import numpy as np

# Global chunk size for reading from the input stream
CHUNK = 16000

class DeepgramSTTAdapter:
    """
    Adapter for Deepgram's streaming STT API.
    """
    def __init__(self, api_key: str, url: str = "wss://api.deepgram.com/v1/listen?punctuate=true&encoding=linear16&sample_rate=16000&model=general"):
        self.api_key = api_key
        self.url = url

    async def stream_transcription(self, input_stream) -> AsyncIterator[str]:
        """
        Reads audio from an InputStream (with an async read method) and yields
        final transcript strings from Deepgram.
        """
        async with websockets.connect(self.url, extra_headers={"Authorization": f"Token {self.api_key}"}) as ws:
            async def sender():
                while True:
                    chunk = await input_stream.read(CHUNK)
                    if not chunk:
                        break

                    await ws.send(chunk)
                # Signal end-of-stream to Deepgram
                await ws.send(json.dumps({"type": "CloseStream"}))

            asyncio.create_task(sender())

            async for message in ws:
                data = json.loads(message)
                # Check if this message is a final transcript
                if data.get("is_final"):
                    transcript = data.get("channel", {}).get("alternatives", [{}])[0].get("transcript", "")
                    yield transcript
