import requests
from django.conf import settings


def send_msg_tg(message, chat_id):
    response = requests.post(
        url=f'https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage',
        params={
            'chat_id': chat_id,
            'text': message
        })
    return response
