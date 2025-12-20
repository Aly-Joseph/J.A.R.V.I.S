from livekit import rtc
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def start_livekit():
    room = rtc.Room()
    await room.connect(
        os.getenv("LIVEKIT_URL"),
        token=os.getenv("LIVEKIT_TOKEN")
    )
    print("🎧 LiveKit connected")

asyncio.run(start_livekit())
