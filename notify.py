import requests
import os
from dotenv import load_dotenv
load_dotenv()

CHAT_ID = os.getenv("MY_CHAT")
TELEGRAM_BOT = os.getenv("TELEGRAM_BOT")
# GROUP_CHAT_ID = os.getenv('GROUP')

def Me(msg):
    URL = f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage"
    parametros = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    respuesta = requests.post(URL, data=parametros)

""" 
        AUN NO

def Channel(IMAGE_URL,CAPTION = ''):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {
        "chat_id": "@WaiFUNotSF",  # Usa '@nombre_del_canal' o
        "photo": IMAGE_URL,
        "caption": CAPTION
    }
    response = requests.post(url, data=payload)
    return response
    
"""