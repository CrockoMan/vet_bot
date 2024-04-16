import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ChatAction, ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (BotCommand, BotCommandScopeDefault, KeyboardButton,
                           ReplyKeyboardMarkup)
from aiogram.utils import markdown
from aiogram import F
from aiogram.utils.chat_action import ChatActionSender

from config import ButtonText
from get_schedule import get_random_picture, read_schedule

dp = Dispatcher()

router = Router(name=__name__)
dp.include_router(router)


async def get_rasp_str():
    ret_arr = []
    schedule = await read_schedule()
    for dat in schedule.items():
        ret_str = ''
        ret_str += f'{markdown.hbold(dat[0])}\n'
        for lesson in dat[1]:
            ret_str += f"{' '.join(lesson)}\n"
        ret_arr.append(ret_str)

    return ret_arr


@router.message(F.text == ButtonText.SCHEDULE)
async def handle_message_bye(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    print(f'Запрос расписания {message.from_user.id} {message.from_user.full_name}')
    rasp = await get_rasp_str()
    if len(rasp) > 0:
        for one_day_rasp in rasp:
            await message.answer(text=f'{one_day_rasp}')
    else:
        await message.answer(text='Ошибка загрузки расписания, попробуйте '
                                  'позже')


@router.message(F.text == ButtonText.COOL_PHOTO)
async def handle_send_photo(message: types.Message, bot: Bot):
    action_sender = ChatActionSender(
        bot=message.bot,
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    )
    print(f'Запрос фото {message.from_user.id} {message.from_user.full_name}')
    async with action_sender:
        url = await get_random_picture()
        if url:
            await bot.send_photo(chat_id=message.chat.id, photo=url)
        else:
            await message.answer(
                text='Ошибка загрузки картинки, попробуйте позже'
            )


def get_on_start_kb():
    button_rasp = KeyboardButton(text=ButtonText.SCHEDULE)
    button_photo = KeyboardButton(text=ButtonText.COOL_PHOTO)
    first_row = [button_rasp]
    second_row = [button_photo]
    button_rows = [first_row, second_row]
    markup_keyboard = ReplyKeyboardMarkup(keyboard=button_rows,
                                          resize_keyboard=True,
                                          )
    return markup_keyboard


@router.message(CommandStart())
async def handle_start(message: types.Message):
    url = 'https://kubsau.ru/local/templates/kit/img/logo.svg'
    text = markdown.text(f'{markdown.hide_link(url)}Привет '
                         f'{markdown.hbold(message.from_user.full_name)}\n',
                         f'id={markdown.hbold(message.from_user.id)}')
    await message.answer(text=text,
                         reply_markup=get_on_start_kb())


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    print(BOT_TOKEN)
    bot = Bot(
        token=BOT_TOKEN,
        parse_mode=ParseMode.HTML
    )

    await bot.delete_webhook()
    await set_commands(bot)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
