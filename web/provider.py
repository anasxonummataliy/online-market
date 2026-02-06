import bcrypt
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

from bot.config import conf


class UsernameAndPasswordProvider(AuthProvider):
    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        if len(username) < 3:
            raise FormValidationError("Username must be at least 3 characters long.")

        if username == conf.web.USERNAME and bcrypt.checkpw(
            password.encode(),
            conf.web.PASSWORD.encode(),
        ):
            request.session.update({"username": username})
            return response

        raise LoginFailed("Invalid username or password.")

    async def is_authenticated(self, request: Request):
        if request.session.get("username") == conf.web.USERNAME:
            request.state.user = conf.web.USERNAME
            return True
        return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        return AdminConfig(app_title="Admin Page")

    def get_admin_user(self, request: Request) -> AdminUser:
        return AdminUser(username=request.state.user)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
