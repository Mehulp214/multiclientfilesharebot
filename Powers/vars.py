from os import getenv

OWNER_ID = int(getenv("OWNER_ID","5434500969"))
SUDO = [int(i) for i in getenv("SUDO","5642570692").strip().split()]
DB_CHANNEL = int(getenv("DB_CHANNEL","-1001902384275"))
BOT_TOKEN = getenv("BOT_TOKEN","6683231223:AAEtwgg-e0ENv72k9DCrqXPGl6blvve6cvE")
API_ID = int(getenv("API_ID","13216322"))
API_HASH = getenv("API_HASH","15e5e632a8a0e52251ac8c3ccbe462c7")
DB_URI = getenv("DB_URI","mongodb+srv://Mehul1234:Mehul1234@cluster0.ieubhon.mongodb.net/")
DB_NAME = getenv("DB_NAME", "FILE_SHARE")
FSUB_CHANNEL = [int(i) for i in getenv("FSUB_CHANNEL", "-1001755279044").strip().split()]
REQ_FSUB = [int(i) for i in getenv("REQ_FSUB", "").strip().split()]
