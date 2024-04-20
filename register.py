import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils import markdown

from config import ButtonText
from db import DB, UserGroup, get_group, save_group

register_router = Router(name=__name__)


class RegisterGroup(StatesGroup):
    group_name = State()


@register_router.message(F.text == ButtonText.SET_GROUP)
async def start_register_group(message: Message, state: FSMContext):
    await message.answer('Для получения расписания\n'
                         'введите номер своей группы\n\n'
                         'Формат ввода номера группы: ВМ2233')
    await state.set_state(RegisterGroup.group_name)


@register_router.message(RegisterGroup.group_name)
async def register_group_number(message: Message, state: FSMContext):
    await state.update_data(group_name=message.text.upper())
    reg_data = await state.get_data()
    group_name = reg_data.get('group_name').upper()

    group_pattern = r'\D{2}\d{4}'
    matches = re.findall(group_pattern, group_name)

    if matches:
        await message.answer('✅ Твоя группа сохранена!\n'
                             'Теперь расписание будешь получать '
                             f'для группы {markdown.hbold(matches)}')
        await state.clear()
        save_group(message.from_user.id, matches)
    else:
        await message.answer('⚠️ Номер группы указан в неверном формате\n'
                             f'Формат ввода номера группы: '
                             f'{markdown.hbold("ВМ2233")}')
