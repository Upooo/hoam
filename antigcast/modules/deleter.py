import asyncio
import re
from typing import Optional
from functools import lru_cache
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.errors import UserNotParticipant, MessageDeleteForbidden, RPCError, FloodWait
from antigcast.helpers.message import Gcast
from antigcast import Bot
from antigcast.config import *
from antigcast.helpers.tools import *
from antigcast.helpers.admins import Admin
from antigcast.helpers.database import *

# Regex untuk deteksi emoji dan pesan aneh
EMOJI_PATTERN = re.compile(r'[\U0001F000-\U0001F9FF\u200d\u2600-\u26FF\u2700-\u27BF]')
GIBBERISH_PATTERNS = [
    re.compile(r'[<>]'),
    re.compile(r'\b(\w)\1{2,}\b'),
    re.compile(r'\b[A-Z\s]{4,}\b'),
    re.compile(r'@\w+'),
    re.compile(r'(\b\w\b\s)+'),
    re.compile(r'[\u0080-\uFFFF]{10,}'),
    re.compile(r'\b\w+\W+\w+\W+\w+\b')
]

@lru_cache(maxsize=1000)
def is_emoji(text: str) -> bool:
    return bool(EMOJI_PATTERN.match(text)) or len(EMOJI_PATTERN.findall(text)) > 3

@lru_cache(maxsize=1000)
def jaccard_similarity(str1: str, str2: str) -> float:
    set1, set2 = set(str1.lower().split()), set(str2.lower().split())
    return len(set1 & set2) / len(set1 | set2) if set1 | set2 else 0

def is_gibberish(text: str) -> bool:
    if not text:
        return True
    if text.isupper() and len(text) > 3:
        return True
    if text.startswith("||") and text.endswith("||"):
        return True
    if any(ord(char) > 127 and not is_emoji(char) for char in text):
        return True
    if sum(1 for char in text if '\u0300' <= char <= '\u036F') > len(text) * 0.3:
        return True
    return any(p.search(text) for p in GIBBERISH_PATTERNS)

async def is_blacklist(text: str) -> Optional[str]:
    blacklist_data = await get_bl_words()
    for word in blacklist_data:
        keyword = word.lower()
        if re.search(fr"\b{re.escape(keyword)}\b", text, re.IGNORECASE):
            return keyword
    return None


