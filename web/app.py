import bcrypt
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

from bot.config import conf

class UsernameAndPasswordProvider(AuthProvider):

