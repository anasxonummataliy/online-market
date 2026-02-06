import os
import uvicorn
from starlette.middleware import Middleware
from libcloud.storage.drivers.local import LocalStorageDriver
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView
from starlette_admin.contrib.sqla.admin import Middleware, Starlette
from sqlalchemy_file.storage import StorageManager


from bot.config import conf
from database.models import Product, User, Category
import database.base as base
from web.provider import UsernameAndPasswordProvider


middleware = [
    Middleware(SessionMiddleware, secret_key=conf.web.SECRET_KEY),
]

app = Starlette(middleware=middleware)

logo_url = "https://cdn-icons-png.flaticon.com/512/5968/5968705.png"
admin = Admin(
    engine=base.db._engine,
    title="Aiogram Admin Panel",
    base_url="/",
    logo_url=logo_url,
    auth_provider=UsernameAndPasswordProvider(),
)


class ProductModelView(ModelView):
    exclude_fields_from_list = ("created_at", "updated_at")
    exclude_fields_from_create = ("created_at", "updated_at")
    exclude_fields_from_edit = ("created_at", "updated_at")


class UserModelView(ModelView):
    exclude_fields_from_edit = ("created_at", "updated_at")


class CategoryModelView(ModelView):
    exclude_fields_from_create = ("created_at", "updated_at")
    exclude_fields_from_edit = ("created_at", "updated_at")


admin.add_view(ProductModelView(Product))
admin.add_view(UserModelView(User))
admin.add_view(CategoryModelView(Category))

admin.mount_to(app)

os.makedirs("./media/attachment", mode=0o777, exist_ok=True)
container = LocalStorageDriver("./media").get_container("attachment")
StorageManager.add_storage("default", container)


if __name__ == "__main__":
    uvicorn.run("web.app:app", host="0.0.0.0", port=8000, reload=True)