@Bot.on_message(filters.command("ankes") & filters.group & Admin, group=1)
async def handler_command(client: Client, message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("Gunakan: /ankes on atau /ankes off")

    status = args[1].lower()
    if status == "on":
        await set_state(message.chat.id, True)
        await message.reply("✅ Ankes diaktifkan.")
    elif status == "off":
        await set_state(message.chat.id, False)
        await message.reply("❌ Ankes dinonaktifkan.")
    else:
        await message.reply("Argumen tidak valid. Gunakan 'on' atau 'off'.")

@Bot.on_message(filters.command("superankes") & filters.group & Admin, group=2)
async def handler_command(client: Client, message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("Gunakan: /superankes on atau /superankes off")

    status = args[1].lower()
    if status == "on":
        await set_superankes_state(message.chat.id, True)
        await message.reply("✅ Super ankes diaktifkan.")
    elif status == "off":
        await set_superankes_state(message.chat.id, False)
        await message.reply("❌ Super ankes dinonaktifkan.")
    else:
        await message.reply("Argumen tidak valid. Gunakan 'on' atau 'off'.")

async def is_replying_admin(client : Client, message: Message) -> bool:
    if not message.reply_to_message:
        return False
    replied_user = message.reply_to_message.from_user
    if not replied_user:
        return False
    try:
        STATUS = enums.ChatMemberStatus
        member = await client.get_chat_member(message.chat.id, replied_user.id)
        return member.status in [STATUS.OWNER, STATUS.ADMINISTRATOR]
    except:
        return False

@Bot.on_message(filters.group & filters.incoming, group=3)
async def handle_superankes(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Cek status SuperAnkes
    if not await get_superankes_state(chat_id):
        return

    # Jangan hapus jika admin
    member = await client.get_chat_member(chat_id, user_id)
    STATUS = enums.ChatMemberStatus
    if member.status in [STATUS.OWNER, STATUS.ADMINISTRATOR]:
        return

    # Jangan hapus jika termasuk TEAM_IDOL
    if user_id in TEAM_IDOL:
        return

    # Jangan hapus jika reply ke admin
    if await is_replying_admin(client, message):
        return

    # Hapus pesan selain di atas
    try:
        await message.delete()
    except:
        pass


@Bot.on_message(filters.group & filters.incoming & Gcast, group=4)
async def message_handler(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Cek status fitur (aktif/nonaktif) via state
    state = await get_state(chat_id)
    if not state:
        return  # Fitur dimatikan untuk grup ini
    
    if user_id in TEAM_IDOL:
        return
    
    # Cek apakah admin
    member = await client.get_chat_member(chat_id, user_id)
    STATUS = enums.ChatMemberStatus
    if member.status in [STATUS.OWNER, STATUS.ADMINISTRATOR]:
        return  # Jangan hapus pesan admin

    # Cek apakah user sudah di-approve
    if await is_free_user(chat_id, user_id):  # ✅ Pastikan fungsi ini tersedia
        return  # Jangan hapus pesan user yang di-whitelist

    try:
        # Hapus pesan dan kirim notifikasi sementara
        await message.delete()
        notice = await client.send_message(
            chat_id,
            f"<blockquote><b>🚫 Pesan dari anak anjeng {message.from_user.mention} berhasil dihapus karna typingan nya jamet.</b></blockquote>"
        )
        await asyncio.sleep(2)
        await notice.delete()

    except MessageDeleteForbidden:
        # Tidak punya izin, keluar dari grup
        try:
            await message.reply("Bot tidak memiliki izin menghapus pesan. Meninggalkan grup dalam 5 detik.")
            await asyncio.sleep(5)
            await client.leave_chat(chat_id)
        except RPCError:
            pass

@Bot.on_message(filters.command("addbl") & filters.group & Admin, group=5)
async def addbl_message(client: Client, message: Message):
    trigger = get_arg(message) or (message.reply_to_message.text if message.reply_to_message else "")
    if not trigger:
        return await message.reply("Tidak ada teks untuk ditambahkan ke blacklist.")

    proses = await message.reply(f"Menambahkan `{trigger}` ke blacklist...")
    try:
        await add_bl_word(trigger.lower())
        await proses.edit(f"✅ `{trigger}` berhasil ditambahkan ke blacklist.")
    except Exception as e:
        await proses.edit(f"❌ Gagal menambahkan: `{e}`")

    await asyncio.sleep(5)
    await proses.delete()
    await message.delete()

@Bot.on_message(filters.command("delbl") & filters.group & Admin, group=6)
async def delbl_message(client: Client, message: Message):
    trigger = get_arg(message) or (message.reply_to_message.text if message.reply_to_message else "")
    if not trigger:
        return await message.reply("Tidak ada teks untuk dihapus dari blacklist.")

    proses = await message.reply(f"Menghapus `{trigger}` dari blacklist...")
    try:
        await remove_bl_word(trigger.lower())
        await proses.edit(f"✅ `{trigger}` berhasil dihapus dari blacklist.")
    except Exception as e:
        await proses.edit(f"❌ Gagal menghapus: `{e}`")

    await asyncio.sleep(5)
    await proses.delete()
    await message.delete()

@app.on_message(filters.command("acc") & filters.group, group=7)
async def addfree_command(client: Client, message: Message):
    admin = await client.get_chat_member(message.chat.id, message.from_user.id)
    if admin.status not in [CMS.OWNER, CMS.ADMINISTRATOR] and message.from_user.id != OWNER_ID:
        return
    chat_id = message.chat.id
    reply_message = message.reply_to_message
    if not reply_message:
        return await message.reply("Please reply to the user to be approved!")
    
    sender_id = reply_message.from_user.id
    grup_id = message.chat.id
    
    success = await add_free_user(grup_id, sender_id)
    text = f"User: {reply_message.from_user.mention}\nSuccessfully approved!" if success else f"User: {reply_message.from_user.mention}\nIt's been approved."
    await client.send_message(chat_id,text)


@Bot.on_message(filters.command("unacc") & filters.group, group=8)
async def delfree_command(client: Client, message: Message):
    admin = await client.get_chat_member(message.chat.id, message.from_user.id)
    if admin.status not in [CMS.OWNER, CMS.ADMINISTRATOR] and message.from_user.id != OWNER_ID:
        return
    chat_id = message.chat.id
    
    reply_message = message.reply_to_message
    if not reply_message:
        return await message.reply("Please reply to user!")
    
    sender_id = reply_message.from_user.id
    grup_id = message.chat.id
    
    success = await delete_free_user(grup_id, sender_id)
    text = f"User: {reply_message.from_user.mention}\nRemoved from approve list!" if success else f"User: {reply_message.from_user.mention}\nNot on the approved list!"
    await client.send_message(chat_id,text)
    return

@Bot.on_message(filters.command("approved") & filters.group, group=9)
async def getfree_command(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return
    
    chat_id = message.chat.id
    blacklist_data = await get_free_user(chat_id)
    
    if not blacklist_data:
        return await message.reply("There is no list of approved users!")
    
    blacklist_text = "\n".join(f"{i+1}. {data['user_id']}" for i, data in enumerate(blacklist_data))
    text = f"List of approved users in this group:\n\n{blacklist_text}"
    await client.send_message(chat_id,text)
