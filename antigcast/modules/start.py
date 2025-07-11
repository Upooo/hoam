import asyncio

from antigcast import Bot
from pyrogram import filters, enums
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from antigcast.config import *
from antigcast.helpers.database import *


CTYPE = enums.ChatType

# inline buttons
inlinegc = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="ᴄʀᴇᴀᴛᴏʀ", url="https://t.me/nathanidol"),
            InlineKeyboardButton(text="ᴄʜᴀɴɴᴇʟ", url="https://t.me/xnxxnathan")
        ]
    ]
)

inline = InlineKeyboardMarkup(
    [
        [
                    InlineKeyboardButton(text="Tambahkan Ke Group", url=f"https://t.me/idolankesbot?startgroup=true")
        ],
        [
                    InlineKeyboardButton(text="ᴄʀᴇᴀᴛᴏʀ", url=f"http://t.me/nathanidol"),
                    InlineKeyboardButton(text="ᴄʜᴀɴɴᴇʟ", url="https://t.me/xnxxnathan")
        ]
    ]
)

def add_panel(username):
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Tambahkan Ke Group", url=f"http://t.me/{username}?startgroup=appstart")
            ]
        ]
    )

    return button

def admin_panel():
    buttons = [
        [
            InlineKeyboardButton(text="Hubungi Admin", url=f"http://t.me/nathanidol")
        ],
    ]

    return buttons

@Bot.on_message(filters.command("start"))
async def start_msgmessag(app : Bot, message : Message):
    bot = await app.get_me()
    username = bot.username
    user = message.from_user.mention
    chat_type = message.chat.type
    if chat_type == CTYPE.PRIVATE:
        msg = f"👋🏻 Hi {user}!\n\nBot ini akan menghapus otomatis pesan gcast yang mengganggu di group. Tambahkan bot sebagai admin agar bisa berjalan dengan baik."
        try:
            await message.reply(text=msg, reply_markup=inline)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply(text=msg, reply_markup=inline)
    elif chat_type == CTYPE.SUPERGROUP:
        msg = f"**Hey!**\n\n__Jadikan saya sebagai admin group, maka group ini tidak akan ada spam gcast yang mengganggu!__\n\nCreated by @nathanidol"
        
        try:
            await message.reply(text=msg, reply_markup=inlinegc)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply(text=msg, reply_markup=inlinegc)