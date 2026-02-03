import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import conf
from database.base import db
from bot.handlers.private.menu import menu_router

dp = Dispatcher()
bot = Bot(conf.bot.TOKEN)


async def startup(bot: Bot):
    await db.create_all()
    print("yaratildi")
    await bot.send_message(chat_id=8122865725, text="ishga tushdi")


async def main():
    dp.include_router(menu_router)
    dp.startup.register(startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
