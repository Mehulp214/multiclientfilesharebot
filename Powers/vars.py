from os import getenv

OWNER_ID = int(getenv("OWNER_ID"))
SUDO = [int(i) for i in getenv("SUDO").strip().split()]
DB_CHANNEL = int(getenv("DB_CHANNEL"))
BOT_TOKEN = getenv("BOT_TOKEN")
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
DB_URI = getenv("DB_URI")
DB_NAME = getenv("DB_NAME", "FILE_SHARE")
