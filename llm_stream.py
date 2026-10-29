
import os
from openai import OpenAI

client = OpenAI(
    base_url=os.environ["LLM_BASE_URL"],
    api_key=os.getenv("LLM_API_KEY", "EMPTY"),
    timeout=60.0,
)

MODEL = client.models.list().data[0].id

SYSTEM_PROMPT = (
    "あなたは日本語の音声アシスタントです。"
    "自然で簡潔な日本語で回答してください。"
)

def stream_llm(transcription, history=None):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *(history or []),
        {"role": "user", "content": transcription},
    ]

    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=160,
        temperature=0.3,
        stream=True,
    )

    full_answer = ""

    for event in stream:
        delta = event.choices[0].delta.content
        if delta:
            full_answer += delta
            yield delta

    return full_answer


if __name__ == "__main__":
    print("A40 response: ", end="", flush=True)

    for token in stream_llm("こんにちは。自己紹介してください。"):
        print(token, end="", flush=True)

    print()
