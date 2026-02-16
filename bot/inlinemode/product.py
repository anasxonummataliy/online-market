from aiogram import Router
from aiogram.utils.deep_linking import create_deep_link
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton,
)

from database import Product


inline_router = Router()


@inline_router.inline_query()
async def get_inline_query(query: InlineQuery):
    results = []
    if len(query.query):
        products = await Product.filter_startwith(query.query)
    else:
        products = await Product.get_all()

    bot_data = await query.bot.me()

    for product in products:
        link = create_deep_link(
            bot_data.username, "start", f"product_{product.id}", encode=True
        )
        ikm = InlineKeyboardBuilder()
        ikm.row(InlineKeyboardButton(text=_("Add to Cart 🛒"), url=link))

        results.append(
            InlineQueryResultArticle(
                id=str(product.id),
                title=f"{product.name},\n{product.price} 💵",
                description=product.description,
                input_message_content=InputTextMessageContent(
                    message_text=f"{product.name}\n{product.price}＄"
                ),
                reply_markup=ikm.as_markup(),
            )
        )

    await query.answer(results, cache_time=0)
