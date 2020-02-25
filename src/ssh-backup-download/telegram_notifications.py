import os
import requests


def send_notification(message='', notification_type=''):
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    telegram_api = os.getenv('TELEGRAM_API')
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    message = f'{notification_type}: {message}' if notification_type else message
    url = f'{telegram_api}/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}'
    requests.post(url)
