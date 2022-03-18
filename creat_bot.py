from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import asyncio

from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

loop = asyncio.get_event_loop()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, loop=loop, storage=(storage := MemoryStorage()))
