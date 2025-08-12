import os
from dotenv import load_dotenv
load_dotenv()

CHAT_ID = os.getenv("MY_CHAT")
TELEGRAM_BOT = os.getenv("TELEGRAM_BOT")

SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_DB = os.getenv("SUPABASE_DB")

TOKEN_FB1 = os.getenv("TOKEN_FB1")
TOKEN_FB2 = os.getenv("TOKEN_FB2")