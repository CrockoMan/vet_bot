import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils import markdown

from config import ButtonText, DEFAULT_GROUP
from db import save_group

register_router = Router(name=__name__)


class RegisterGroup(StatesGroup):
    group_name = State()


@register_router.message(F.text == ButtonText.SET_GROUP)
async def start_register_group(message: Message, state: FSMContext):
    await message.answer('Для получения расписания\n'
                         'введите номер своей группы\n\n'
                         f'Формат ввода номера группы: {DEFAULT_GROUP}')
    await state.set_state(RegisterGroup.group_name)


@register_router.message(RegisterGroup.group_name)
async def register_group_number(message: Message, state: FSMContext):
    await state.update_data(group_name=message.text.upper())
    reg_data = await state.get_data()
    group_name = reg_data.get('group_name').upper()

    group_pattern = re.compile(r'(?P<group_name>\D{2}\d{4})')

    matches = group_pattern.search(group_name)

    if matches:
        await message.answer(
            '✅ Твоя группа сохранена!\n'
            'Теперь расписание будешь получать '
            f'для группы {markdown.hbold(matches.group("group_name"))}')
        await state.clear()
        save_group(message.from_user.id, matches.group("group_name"))
    else:
        await message.answer('⚠️ Номер группы указан в неверном формате\n'
                             f'Формат ввода номера группы: '
                             f'{markdown.hbold(DEFAULT_GROUP)}')
