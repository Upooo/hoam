import random
from asyncio import sleep

import asyncio

from antigcast import app
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserNotParticipant

from antigcast.config import *

STATUS = ChatMemberStatus
spam_chats = []
emoji = "😀 😃 😄 😁 😆 😅 😂 🤣 😭 😗 😙 😚 😘 🥰 😍 🤩 🥳 🤗 🙃 🙂 😊 😏 😌 😉 🤭 😶 😐 😑 😔 😋 😛 😝 😜 🤪 🤔 🤨 🧐 🙄 😒 😤 😠 🤬 ☹️ 🙁 😕 😟 🥺 😳 😬 🤐 🤫 😰 😨 😧 😦 😮 😯 😲 😱 🤯 😢 😥 😓 😞 😖 😣 😩 😫 🤤 🥱 😴 😪 🌛 🌜 🌚 🌝 🎲 🧩 ♟ 🎯 🎳 🎭💕 💞 💓 💗 💖 ❤️‍🔥 💔 🤎 🤍 🖤 ❤️ 🧡 💛 💚 💙 💜 💘 💝 🐵 🦁 🐯 🐱 🐶 🐺 🐻 🐨 🐼 🐹 🐭 🐰 🦊 🦝 🐮 🐷 🐽 🐗 🦓 🦄 🐴 🐸 🐲 🦎 🐉 🦖 🦕 🐢 🐊 🐍 🐁 🐀 🐇 🐈 🐩 🐕 🦮 🐕‍🦺 🐅 🐆 🐎 🐖 🐄 🐂 🐃 🐏 🐑 🐐 🦌 🦙 🦥 🦘 🐘 🦏 🦛 🦒 🐒 🦍 🦧 🐪 🐫 🐿️ 🦨 🦡 🦔 🦦 🦇 🐓 🐔 🐣 🐤 🐥 🐦 🦉 🦅 🦜 🕊️ 🦢 🦩 🦚 🦃 🦆 🐧 🦈 🐬 🐋 🐳 🐟 🐠 🐡 🦐 🦞 🦀 🦑 🐙 🦪 🦂 🕷️ 🦋 🐞 🐝 🦟 🦗 🐜 🐌 🐚 🕸️ 🐛 🐾 🌞 🤢 🤮 🤧 🤒 🍓 🍒 🍎 🍉 🍑 🍊 🥭 🍍 🍌 🌶 🍇 🥝 🍐 🍏 🍈 🍋 🍄 🥕 🍠 🧅 🌽 🥦 🥒 🥬 🥑 🥯 🥖 🥐 🍞 🥜 🌰 🥔 🧄 🍆 🧇 🥞 🥚 🧀 🥓 🥩 🍗 🍖 🥙 🌯 🌮 🍕 🍟 🥨 🥪 🌭 🍔 🧆 🥘 🍝 🥫 🥣 🥗 🍲 🍛 🍜 🍢 🥟 🍱 🍚 🥡 🍤 🍣 🦞 🦪 🍘 🍡 🥠 🥮 🍧 🍨".split(
    " "
)

nama_kodam = [
    "MACAN MENCRET\nDia sebenarnya adalah orang yang tangguh, namun dia menjadi lemah karena suka mencret dan berak di celana.",
    "KETOMBE SEMUT\nDia adalah orang yang paling malas untuk mandi bahkan orang ini bisa mandi hanya satu kali dalam seminggu.",
    "DADAR GULUNG\nOrang ini suka makan tetapi hanya makan telur sehingga banyak bisul dan bekas bisul di pantat nya.",
    "CICAK ARAB\nKodam dia berasal dari arab dan orang ini adalah keturunan arab(arab gokil)",
    "BADARAWUHI\nOrangnya suka tantrum kalo lagi berantem. ", 
    "TUYUL BUSUNG LAPAR\nBadannya kurus tapi suka makan banyak. ",
    "GENDERUWO TIKTOK\nOrangnya gede tinggi lebat berbulu dan suka geal geol. ",
    "SETAN PAYUNG BOCOR\nOrang yang memiliki khodam ini akan mempunya skill ghibah kemanapun ia pergi. ", 
    "KUNTILANAK SELFIE\nOrang yang punya khodam ini bakalan sering ngerasa cantik dijam 3 pagi dan selfie terus sampe memori hpnya penuh. ", 
    "BATUBATA\nOrangnya bakalan susah dinasehatin karena sifatnya sekeras batu. ",
    "REMAHAN RENGGINANG\nOrang yang punya khodam ini sering ketawa mulu sekrispin remahan rengginang. ",
    "JIN PENUNGGU OS\nKhodam ini membuat pemiliknya betah terus terusan tidur di os seharian. ",
    "MANUSIA HARIMAU\nOrang yg punya khodam ini sering bikin pemiliknya mengeluarkan suara Rawr di OS. ",
    "KOSONG\nKhodam kamu kosong kaya otak kamu, silahkan isi di pom bensin terdekat. ",
    "RAWARONTEK\nOrang yang punya khodam ini kebal senjata tajam. ",
    "LC KARAOKE\nOrang yang punya khodam ini otomatis dapat memikat lawan jenis. ",
    "AWEWE GOMBEL\nOrang yamg punya khodam ini biasanya tante tante yang suka  nyulik laki laki di tele buat move ke WA.",
    "AYAM HALU\nOrang yang punya khodam ini sering Halu tiap malem ,berharap Biasnya bisa jadi suami. ", 
    "KAMBING CONGE\nOrang yang punya khodam ini adalah orang yang suka diem di OS padahal udah sering disapa. ",
    "KUNTILANAK STAR SYNDROME\nOrang yang punya khodam ini adalah orang yang dichat sekarang balesnya lebaran tahun depan. ",
    "BEBEK SUMBING\nOrangnya suka ngomong ekbew di OS. ",
    "TUYUL KULIAH ONLINE\nCiri ciri orang yang punya khodam ini adalah mempunyai kantung mata karena keseringan begadang ngerjain tugas. ",
    "VAMPIRE CABUL\nOrang yang punya khodam ini sering mengincar Chindo di Os. ",
    "SEMAR MESEM\nOrang yang punya khodam ini bakalan memikat orang dengan senyuman mautnya. ",
    "GAGANG TELEPON\nOrang yang punya khodam ini gabakalan bisa hidup tanpa sleepcall dipagi siang dan malam. ",
    "SUMANTO\nOrang yang punya khodam Sumanto adalah orang yang rela makan temennya demi suatu hal. ",
]

