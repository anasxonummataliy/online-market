from builtins import str
from aiogram import Bot, Router, F
from aiogram.enums import ParseMode
from aiogram.types import (
    Message,
    InlineQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
    SwitchInlineQueryChosenChat,
)
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.sub_menu import MY_REFERRALS
from database import User

referrals_router = Router()


@referrals_router.message(F.text == __(MY_REFERRALS))
async def my_referrals(msg: Message, bot: Bot):
    count = await User.get_referrals_count(msg.from_user.id)

    await msg.answer(
        _(
            "<b>🎁 Your Referrals</b>\n\n" "👥 Total invited users: <b>{count}</b>"
        ).format(count=count),
        parse_mode=ParseMode.HTML,
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("📨 Share invite link"),
                    switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat(
                        query="ref",
                        allow_user_chats=True,
                        allow_group_chats=True,
                        allow_supergroup_chats=True,
                        allow_channel_chats=False,
                    ),
                )
            ]
        ]
    )

    await msg.answer(
        _("Tap the button below to choose a chat and share your invite link."),
        reply_markup=kb,
    )


@referrals_router.inline_query()
async def referral_inline_handler(query: InlineQuery, bot: Bot):

    if query.query != "ref":
        await query.answer([], cache_time=1, is_personal=True)
        return

    link = await create_start_link(bot, str(query.from_user.id), encode=True)

    share_text = _(
        "🎉 <b>You are invited!</b>\n\n"
        "Join our bot using my personal invite link below.\n\n"
        "🔗 <code>{link}</code>"
    ).format(link=link)

    result = InlineQueryResultArticle(
        id="share_referral",
        title=_("Send invite link"),
        description=_("Share your personal referral link"),
        input_message_content=InputTextMessageContent(
            message_text=share_text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        ),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=_("🚀 Open bot"),
                        url=link,
                    )
                ]
            ]
        ),
    )

    await query.answer(
        results=[result],
        cache_time=1,
        is_personal=True,
    )
