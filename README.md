# Voice Bot Library

This project provides a streamlined library to transform LLM-based chatbots into voice bots with minimal latency. It leverages Deepgram for Speech-to-Text (STT) and OpenAI for both Large Language Model (LLM) responses and Text-to-Speech (TTS).

## Features

- **Speech-to-Text (STT):**  
  Uses Deepgram's streaming STT API to convert microphone audio into text.

- **LLM Interaction:**  
  Processes the transcript using OpenAI's LLM (e.g., GPT-4o-mini) to generate concise responses.

- **Text-to-Speech (TTS):**  
  Converts the LLM response into speech using OpenAI's TTS API.

- **Low-Latency Streaming:**  
  Streams both audio input and output in real time with built-in pause/resume functionality to prevent echo.

- **Observability:**  
  Collects performance metrics, including:
  - Total time for STT post user stopped speaking. [ Pending IMPL ]
  - Time for first token from LLM. [ Pending IMPL ]
  - Time for complete response from LLM.
  - Total time from when the user stopped speaking until TTS generates the first speech. [ Pending IMPL ]

- **Graceful Shutdown:**  
  The conversation ends if the user says "goodbye".

## Prerequisites

- **Python 3.10+**
- **Deepgram API Key:** Required for accessing Deepgram’s STT API.
- **OpenAI API Key:** Required for accessing OpenAI’s LLM and TTS APIs.

## Setup

### 1. Clone the Repository

```bash
git clone repo-url
cd voice-bot-v2
```

### 3. Install Dependencies
Install the required dependencies using the provided requirements.txt:

```
pip install -r requirements.txt
```

## How It Works
### Audio Input:
The project uses PyAudio to capture microphone input and streams the audio to Deepgram’s STT API.

#### Speech-to-Text Processing:
Deepgram processes the audio stream and returns final transcripts.
Observability: The system logs the time from when the user stops speaking until the final transcript is received.

LLM Interaction:
The transcript is sent to OpenAI’s LLM (with a predefined system prompt) to generate a reply.
Observability: Metrics are recorded for the full LLM response time and the delay until the first token is received.

Text-to-Speech (TTS):
The LLM reply is converted into speech using OpenAI’s TTS API and streamed to the speakers.
Observability: Metrics are logged for TTS streaming time and the delay from LLM response completion to the first audio chunk.

Ending the Conversation:
If the user says "goodbye" in their speech, the system detects this keyword and gracefully ends the conversation.

Performance Metrics:
At the end of the conversation, the application prints a comprehensive performance metrics report.

Project Structure
graphql
Copy
voice_bot/
├── adapters/
│   ├── __init__.py          # (Optional: can be empty)
│   ├── stt_deepgram.py      # Deepgram STT adapter
│   ├── llm_openai.py        # OpenAI LLM adapter
│   └── tts_openai.py        # OpenAI TTS adapter
├── streams/
│   ├── __init__.py          # (Optional: can be empty)
│   ├── input_stream.py      # Input stream abstraction using PyAudio
│   └── output_stream.py     # Output stream abstraction using PyAudio
├── config.py                # Configuration and setup for the bot
├── conversation.py          # Conversation manager orchestrating STT, LLM, TTS and metrics logging
├── metrics.py               # Metrics logger (singleton) for observability
├── cli.py                   # Command-line interface to run the conversation
├── requirements.txt         # Required dependencies
└── README.md                # This file
