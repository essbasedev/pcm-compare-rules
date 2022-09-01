import requests
import os
from dotenv import load_dotenv

load_dotenv()
telegram_token = os.getenv('telegram_token')
telegram_channel = os.getenv('telegram_channel')


def send_message(message):
    parameters = {
    "chat_id": telegram_channel,
    "text": {message},
    "parse_mode": "Markdown"
    }
    response = requests.get(url=f"https://api.telegram.org/bot{telegram_token}/sendMessage?",
        params=parameters)
    response.raise_for_status()
