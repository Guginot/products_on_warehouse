#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import asyncio
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from telebot.async_telebot import AsyncTeleBot


# Определяем область доступа
scope = ["https://www.googleapis.com/auth/drive.readonly"]

# Загружаем учетные данные из файла JSON
creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Projects\products on warehouse\credentials.json', scope)

# Авторизуемся
client = gspread.authorize(creds)

# Открываем таблицу по названию
sheet = client.open("Birthday of bot").sheet1  # sheet1 — это первый лист

# Читаем данные из таблицы
data = sheet.get_all_records()
print(data)


bot = AsyncTeleBot(os.environ['TELEGRAM_TOKEN_WAREHOUSE'])


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = 'Hi, I am EchoBot.\nJust write me something and I will repeat it!'
    await bot.reply_to(message, text)



# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)






if __name__ == '__main__':
   asyncio.run(bot.polling())