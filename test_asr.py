import numpy as np
import soundfile as sf
import httpx

from scipy.signal import resample_poly
from math import gcd

BASE_URL = "http://127.0.0.1:8004"
AUDIO_FILE = "japanese.wav"
TARGET_SR = 16000
CHUNK_SEC = 0.5

# Load audio
audio, sr = sf.read(AUDIO_FILE, dtype="float32")

# Stereo -> mono
if audio.ndim == 2:
    audio = audio.mean(axis=1)

# Resample -> 16 kHz
if sr != TARGET_SR:
    divisor = gcd(sr, TARGET_SR)

    audio = resample_poly(
        audio,
        TARGET_SR // divisor,
        sr // divisor
    )

audio = np.ascontiguousarray(audio, dtype=np.float32)

print(f"Audio duration: {len(audio) / TARGET_SR:.2f}s")

# Start session
with httpx.Client(timeout=120.0) as client:

    response = client.post(f"{BASE_URL}/asr/start")
    response.raise_for_status()

    session_id = response.json()["session_id"]
    print("Session:", session_id)

    chunk_size = int(TARGET_SR * CHUNK_SEC)

    # Stream audio sequentially
    for start in range(0, len(audio), chunk_size):
        chunk = audio[start:start + chunk_size]

        response = client.post(
            f"{BASE_URL}/asr/chunk",
            params={"session_id": session_id},
            content=chunk.tobytes(),
            headers={
                "Content-Type": "application/octet-stream"
            }
        )

        response.raise_for_status()

        result = response.json()

        print(
            f"Partial [{start / TARGET_SR:.1f}s]:",
            result.get("text", "")
        )

    # Finalize
    response = client.post(
        f"{BASE_URL}/asr/finish",
        params={"session_id": session_id}
    )

    response.raise_for_status()

    print("\nFINAL:", response.json())