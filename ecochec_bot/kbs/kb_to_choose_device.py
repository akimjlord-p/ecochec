from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from typing import Optional


class DeviceCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[str] = None


def d_get_kb(n, texts, ids, page):
    builder = InlineKeyboardBuilder()
    if n < 20 or (page + 1) * 20 >= n:
        for i in range(page * 20, n):
            builder.button(text=str(texts[i]),
                           callback_data=DeviceCallbackFactory(action="device", value=str(ids[i])))
    else:
        for i in range(page * 20, (page + 1) * 20):
            builder.button(text=str(texts[i]),
                           callback_data=DeviceCallbackFactory(action="device", value=str(ids[i])))
    if n < 20:
        pass
    elif (page + 1) * 20 >= n:
        builder.button(text='<--', callback_data=DeviceCallbackFactory(action='switch', value='previous_d'))
    elif page == 0:
        builder.button(text='-->', callback_data=DeviceCallbackFactory(action='switch', value='next_d'))
    else:
        builder.button(text='<--', callback_data=DeviceCallbackFactory(action='switch', value='previous_d'))
        builder.button(text='-->', callback_data=DeviceCallbackFactory(action='switch', value='next_d'))

    builder.adjust(2)
    return builder.as_markup()