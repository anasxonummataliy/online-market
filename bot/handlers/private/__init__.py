from aiogram import Router

from .admin import admin_product, admin_menu, admin_category

main_router = Router()
main_router.include_routers(
    admin_menu,
    admin_category,
    admin_product,
)
