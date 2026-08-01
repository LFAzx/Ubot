import os
import asyncio
from groq import Groq

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

_client = Groq(api_key=GROQ_API_KEY)


def _ask_ai_sync(prompt: str) -> str:
    completion = _client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.7,
    )
    return completion.choices[0].message.content


async def ask_ai(prompt: str) -> str:
    """Groq's SDK is sync, so run it in a thread to avoid blocking the event loop."""
    return await asyncio.to_thread(_ask_ai_sync, prompt)

