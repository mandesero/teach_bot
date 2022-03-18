from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from creat_bot import bot
from config import ADMIN_ID, TOKEN
import urllib


class FSMAdmin(StatesGroup):
    lesson = State()
    work = State()
    file = State()


async def new_lesson(message: types.Message):
    if message.from_user.id in ADMIN_ID:
        await FSMAdmin.lesson.set()
        await message.answer("Номер урока")
    else:
        await message.reply(
            "Traceback (most recent call last):\n"
            "File 'main.py', line 1, in <module>\n\n"
            "PermissionError: you don't have permission"
        )


async def get_new_lesson(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["lesson"] = message.text
    await message.answer("Номер задания")
    await FSMAdmin.next()


async def get_new_work(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["work"] = message.text
    await FSMAdmin.next()
    await message.answer("Прикрепи файл с заданием")


async def get_new_file(message: types.Message, state: FSMContext):
    document_id = message.document.file_id
    file_info = await bot.get_file(file_id=document_id)
    fi = file_info.file_path
    ff = message.document.file_name.split('.')[-1]
    async with state.proxy() as data:
        name = f"{data['lesson']}_{data['work']}_W.{ff}"
    urllib.request.urlretrieve(
        f'https://api.telegram.org/file/bot{TOKEN}/{fi}',
        f'./works/{name}'
    )
    await bot.send_message(message.from_user.id, 'Файл успешно сохранён')
    await state.finish()


async def new_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Ok")


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(new_cancel, state="*", commands="отмена")
    dp.register_message_handler(new_cancel, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(new_lesson, commands=['new'], state=None)
    dp.register_message_handler(get_new_lesson, state=FSMAdmin.lesson)
    dp.register_message_handler(get_new_work, state=FSMAdmin.work)
    dp.register_message_handler(get_new_file, content_types=['document'], state=FSMAdmin.file)
