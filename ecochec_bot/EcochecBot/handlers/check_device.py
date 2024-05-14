from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from .. import texts
from ..kbs.kb_to_choose_device import d_get_kb, DeviceCallbackFactory
from ..kbs.main_kb import get_main_kb
from ..kbs.cancel import cancel_kb
from db_func import get_devices, get_data_from_device, get_user_city, check_user, get_addr, get_city_by_id
from aiogram import html
router = Router()


class CheckDevice(StatesGroup):
    device = State()
    devices_addresses = State()
    devices_ids = State()
    page = State()


@router.message(F.text.lower() == 'ecochec')
async def choose_device_msg(message: Message, state: FSMContext):
    if check_user(str(message.from_user.id)):
        devices_info = get_devices(get_user_city(str(message.from_user.id)))
        if not devices_info:
            await message.answer(text='В вашем городе не установлена система Ecochec')
            return
        kb = d_get_kb(len(devices_info), [device['address'] for device in devices_info],
                      [device['device_id'] for device in devices_info], 0)
        await state.set_state(CheckDevice.device)
        await state.update_data(devices_addresses=[device['address'] for device in devices_info],
                                devices_ids=[device['device_id'] for device in devices_info], page=0)
        await message.answer(text=texts.list_of_devices(get_city_by_id(get_user_city(str(message.from_user.id)))),
                             reply_markup=cancel_kb)
        await message.answer(text=html.quote(texts.choose_device_switch()), reply_markup=kb)


@router.callback_query(CheckDevice.device, DeviceCallbackFactory.filter(F.action == "device"))
async def get_device(callback: CallbackQuery, state: FSMContext, callback_data: DeviceCallbackFactory):
    device_id = callback_data.value
    device = get_data_from_device(device_id)
    address = get_addr([device['latitude'], device['longitude']])
    await callback.message.answer(text=texts.device_data(t=device['t'],
                                                         g=device['g'],
                                                         s=device['s'],
                                                         time=device['time'],
                                                         city=get_city_by_id(get_user_city(str(callback.from_user.id))),
                                                         address=address))
    if address == 'Ошибка':
        await callback.message.answer(text=texts.error_address(), reply_markup=get_main_kb(callback.from_user.id))
    else:
        await callback.message.answer_location(latitude=device['latitude'],
                                               longitude=device['longitude'],
                                               reply_markup=get_main_kb(callback.from_user.id))
    await state.clear()


@router.callback_query(CheckDevice.device, DeviceCallbackFactory.filter(F.action == "switch"))
async def next_page_devices(callback: CallbackQuery, state: FSMContext, callback_data: DeviceCallbackFactory):
    switch = callback_data.value
    data = await state.get_data()
    page = data['page']
    devices_addresses = data['devices_addresses']
    devices_ids = data['cities_ids']
    await callback.message.delete()
    if not (page == 0) or not (page * 20 >= len(devices_ids)):
        if switch == 'next_c':
            await state.update_data(page=int(page) + 1)
            await callback.message.answer(text=html.quote(texts.choose_city_switch()),
                                          reply_markup=d_get_kb(len(devices_addresses), devices_addresses, devices_ids,
                                                                page + 1))
        else:
            await state.update_data(page=int(page) - 1)
            await callback.message.answer(text=html.quote(texts.choose_city_switch()),
                                          reply_markup=d_get_kb(len(devices_ids), devices_addresses, devices_ids,
                                                                page - 1))
