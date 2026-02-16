from aiogram import Bot, Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.i18n import gettext as _


from bot.buttons.sub_menu import MY_REFERRALS

referrals_router = Router()


@referrals_router.message(F.text == MY_REFERRALS)
async def my_referrals(msg: Message, bot: Bot):
    link = await create_start_link(bot, str(msg.from_user.id), encode=True)
    n = 15
    text = _(
        "✨ Number of people you invited: <b>{n}</b>\n"
        '🔗 Invitation link: <a href="{link}">Click to enter</a>'
    ).format(n=n, link=link)

    await msg.answer(text, parse_mode=ParseMode.HTML)


# "✨ Siz taklif qilganlar soni: <b>{n}</b>🔗 Taklif havolasi: <a href="{link}">Bosish orqali kirish"
