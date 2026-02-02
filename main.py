from sqlalchemy import create_engine
from config import conf
import db.models
from db.base import Base


import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.types import Message

from config import conf

dp = Dispatcher()
bot = Bot(conf.bot.TOKEN)


async def startup(bot: Bot):
    engine = create_engine(conf.db.db_url)
    Base.metadata.create_all(engine)
    print("yaratildi")
    await bot.send_message(chat_id=8122865725, text="ishga tushdi")


async def main():
    dp.startup.register(startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
