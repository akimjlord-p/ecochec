from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from ecochec_bot.EcochecBot.texts import get_start_text, info, admin_info
from ..kbs.main_kb import get_main_kb
from db_func import is_admin


router = Router()



@router.message(Command('start'))
async def start_cmd(message: Message):
    await message.answer(text=get_start_text(message.from_user.id), reply_markup=get_main_kb(message.from_user.id))


@router.message(StateFilter(None), Command(commands=["cancel"]))
@router.message(default_state, F.text.lower() == "отмена")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    kb = get_main_kb(message.from_user.id)
    await state.set_data({})
    await message.answer(
        text="Нечего отменять",
        reply_markup=kb)


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    kb = get_main_kb(message.from_user.id)
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=kb)


@router.message(F.text.lower() == 'информация')
async def msg_info(message: Message):
    kb = get_main_kb(message.from_user.id)
    await message.answer(text=info(), reply_markup=kb)


@router.message(F.text.lower() == 'admin')
async def msg_info(message: Message):
    if is_admin(str(message.from_user.id)):
        kb = get_main_kb(message.from_user.id)
        await message.answer(text=admin_info(), reply_markup=kb)

