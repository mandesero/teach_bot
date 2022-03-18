from aiogram.types import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton
from callback_data.callback_data import menu_callback

# --- Main menu ---
btnMenu = KeyboardButton("MENU")
menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(btnMenu)

# --- Menu ---
main_menu_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[

        [
            InlineKeyboardButton(
                text="Отправить на проверку",
                callback_data=menu_callback.new(ans="send")
            )
        ],

        [
            InlineKeyboardButton(
                text="Моё расписание",
                callback_data="send:timetable"
            )
        ],
        [
            InlineKeyboardButton(
                text="Мои оценки",
                callback_data="send:marks"
            )
        ]

    ]
)
