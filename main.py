from aiogram.utils import executor
from creat_bot import bot, dp
from config import ADMIN_ID


from handlers import client, admin, other
client.register_client_handlers(dp)
admin.register_admin_handlers(dp)
other.register_other_handlers(dp)


async def start_admin(_):
    await bot.send_message(chat_id=ADMIN_ID[0], text="Starting bot...")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=start_admin)
