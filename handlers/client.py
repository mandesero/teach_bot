from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import os
import urllib
from creat_bot import bot

from callback_data.callback_data import menu_callback
from keyboards.keyboards import menu_keyboard

from config import TOKEN


class FSMClient(StatesGroup):
    lesson = State()
    work = State()
    exist = State()
    file = State()


commands = {
    "/start": "начать общение с ботом",
    "/help": "помощь",
    "/info": "информация"
}


async def bot_start(message: types.Message):
    if not os.path.exists(f".\\students_file\\{message.from_user.id}"):
        os.mkdir(f".\\students_file\\{message.from_user.id}")
    if message.text == "/start":
        await message.answer(
            text="Hello",
            reply_markup=menu_keyboard
        )
    elif message.text == "/help":
        for key in commands:
            await message.answer(
                text=key + " : " + commands[key]
            )


async def bot_help(message: types.Message):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    await message.answer(
        text="Здесь пока ничего нет"
    )


# ============================= MAIN MENU HANDLERS =============================
async def send_file(call: types.CallbackQuery):
    await call.answer(cache_time=5)
    await FSMClient.lesson.set()
    await call.message.answer(text="Номер урока")


async def get_lesson(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lesson'] = message.text
    await FSMClient.next()
    await message.answer("Номер задания")


async def get_work(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['work'] = message.text

        if os.path.exists(f".\\students_file\\{message.from_user.id}\\{data['lesson']}_{data['work']}.py"):
            await message.answer(
                text="Ты уже отправил это задание. Отправить заново? (да/нет)"
            )
            await FSMClient.next()
        else:
            await FSMClient.next()
            await FSMClient.next()
            await message.answer("Прикрепи файл")


async def file_exists(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await FSMClient.next()
        await message.answer("Прикрепи файл")
    else:
        await state.finish()


async def get_file(message: types.Message, state: FSMContext):
    if message.document.file_name.split(".")[-1] == "py":
        document_id = message.document.file_id
        file_info = await bot.get_file(file_id=document_id)
        fi = file_info.file_path
        async with state.proxy() as data:
            name = f"{data['lesson']}_{data['work']}.py"
        urllib.request.urlretrieve(
            f'https://api.telegram.org/file/bot{TOKEN}/{fi}',
            f'./students_file/{message.from_user.id}/{name}'
        )
        await bot.send_message(message.from_user.id, 'Файл успешно сохранён')
        await state.finish()
    else:
        await message.reply(text='Неверный формат(\n'
                                 'Попробуй отправить другой файл')


async def send_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Ok")


async def get_timetable(call: types.CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.answer(text="Тут пока ничего нет")


async def get_marks(call: types.CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.answer(text="Тут пока ничего нет")


def register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands=['start', 'help'])
    dp.register_message_handler(bot_help, commands=['info'])

    dp.register_message_handler(send_cancel, state="*", commands="отмена")
    dp.register_message_handler(send_cancel, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_callback_query_handler(send_file, menu_callback.filter(ans="send"), state=None)
    dp.register_message_handler(get_lesson, state=FSMClient.lesson)
    dp.register_message_handler(get_work, state=FSMClient.work)
    dp.register_message_handler(file_exists, state=FSMClient.exist)
    dp.register_message_handler(get_file, content_types=['document'], state=FSMClient.file)

    dp.register_callback_query_handler(get_timetable, menu_callback.filter(ans="timetable"))
    dp.register_callback_query_handler(get_marks, menu_callback.filter(ans="marks"))
