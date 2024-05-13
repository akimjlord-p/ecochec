from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from .. import texts
from ..kbs.kb_to_choose_city import c_get_kb, CityCallbackFactory
from ..kbs.main_kb import get_main_kb
from ..kbs.cancel import cancel_kb
from ..db_func import get_cities, add_user, get_city_by_id, check_user, change_city
from aiogram import html

router = Router()


class AddUser(StatesGroup):
    id_tg = State()
    cities = State()
    cities_ids = State()
    city_id = State()
    page = State()


@router.message(F.text.lower() == 'сменить город')
@router.message(F.text.lower() == 'выбрать город')
async def choose_city_msg(message: Message, state: FSMContext):
    cities_info = get_cities()
    kb = c_get_kb(len(cities_info), [city['city'] for city in cities_info],
                    [city['city_id'] for city in cities_info], 0)
    await state.set_state(AddUser.city_id)
    await state.update_data(cities=[city['city'] for city in cities_info],
                            cites_ids=[city['city_id'] for city in cities_info], page=0)
    await message.answer(text=texts.list_of_cities(), reply_markup=cancel_kb)
    await message.answer(text=html.quote(texts.choose_city_switch()), reply_markup=kb)


@router.callback_query(AddUser.city_id, CityCallbackFactory.filter(F.action == 'city'))
async def get_class(callback: CallbackQuery, state: FSMContext, callback_data: CityCallbackFactory):
    city_id = callback_data.value
    data = await state.get_data()
    if not check_user(str(callback.from_user.id)):
        add_user(str(callback.from_user.id), str(city_id))
        city = get_city_by_id(city_id)
        await callback.message.answer(text=texts.set_city(city), reply_markup=get_main_kb(callback.from_user.id))
        await state.clear()
    else:
        change_city(str(callback.from_user.id), city_id=callback_data.value)
        city = get_city_by_id(city_id)
        await callback.message.answer(text=texts.set_city(city), reply_markup=get_main_kb(callback.from_user.id))


@router.callback_query(AddUser.city_id, CityCallbackFactory.filter(F.action == "switch"))
async def next_page_cities(callback: CallbackQuery, state: FSMContext, callback_data: CityCallbackFactory):
    switch = callback_data.value
    data = await state.get_data()
    page = data['page']
    cities = data['cities']
    cities_ids = data['cities_ids']
    await callback.message.delete()
    if not (page == 0) or not (page * 20 >= len(cities_ids)):
        if switch == 'next_c':
            await state.update_data(page=int(page) + 1)
            await callback.message.answer(text=html.quote(texts.choose_city_switch()),
                                          reply_markup=c_get_kb(len(cities), cities, cities_ids, page + 1))
        else:
            await state.update_data(page=int(page) - 1)
            await callback.message.answer(text=html.quote(texts.choose_city_switch()),
                                          reply_markup=c_get_kb(len(cities_ids), cities, cities_ids, page - 1))



