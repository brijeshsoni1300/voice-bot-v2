# streams/output_stream.py

import pyaudio


class PyAudioOutputStream:
    def __init__(self, stream: pyaudio.Stream):
        self.stream = stream

    def write(self, b: bytes) -> None:
        """
        Writes audio data to the PyAudio output stream.
        """
        self.stream.write(b)

def create_output_stream(sample_rate: int) -> PyAudioOutputStream:
    """
    Creates a PyAudio output stream wrapped in our PyAudioOutputStream class.
    """
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate,
        output=True,
    )
    return PyAudioOutputStream(stream)
