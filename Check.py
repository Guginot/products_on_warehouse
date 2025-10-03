async def send_messages_within_time_range(sheet, chat_id, bot):
    now = datetime.datetime.now()
    lower_bound = now - datetime.timedelta(minutes=1)
    upper_bound = now + datetime.timedelta(minutes=1)

    # Получаем все данные из таблицы
    messages = sheet.get_all_values()

    # Пропускаем заголовок и обрабатываем только данные
    for message in messages[1:]:  # Начинаем с первого индекса, чтобы пропустить заголовок
        try:
            # Предполагаем, что 'Время отправки' находится в шестом столбце (индекс 5)
            message_time_str = message[5]  # Убедитесь, что это правильный индекс
            message_time = datetime.datetime.strptime(message_time_str, '%d.%m.%Y %H:%M:%S')

            if lower_bound <= message_time <= upper_bound:
                # Предполагаем, что 'Текст сообщения' находится во втором столбце (индекс 1)
                await bot.send_message(chat_id=chat_id, text=message[1])

        except ValueError as e:
            print(f"Ошибка преобразования даты для строки {message}: {e}")
        except IndexError as e:
            print(f"Ошибка доступа к элементу в строке {message}: {e}")