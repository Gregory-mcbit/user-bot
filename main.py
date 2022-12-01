from pyrogram import Client
import asyncio

try:
    api_id = input("Введите api_id -> ")
    api_hash = input("Введите api_hash -> ")

    app = Client(
        "account",
        api_id=api_id,
        api_hash=api_hash
    )

    logined = False

    print("Происходит запуск программы. Пожалуйста, подождите...")
    chat_list = []  # [chat_id, chat_title, chat_num]

    app.start()

    async def get_dialogs():
        global chat_list
        index = 1

        async for dialog in app.get_dialogs():

            if str(dialog.chat.type) != "ChatType.PRIVATE" and str(dialog.chat.type) != "ChatType.BOT":
                chat_name, chat_id = dialog.chat.title or dialog.chat.first_name, dialog.chat.id

                if chat_name is not None:
                    chat_list.append([chat_id, chat_name.lower(), index])
                    index += 1


    if not logined:

        tracked_chats_ids = set()
        tracked_chats_titles = set()

        print("Сейчас будет произведено чтение групп на вашем аккаунте")

        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_dialogs())

        print("Готово")

        print('Список чатов:')
        c = "\n".join([str(x[2]) + ") " + x[1] for x in chat_list])
        print(c)

        numbers = input("\nДля выбора отслеживаемых чатов введите их номера через запятую. Пример: 1, 2, 3, 4, 5, "
                        "... (Обязательно пробел после запятой) ---> ")
        numbers = numbers.split(", ")

        try:
            for digit in numbers:
                tracked_chats_ids.add(chat_list[int(digit) - 1][0])
                tracked_chats_titles.add(chat_list[int(digit) - 1][1])

        except Exception:
            print("Номера групп были неправильно введены. Перезапустите программу и повторите попытку\n")
            input('Press ENTER to exit')

        print("\nСписок отслеживаемых чатов:")
        print(" | ".join(list(tracked_chats_titles)))

        phrase4user = input("\nВведите фразу, которая будет отправлена пользователю -> ")
        print("Принято!\n")

        key_phrases = []
        print('Ниже введите ключевые слова/фразы для поиска. Для окончания ввода напишите "stop/стоп"')

        while True:
            phrase = input("Введите фразу --> ")
            if phrase == "stop" or phrase == "стоп":
                break

            key_phrases.append(phrase.lower())

        print("\nВвод фраз окончен. Программа работает и сканирует чаты...")
        logined = True

    app.stop()


    @app.on_message()
    async def check_msg(client, message):
        try:
            if any([word for word in key_phrases if word in message.text.lower()]) & (message.chat.id in tracked_chats_ids):
                await app.send_message(message.from_user.id, phrase4user)
                print(f"Сообщение отправлено пользователю {message.from_user.first_name} {message.from_user.last_name} из чата {message.chat.title}")
            
            except:
                pass


    app.run()

except Exception as e:
    input(f"Ошибка\n{e}\n НАЖМИТЕ ENTER ДЛЯ ВЫХОДА  ")
