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
   creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Projects\products on warehouse\my-project-copy-end-file-f6ec472d11ef.json', scope)

# Авторизуемся
   client = gspread.authorize(creds)
   spreadsheet = client.open('Копия Выкуп со склада_мой вариант')
   worksheet = spreadsheet.get_worksheet(4)

   return worksheet


async def filter_column_data(worksheet):
    # Получаем все данные из таблицы
    all_data = worksheet.get_all_values()

    # Применяем условия к строкам
    filtered_rows = []
    for row in all_data[1:]:  # Пропускаем заголовок
#        if len(row) < 8:  # Проверяем, чтобы избежать IndexError
#            continue

        # Условия:
        if row[6] == 'TRUE':
            filtered_rows.append(row)

    return filtered_rows

#async def filter_column_data(worksheet):

    # Получаем все данные из нужного столбца (например, G, который имеет индекс 7)
#   column_data = worksheet.col_values(6)  # 7 - это индекс столбца G

    # Применяем условия к значениям в столбце
#   filtered_values = [value for value in column_data if value.lower() == 'TRUE']
#   return filtered_values
#    return filtered_values




# Функция для отправки сообщений
async def send_messages_within_time_range(sheet, chat_id, bot):
    now = datetime.datetime.now()
    lower_bound = now - datetime.timedelta(minutes=1)
    upper_bound = now + datetime.timedelta(minutes=1)

    filtered_data = await filter_column_data(sheet)

    for row in filtered_data:
        message_time = datetime.datetime.strptime(row[4], '%d.%m.%Y %H:%M:%S')

        if lower_bound <= message_time <= upper_bound:
            await bot.send_message(chat_id=chat_id, text=row[5])




    # Получаем все данные из таблицы

#    messages = sheet.get_all_values()

#    for message in messages[1:]:


#        message_time = datetime.datetime.strptime(message[4], '%d.%m.%Y %H:%M:%S')

#        if lower_bound <= message_time <= upper_bound:
#            await bot.send_message(chat_id=chat_id, text=message[5])


async def main():
    # Инициализация бота
    bot = AsyncTeleBot(os.environ['TELEGRAM_TOKEN_WAREHOUSE'])
    chat_id = '-4974550659'

    # Настройка Google Sheets
    sheet = await setup_google_sheets()

    # Запуск функции в цикле
    while True:
        await send_messages_within_time_range(sheet, chat_id, bot)
        await asyncio.sleep(30)  # Проверяем каждые 10 секунд


if __name__ == "__main__":
    asyncio.run(main())