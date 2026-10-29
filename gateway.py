import os

import httpx
from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI(title="Japanese Voice Gateway")

HTML_FILE = Path(__file__).with_name("index.html")

@app.get("/")
async def index():
    return FileResponse(HTML_FILE)

ASR_BASE_URL = os.getenv(
    "ASR_BASE_URL",
    "http://127.0.0.1:8002"
)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "asr_url": ASR_BASE_URL
    }


@app.post("/asr/start")
async def asr_start():
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{ASR_BASE_URL}/api/start"
            )

            response.raise_for_status()

            return response.json()

    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"ASR server error: {exc}"
        )



@app.post("/asr/chunk")
async def asr_chunk(session_id: str, request: Request):
    audio_bytes = await request.body()

    if not audio_bytes:
        raise HTTPException(
            status_code=400,
            detail="Empty audio chunk"
        )

    if len(audio_bytes) % 4 != 0:
        raise HTTPException(
            status_code=400,
            detail="Audio must be float32 PCM"
        )

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{ASR_BASE_URL}/api/chunk",
                params={"session_id": session_id},
                content=audio_bytes,
                headers={
                    "Content-Type": "application/octet-stream"
                }
            )

            response.raise_for_status()
            return response.json()

    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"ASR chunk error: {exc}"
        )

@app.post("/asr/finish")
async def asr_finish(session_id: str):
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{ASR_BASE_URL}/api/finish",
                params={"session_id": session_id}
            )

            response.raise_for_status()
            return response.json()

    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"ASR finish error: {exc}"
        )

from fastapi.responses import StreamingResponse

LLM_RELAY_URL = "http://127.0.0.1:8003/respond"

@app.post("/llm")
async def llm(request: Request):
    payload = await request.json()

    async def generate():
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                LLM_RELAY_URL,
                json=payload
            ) as response:
                response.raise_for_status()

                async for chunk in response.aiter_bytes():
                    yield chunk

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )