import os
import uvicorn
from sqlalchemy import create_engine
from starlette_admin import FileField
from starlette.middleware import Middleware
from starlette.applications import Starlette
from sqlalchemy_file.storage import StorageManager
from starlette_admin.contrib.sqla import Admin, ModelView
from starlette.middleware.sessions import SessionMiddleware
from libcloud.storage.drivers.local import LocalStorageDriver

from bot.config import conf
from database.models import Product, User, Category, Order, OrderItem
from web.provider import UsernameAndPasswordProvider

middleware = [Middleware(SessionMiddleware, secret_key=conf.web.SECRET_KEY)]

app = Starlette(middleware=middleware)

sync_engine = create_engine(
    conf.db.db_url.replace("+asyncpg", ""), echo=False, pool_pre_ping=True
)
admin = Admin(
    sync_engine,
    title="Aiogram Admin Panel",
    base_url="/",
    logo_url="https://cdn-icons-png.flaticon.com/512/5968/5968705.png",
    auth_provider=UsernameAndPasswordProvider(),
)


class ProductModelView(ModelView):
    fields = [
        "id",
        "name",
        "description",
        "price",
        "quantity",
        "category",
        FileField("image", label="Upload Image", required=False),  # Fayl upload maydoni
    ]


class UserModelView(ModelView):
    fields = ["id", "fullname", "username", "phone_number", "type"]


admin.add_view(ModelView(Category))
admin.add_view(ProductModelView(Product))
admin.add_view(UserModelView(User))
admin.add_view(ModelView(Order))
admin.add_view(ModelView(OrderItem))

admin.mount_to(app)

os.makedirs("./media/attachment", mode=0o777, exist_ok=True)
container = LocalStorageDriver("./media").get_container("attachment")
try:
    StorageManager.add_storage("default", container)
except RuntimeError:
    pass

if __name__ == "__main__":
    uvicorn.run("web.app:app", host="0.0.0.0", port=8000, reload=True)
