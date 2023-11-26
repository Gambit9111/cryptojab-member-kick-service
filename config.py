import os
from dotenv import load_dotenv
load_dotenv()

DB_URL = os.getenv("DB_URL")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_ADMIN_ID = os.getenv("TELEGRAM_ADMIN_ID")
TELEGRAM_PREMIUM_CHANNEL_ID = os.getenv("TELEGRAM_PREMIUM_CHANNEL_ID")
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")

if DB_URL is None:
    raise Exception("DB_URL not set in .env file")
elif TELEGRAM_BOT_TOKEN is None:
    raise Exception("TELEGRAM_BOT_TOKEN not set in .env file")
elif TELEGRAM_ADMIN_ID is None:
    raise Exception("TELEGRAM_ADMIN_ID not set in .env file")
elif TELEGRAM_PREMIUM_CHANNEL_ID is None:
    raise Exception("TELEGRAM_PREMIUM_CHANNEL_ID not set in .env file")
elif STRIPE_API_KEY is None:
    raise Exception("STRIPE_API_KEY not set in .env file")
else :
    print("All environment variables set")