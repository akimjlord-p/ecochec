from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import db_func
from ..kbs.main_kb import get_main_kb
from ..kbs.cancel import cancel_kb
from db_func import is_admin, add_device, get_user_city

router = Router()


class AddDevice(StatesGroup):
    device = State()


@router.message(F.text.lower() == 'добавить устройство')
async def add_device_msg(message: Message, state: FSMContext):
    if is_admin(str(message.from_user.id)):
        await message.answer('Введите <b>Верно</b> для добавления устройства'
                             ' (устройство будет зарегестрировано в текущем выбранном городе)',
                             reply_markup=cancel_kb)
        await state.set_state(AddDevice.device)


@router.message(AddDevice.device)
async def get_device(message: Message, state: FSMContext):
    if message.text.lower() == 'верно':

        device_id = add_device(get_user_city(str(message.from_user.id)))
        await message.answer(text=f'Устройство с id <b>{device_id}</b> зарегестрировано',
                             reply_markup=get_main_kb(message.from_user.id))
        await state.clear()
    else:
        await message.answer(text='Действие отменено',
                             reply_markup=get_main_kb(message.from_user.id))
        await state.clear()


@router.message(F.text.lower() == 'все устройства города')
async def get_all_devices(message: Message):
    devices = db_func.get_devices(db_func.get_user_city(str(message.from_user.id)))
    text = ''
    for device in devices:
        text += str(device) + '\n'
    await message.answer(text=text,
                         reply_markup=get_main_kb(message.from_user.id))
