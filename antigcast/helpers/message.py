from pyrogram.types import Message
from pyrogram import filters
import os

# Baca isi blacklist dari file bl.txt saat modul di-load
BLACKLIST_WORDS = []
bl_path = os.path.join(os.path.dirname(__file__), "bl.txt")
if os.path.exists(bl_path):
    with open(bl_path, encoding="utf-8") as f:
        BLACKLIST_WORDS = [line.strip().lower() for line in f if line.strip()]

async def isGcast(_, __, message: Message) -> bool:
    if not message.text:
        return False

    text = message.text.lower()
    return any(word in text for word in BLACKLIST_WORDS)

# Filter siap pakai
Gcast = filters.create(isGcast)
