import os
import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from sqlalchemy import create_engine
from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy_file.storage import StorageManager
from starlette_admin.contrib.sqla import Admin, ModelView

from bot.config import conf
from database.models import Product, User, Category
from web.provider import UsernameAndPasswordProvider

middleware = [
    Middleware(SessionMiddleware, secret_key=conf.web.SECRET_KEY),
]

app = Starlette(middleware=middleware)


sync_engine = create_engine(conf.db.db_url.replace("asyncpg", "psycopg2"), echo=True)

logo_url = "https://cdn-icons-png.flaticon.com/512/5968/5968705.png"
admin = Admin(
    engine=sync_engine,
    title="Aiogram Admin Panel",
    base_url="/admin",
    logo_url=logo_url,
    auth_provider=UsernameAndPasswordProvider(),
)


class CategoryModelView(ModelView):
    exclude_fields_from_list = ("created_at", "updated_at", "image")
    exclude_fields_from_create = ("created_at", "updated_at")
    exclude_fields_from_edit = ("created_at", "updated_at")


class UserModelView(ModelView):
    pass


class ProductModelView(ModelView):
    exclude_fields_from_list = ("created_at", "updated_at", "image")
    exclude_fields_from_create = ("created_at", "updated_at")
    exclude_fields_from_edit = ("created_at", "updated_at")


admin.add_view(ProductModelView(Product))
admin.add_view(UserModelView(User))
admin.add_view(CategoryModelView(Category))

admin.mount_to(app)

os.makedirs("./media/attachment", mode=0o777, exist_ok=True)
container = LocalStorageDriver("./media").get_container("attachment")
try:
    StorageManager.add_storage("default", container)
except RuntimeError:
    pass

if __name__ == "__main__":
    uvicorn.run("web.app:app", host="0.0.0.0", port=8000, reload=False)
