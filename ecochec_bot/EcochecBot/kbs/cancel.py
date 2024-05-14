from aiogram import types


kb = [
    [types.KeyboardButton(text="отмена")],
]

cancel_kb = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
    input_field_placeholder='Что будем делать?'
)