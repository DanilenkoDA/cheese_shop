import requests
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_telegram_message(order):
    text = f"🧀 Новый заказ #{order.id} от {order.name}!\n📞 Тел: {order.phone}\n📍 Адрес: {order.address}\n"
    for item in order.items.all():
        text += f"• {item.product.name} x {item.quantity}\n"
    text += f"\n👤 Пользователь: {order.user.username}"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': text})