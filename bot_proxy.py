import os
import json
import telebot
import requests
from telebot.types import Update

token = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(token, parse_mode=None)


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
# 	bot.reply_to(message, message.text)
#
# bot.infinity_polling()
#
# updates = bot.get_updates()
# print(updates[0].message)


base_url = f'https://api.telegram.org/bot{token}/getUpdates'

# print(requests.get(url).json())

offset = 75364642
while True:
    url = base_url + f'?offset={offset}&limit=1'
    response = requests.get(url).json()
    if response['result']:
        offset = response['result'][0]['update_id'] + 1
        print(response['result'][0])
        requests.post(
            'http://127.0.0.1:8000/',
            json.dumps(response['result'][0]),
            headers={'Content-Type': 'application/json',}
        )