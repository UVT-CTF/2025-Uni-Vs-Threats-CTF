import os
import random
import logging
from typing import List

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ─── Logging Setup ─────────────────────────────────────────────────────────────
logger = logging.getLogger("uvt_ctf")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ─── App Initialization ────────────────────────────────────────────────────────
app = FastAPI(
    title="UVT CTF 2025 API",
    version="1.0.0",
    description="Simple backend for UVT CTF with jokes, contest info, and flag retrieval"
)

# ─── CORS (if you need it) ─────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔒 In production, lock this down to your frontend URL(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Response Models ───────────────────────────────────────────────────────────
class JokeResponse(BaseModel):
    id: int
    joke: str

class CTFInfo(BaseModel):
    name: str
    year: int
    description: str
    url: str

class FlagResponse(BaseModel):
    flag: str

# ─── In-Memory Data ────────────────────────────────────────────────────────────
JOKES: List[str] = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "I told my computer I needed a break, and it said 'No problem – I'll go to sleep.'",
    "Why did the developer go broke? Because he used up all his cache."
]

CTF_INFO = CTFInfo(
    name="uvt_ctf_2025",
    year=2025,
    description="Capture-The-Flag contest hosted by UVT students",
    url="https://cybersec.uvt.ro/events/UniVsThreats25/"
)

# Fetch the real flag from an environment variable, fallback to a placeholder
FLAG = os.getenv("CTF_FLAG", "UVT{m0b1l3_.s0_m4y_c0nt4in_s3ns1tiv3_1nf0}")

# ─── Endpoints ────────────────────────────────────────────────────────────────

@app.get(
    "/jokes",
    response_model=JokeResponse,
    summary="Get a random programming joke"
)
async def get_random_joke():
    """Return a random programming joke."""
    idx = random.randrange(len(JOKES))
    joke = JOKES[idx]
    logger.info(f"Served joke #{idx}")
    return JokeResponse(id=idx, joke=joke)

@app.get(
    "/uvt-ctf",
    response_model=CTFInfo,
    summary="Get UVT CTF contest information"
)
async def get_ctf_info():
    """Return information about the UVT CTF contest."""
    logger.info("Served CTF info")
    return CTF_INFO

@app.get(
    "/somebody-found-a-random-flag-path",
    response_model=FlagResponse,
    summary="Retrieve the CTF flag"
)
async def get_flag():
    """Return the CTF flag (must be in UVT{…} format)."""
    logger.warning("Flag endpoint accessed")
    if not FLAG.startswith("UVT{") or not FLAG.endswith("}"):
        logger.error("Flag is improperly formatted")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Flag not properly configured on the server"
        )
    return FlagResponse(flag=FLAG)
