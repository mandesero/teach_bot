from aiogram import types, Dispatcher

from creat_bot import bot
import string
import json

from keyboards.keyboards import main_menu_keyboard


async def ordinary_message(message: types.Message):
    if message.text == "MENU":
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
        await message.answer(
            text="МЕНЮ БОТА:",
            reply_markup=main_menu_keyboard
        )
    elif {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
            .intersection(set(json.load(open('censure.json')))):
        await message.reply("Маты запрещены!")
        await message.delete()


def register_other_handlers(dp: Dispatcher):
    dp.register_message_handler(ordinary_message)
