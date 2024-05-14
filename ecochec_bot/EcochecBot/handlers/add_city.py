from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from .. import texts
from ..kbs.main_kb import get_main_kb
from ..kbs.cancel import cancel_kb
from db_func import is_admin, add_city, check_city


router = Router()


class AddCity(StatesGroup):
    city = State()


@router.message(F.text.lower() == 'добавить город')
async def add_city_msg(message: Message, state: FSMContext):
    if is_admin(str(message.from_user.id)):
        await message.answer('Введите название города', reply_markup=cancel_kb)
        await state.set_state(AddCity.city)


@router.message(AddCity.city)
async def get_city(message: Message, state: FSMContext):
    if not check_city(message.text):
        city_id = add_city(str(message.text))
        await message.answer(text=texts.add_city(message.text, city_id), reply_markup=get_main_kb(message.from_user.id))
    else:
        await message.answer(text=texts.error_city(), reply_markup=get_main_kb(message.from_user.id))
    await state.clear()