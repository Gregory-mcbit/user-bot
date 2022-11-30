from pyrogram import enums, Client, filters, errors
import asyncio

api_id = 28067374
api_hash = "52a54ec6fdaa4d8e608c137c9faa4316"

app = Client(
    "account",
    api_id=api_id,
    api_hash=api_hash
)

# @app.on_message(filters.me)
# def echo(client, message):
#     message.reply_text(message.text)
#
#
# app.run()

chat_list = []  # [chat_id, chat_title, chat_num]
tracked_chats_ids = []
tracked_chats_titles = []


async def get_chats():
    global chat_list
    index = 1

    try:
        async with app:
            async for dialog in app.get_dialogs():
                chat_name, chat_id = dialog.chat.title, dialog.chat.id
                if chat_name is not None:
                    chat_list.append([chat_id, chat_name.lower(), index])
                    index += 1

    except Exception:
        pass


def main():
    print("Сейчас будет произведено чтение групп на вашем аккаунте")
    asyncio.run(get_chats())
    print("Готово")

    print('Список чатов:')
    c = "\n".join([str(x[2]) + ") " + x[1] for x in chat_list])
    print(c)

    numbers = input("\nДля выбора отслеживаемых чатов введите их номера через запятую. Пример: 1, 2, 3, 4, 5, "
                    "... (Обязательно пробел после запятой) ---> ")
    numbers = numbers.split(", ")

    for digit in numbers:
        tracked_chats_ids.append(chat_list[int(digit) - 1][0])
        tracked_chats_titles.append(chat_list[int(digit) - 1][1])

    print("\nСписок отслеживаемых чатов:")
    print("; ".join(tracked_chats_titles))

    phrase = input("\nВведите фразу, которая будет отправлена пользователю -> ")


if __name__ == "__main__":
    main()
