
import os
from openai import OpenAI

client = OpenAI(
    base_url=os.environ["LLM_BASE_URL"],
    api_key=os.getenv("LLM_API_KEY", "EMPTY"),
    timeout=60.0,
)

model_name = client.models.list().data[0].id

SYSTEM_PROMPT = """
あなたは日本語の電話対応AIアシスタントです。
自然で丁寧な日本語で回答してください。
回答は短く、話し言葉にしてください。
わからないことは推測せず、確認してください。
"""

def generate_response(transcription, history=None):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *(history or []),
        {"role": "user", "content": transcription},
    ]

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.3,
        max_tokens=160,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    transcription = "こんにちは。営業時間を教えてください。"

    answer = generate_response(transcription)

    print("ASR:", transcription)
    print("LLM:", answer)
