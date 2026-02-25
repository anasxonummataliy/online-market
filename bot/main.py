import os
import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import FSMI18nMiddleware, I18n

from bot.config import conf
from bot.inlinemode import inline_router
from database import db
from bot.handlers.private import main_router
from sqlalchemy_file.storage import StorageManager
from libcloud.storage.drivers.local import LocalStorageDriver

dp = Dispatcher()
bot = Bot(conf.bot.TOKEN)


@dp.startup()
async def startup(bot: Bot):
    os.makedirs("./media/attachment", mode=0o777, exist_ok=True)
    container = LocalStorageDriver("./media").get_container("attachment")
    try:
        StorageManager.add_storage("default", container)
    except RuntimeError:
        pass
    await db.create_all()
    await bot.send_message(chat_id=conf.bot.ADMIN, text="Bot started.✅")


@dp.shutdown()
async def shutdown(bot: Bot):
    # await db.drop_all()
    await bot.send_message(chat_id=conf.bot.ADMIN, text="Bot stopped.🛑")


async def main():
    i18n = I18n(path="locales", default_locale="en")
    dp.update.outer_middleware(FSMI18nMiddleware(i18n))
    dp.include_routers(main_router)
    dp.include_routers(inline_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
