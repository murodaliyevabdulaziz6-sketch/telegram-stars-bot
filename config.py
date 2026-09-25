import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "8985537152:AAGwr18aMa9oj1s5J6zEO0hE4ytLXurO6_I")

# Super Admin ID (Eng katta ega)
SUPER_ADMIN_ID = 6781163470

# Admin IDs list
admin_ids_raw = os.getenv("ADMIN_IDS", "6781163470")
ADMIN_IDS = [int(x.strip()) for x in admin_ids_raw.split(",") if x.strip().isdigit()]
if SUPER_ADMIN_ID not in ADMIN_IDS:
    ADMIN_IDS.append(SUPER_ADMIN_ID)

# Mandatory Subscription Channels (e.g. @mychannel or -100123456789)
channels_raw = os.getenv("REQUIRED_CHANNELS", "")
REQUIRED_CHANNELS = [x.strip() for x in channels_raw.split(",") if x.strip()]

DB_PATH = BASE_DIR / os.getenv("DB_PATH", "data/bot.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
