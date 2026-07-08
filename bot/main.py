import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import FSMI18nMiddleware, I18n

from bot.config import conf
from database import db
from database.models import User

dp = Dispatcher()
bot = Bot(conf.bot.TOKEN)


@dp.startup()
async def startup(bot: Bot):
    await bot.delete_webhook()
    await db.create_all()
    await bot.send_message(chat_id=conf.bot.ADMIN, text="Bot started. ✅")


@dp.shutdown()
async def shutdown(bot: Bot):
    await bot.send_message(chat_id=conf.bot.ADMIN, text="Bot stopped. 🛑")


@dp.message(CommandStart())
async def start_handler(message: Message):
    tg_id = message.from_user.id

    user = await User.get_user(tg_id=tg_id)
    if not user:
        admin_id = int(conf.bot.ADMIN) if conf.bot.ADMIN else None
        is_admin = admin_id is not None and tg_id == admin_id
        user = await User.create(
            tg_id=tg_id,
            fullname=message.from_user.full_name,
            username=message.from_user.username,
            type=User.Type.ADMIN if is_admin else User.Type.USER,
            locale="en",
        )
    else:
        admin_id = int(conf.bot.ADMIN) if conf.bot.ADMIN else None
        if admin_id and tg_id == admin_id and not user.is_admin:
            await User.update(tg_id=tg_id, type=User.Type.ADMIN)
            user = await User.get_user(tg_id=tg_id)

    if user.is_admin:
        markup = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Admin 🧑‍💼")]],
            resize_keyboard=True,
        )
        await message.answer("Xush kelibsiz, Admin! 👋", reply_markup=markup)
    else:
        await message.answer("Siz admin emassiz.")


def setup_routers():
    from bot.handlers.private.admin.menu import admin_menu
    from bot.handlers.private.admin.category import admin_category
    from bot.handlers.private.admin.product import admin_product
    dp.include_router(admin_menu)
    dp.include_router(admin_category)
    dp.include_router(admin_product)


async def main():
    setup_routers()
    i18n = I18n(path="locales", default_locale="en", domain="messages")
    dp.update.outer_middleware(FSMI18nMiddleware(i18n))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
