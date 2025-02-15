import asyncio
from openai import OpenAI

class OpenAILLMAdapter:
    """
    Adapter for querying the OpenAI LLM (e.g., GPT-4o-mini).
    """
    def __init__(self, api_key: str, system_prompt: str, model: str = "gpt-4o-mini-2024-07-18"):
        self.client = OpenAI(api_key=api_key)
        self.system_prompt = system_prompt
        self.model = model

    async def query(self, conversation: list[dict]) -> str:
        """
        Given a conversation history (list of messages), query the LLM and return the reply text.
        """
        messages = [{"role": "system", "content": self.system_prompt}] + conversation
        loop = asyncio.get_running_loop()
        # The OpenAI client call is synchronous; we wrap it in an executor.
        response = await loop.run_in_executor(
            None,
            lambda: self.client.chat.completions.create(model=self.model, messages=messages)
        )
        reply = response.choices[0].message.content
        return reply
