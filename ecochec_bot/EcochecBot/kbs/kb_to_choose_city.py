from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from typing import Optional


class CityCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[str] = None


def c_get_kb(n, texts, ids, page):
    builder = InlineKeyboardBuilder()
    if n < 20 or (page + 1) * 20 >= n:
        for i in range(page * 20, n):
            builder.button(text=str(texts[i]),
                           callback_data=CityCallbackFactory(action="city", value=str(ids[i])))
    else:
        for i in range(page * 20, (page + 1) * 20):
            builder.button(text=str(texts[i]),
                           callback_data=CityCallbackFactory(action="city", value=str(ids[i])))
    if n < 20:
        pass
    elif (page + 1) * 20 >= n:
        builder.button(text='<--', callback_data=CityCallbackFactory(action='switch', value='previous_c'))
    elif page == 0:
        builder.button(text='-->', callback_data=CityCallbackFactory(action='switch', value='next_c'))
    else:
        builder.button(text='<--', callback_data=CityCallbackFactory(action='switch', value='previous_c'))
        builder.button(text='-->', callback_data=CityCallbackFactory(action='switch', value='next_c'))

    builder.adjust(2)
    return builder.as_markup()


