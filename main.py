#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import asyncio
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from telebot.async_telebot import AsyncTeleBot

import datetime
import time


# Определяем область доступа
async def setup_google_sheets():
   scope = ["https://www.googleapis.com/auth/drive.readonly"]

# Загружаем учетные данные из файла JSON
   creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Projects\products on warehouse\credentials.json', scope)

# Авторизуемся
   client = gspread.authorize(creds)
   return client.open('Birthday of bot').sheet1


# Функция для отправки сообщений
async def send_messages_within_time_range(sheet, chat_id, bot):
    now = datetime.datetime.now()
    lower_bound = now - datetime.timedelta(minutes=1)
    upper_bound = now + datetime.timedelta(minutes=1)

    # Получаем все данные из таблицы
    messages = sheet.get_all_records()

    for message in messages:
        message_time = datetime.datetime.strptime(message['Дата'], '%d.%m.%Y %H:%M:%S')

        if lower_bound <= message_time <= upper_bound:
            await bot.send_message(chat_id=chat_id, text=message['Текст сообщения'])


async def main():
    # Инициализация бота
    bot = AsyncTeleBot(os.environ['TELEGRAM_TOKEN_WAREHOUSE'])
    chat_id = '-4974550659'

    # Настройка Google Sheets
    sheet = await setup_google_sheets()

    # Запуск функции в цикле
    while True:
        await send_messages_within_time_range(sheet, chat_id, bot)
        await asyncio.sleep(10)  # Проверяем каждые 10 секунд


if __name__ == "__main__":
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())