# streams/input_stream.py

import asyncio
import pyaudio

class PyAudioInputStream:
    def __init__(self, stream: pyaudio.Stream):
        self.stream = stream
        self.__pause_event = asyncio.Event()
        self.__pause_event.set()

    def pause(self):
        """
        Pauses the input stream.
        """
        self.__pause_event.clear()
    
    def resume(self):
        """
        Resumes the input stream.
        """
        self.__pause_event.set()

    async def read(self, chunk_size: int) -> bytes:
        """
        Asynchronously reads audio data from the PyAudio stream.
        """
        await self.__pause_event.wait()
        loop = asyncio.get_running_loop()
        # Run the blocking read call in an executor
        return await loop.run_in_executor(None, self.stream.read, chunk_size)

def create_input_stream(sample_rate: int, chunk_size: int) -> PyAudioInputStream:
    """
    Creates a PyAudio input stream wrapped in our PyAudioInputStream class.
    """
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size,
    )
    return PyAudioInputStream(stream)