def get_arg(message: Message):
    if not message.text:
        return ""
    msg = message.text
    msg = msg.replace(" ", "", 1) if len(msg) > 1 and msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


async def isAdmin(filter, client, update):
    try:
        member = await client.get_chat_member(chat_id=update.chat.id, user_id=update.from_user.id)
    except FloodWait as wait_err:
        await sleep(wait_err.value)
    except UserNotParticipant:
        return False
    except:
        return False

    return member.status in [STATUS.OWNER, STATUS.ADMINISTRATOR]

FiltersAdmin = filters.create(isAdmin)

@app.on_message(filters.command("tagall") & FiltersAdmin & filters.group, group=37)
async def tagall(client, message: Message):
    await message.delete()
    chat_id = message.chat.id
    args = get_arg(message)
    if not args:
        args = "Halooo!"
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    m = client.get_chat_members(chat_id)
    async for usr in m:
        if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f"<a href='tg://user?id={usr.user.id}'>{random.choice(emoji)}</a> <a href='tg://user?id={usr.user.id}'><b>{usr.user.first_name}</b></a>\n"
        if usrnum == 5:
            txt = f"<b>{args}</b>\n\n{usrtxt}"
            try:
                await client.send_message(chat_id, txt)
            except FloodWait as e:
                await sleep(e.value)
                await client.send_message(chat_id, txt)

            await sleep(2)
            usrnum = 0
            usrtxt = ""
    try:
        await client.send_message(chat_id, "<b>ᴘʀᴏꜱᴇꜱ ᴛᴀɢ ᴀʟʟ ᴛᴇʟᴀʜ ꜱᴇʟᴇꜱᴀɪ.</b>")
        spam_chats.remove(chat_id)
    except:
        pass

@app.on_message(filters.command("stoptag") & FiltersAdmin & filters.group, group=36)
async def untag(client, message: Message):
    if not message.chat.id in spam_chats:
        return await message.reply("<b>ꜱᴇᴘᴇʀᴛɪɴʏᴀ ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴛᴀɢ ᴀʟʟ ʏᴀɴɢ ꜱᴇᴅᴀɴɢ ʙᴇʀʟᴀɴɢꜱᴜɴɢ.</b>")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("<b>ᴘʀᴏꜱᴇꜱ ᴛᴀɢ ᴀʟʟ ᴅɪ ʜᴇɴᴛɪᴋᴀɴ.</b>")
        
@app.on_message(filters.command("cekkodam") & FiltersAdmin & filters.group, group=35)
async def cek_kodam_command(client, message):
    OWNER = [7070276015, 6293684359, 7460160870]
    replied_user = message.reply_to_message.from_user.first_name if message.reply_to_message else None
    replied_user_id = message.reply_to_message.from_user.id
    if replied_user_id in TEAM_IDOL:
        response = random.choice(nama_kodam)
        reply_text = f"<blockquote><b>Khodam {replied_user}, adalah: ALBERT EINSTEIN</b></blockquote>\n<blockquote><b>Dia adalah orang yang sangat pintar dan sangat sangat tidak terkalahkan.</b></blockquote>"
        await message.reply_text(reply_text)
    elif replied_user:
        response = random.choice(nama_kodam)
        reply_text = f"<blockquote>Kodam {replied_user} adalah: {response}</blockquote>"
        message.reply_text(reply_text)
    else:
        await message.reply_text("Kamu harus mereply sesorang yang ingin saya cek kodam nya.")