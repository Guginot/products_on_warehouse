import asyncio
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from telebot.async_telebot import AsyncTeleBot
import pytz
import datetime
from datetime import datetime, timedelta

# Определяем область доступа
async def setup_google_sheets():
   scope = ["https://www.googleapis.com/auth/drive.readonly"]

# Загружаем учетные данные из файла JSON
   creds = ServiceAccountCredentials.from_json_keyfile_name(r'/home/products_on_warehouse/projects/products_on_warehouse/seventh-ripsaw-474517-e4-b36b477edbd5.json', scope)
#   creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Projects\products on warehouse/seventh-ripsaw-474517-e4-b36b477edbd5.json', scope)
# Авторизуемся
   client = gspread.authorize(creds)
   spreadsheet = client.open('Выкуп со склада')
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





# Функция для отправки сообщений
async def send_messages_within_time_range(sheet, chat_id, bot):
#    now = datetime.datetime.now()
#    lower_bound = now - datetime.timedelta(seconds=30)
#    upper_bound = now + datetime.timedelta(seconds=30)

# Получаем текущее время в UTC
    utc_now = datetime.now(pytz.utc)

# Конвертируем в московское время
    msk_tz = pytz.timezone('Europe/Moscow')
    now_msk = utc_now.astimezone(msk_tz)

# Убираем информацию о часовом поясе для сравнения
    now_msk_naive = now_msk.replace(tzinfo=None)


    lower_bound = now_msk_naive - timedelta(seconds=30)
    upper_bound = now_msk_naive + timedelta(seconds=30)

#    lower_bound = now.replace(second=0, microsecond=0)
#    upper_bound = lower_bound + datetime.timedelta(minutes=1)

    filtered_data = await filter_column_data(sheet)

    for row in filtered_data:
#        message_time = datetime.datetime.strptime(row[4], '%d.%m.%Y %H:%M:%S')
        message_time = datetime.strptime(row[4], '%d.%m.%Y %H:%M:%S')
        if lower_bound <= message_time <= upper_bound:
            await bot.send_message(chat_id=chat_id, text=row[5])







async def main():
    # Инициализация бота
    bot = AsyncTeleBot(os.environ['TELEGRAM_TOKEN_WAREHOUSE'])
    chat_id = '-1002582008990'

    # Настройка Google Sheets
    sheet = await setup_google_sheets()

    # Запуск функции в цикле
    while True:
        await send_messages_within_time_range(sheet, chat_id, bot)
        await asyncio.sleep(60)  # Проверяем каждые 10 секунд
#        now = datetime.datetime.now()
#        sleep_time = 60 - now.second
#        await asyncio.sleep(sleep_time)


if __name__ == "__main__":
    asyncio.run(main())