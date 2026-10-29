
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from llm_stream import stream_llm

app = FastAPI()

class Transcription(BaseModel):
    text: str

@app.post("/respond")
def respond(data: Transcription):
    def events():
        try:
            for token in stream_llm(data.text):
                yield "data: " + json.dumps(
                    {"token": token}, ensure_ascii=False
                ) + "\n\n"

            yield 'data: {"done": true}\n\n'

        except Exception as exc:
            yield "data: " + json.dumps(
                {"error": str(exc)}
            ) + "\n\n"

    return StreamingResponse(
        events(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )
