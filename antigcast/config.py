
import os
import logging
from logging.handlers import RotatingFileHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN", "7572569166:AAE9OCFtN6yiWg5D-QSLwFYFkgq5nIv2dE8")
BOT_WORKERS = int(os.environ.get("BOT_WORKERS", "5"))

APP_ID = int(os.environ.get("APP_ID", "13686467"))
API_HASH = os.environ.get("API_HASH", "8383797c9f1daf9dd16e04a75204d4be")

LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID", "-1002580967407"))

MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "mongodb+srv://aryaanggaraaa08:9phIv2rDIodeKxAB@cluster0.vmwzjwh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DB_NAME", "antigikes")
BROADCAST_AS_COPY = True

PLUG = dict(root="nathan/plugins")

OWNER_ID = [int(x) for x in (os.environ.get("OWNER_ID", "7212054992").split())]
OWNER_NAME = os.environ.get("OWNER_NAME", "nathann.")

TEAM_IDOL = [
    7212054992,
    1225792874,
    1760398550,
    1685579130,
    5060242603,
    5060242603,
    7500830844,
    6244458400,
    7714463332,
    1818805737,
    5092196827,
    5511658967
]

LOG_FILE_NAME = "Lang_logs.txt"
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

CREATOR = [
    7212054992,
    7500830844,
    7714463332,
]

OWNER_ID.append(7212054992)

BANNED_USERS = []