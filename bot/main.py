import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n

from bot.config import conf
from bot.middleware.i18n import DBi18nMiddleware
from database import db
from bot.handlers.private import main_router

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


async def main():
    i18n = I18n(path="locales", default_locale="en", domain="messages")
    dp.update.outer_middleware(DBi18nMiddleware(i18n))
    dp.include_router(main_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
