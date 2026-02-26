from typing import Any, Dict
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject
from aiogram.utils.i18n import I18nMiddleware

from database import User


class DBi18nMiddleware(I18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        from_user = data.get("event_from_user")
        if not from_user:
            return self.i18n.default_locale

        state: FSMContext = data.get("state")

        if state:
            state_data = await state.get_data()
            locale = state_data.get("locale")

            if locale:
                return locale

        user = await User.get_user(tg_id=from_user.id)
        locale = user.locale if user and user.locale else self.i18n.default_locale

        if state:
            await state.update_data(locale=locale)

        return locale
