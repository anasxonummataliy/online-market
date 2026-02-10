from aiogram import Router

from .product import product_router
from .menu import menu_router, start_handler
from .referrals import referrals_router
from .settings import settings_router
from .admin import admin_product, admin_menu, admin_category

main_router = Router()
main_router.include_routers(
    product_router,
    menu_router,
    referrals_router,
    settings_router,
    admin_menu,
    admin_category,
    admin_product,
)
