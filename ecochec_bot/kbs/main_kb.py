from aiogram import types
from db_func import is_admin, check_user


def get_main_kb(id_tg):
    if is_admin(id_tg):
        print(id_tg)
        kb = [
            [types.KeyboardButton(text='Сменить город')],
            [types.KeyboardButton(text='Добавить устройство')],
            [types.KeyboardButton(text='Добавить город')],
            [types.KeyboardButton(text='ecochec')],
            [types.KeyboardButton(text='Информация')]
        ]
        kb = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder='Что будем делать?'
        )
        return kb

    if not check_user(id_tg):
        kb = [
            [types.KeyboardButton(text='Выбрать город')],
            [types.KeyboardButton(text='Информация')]
        ]
        kb = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder='Что будем делать?'
        )
        return kb

    else:
        kb = [
            [types.KeyboardButton(text='Сменить город')],
            [types.KeyboardButton(text='ecochec')],
            [types.KeyboardButton(text='Информация')]
        ]
        kb = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder='Что будем делать?'
        )
        return kb

        
