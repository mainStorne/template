from fastapi_users import FastAPIUsers as APIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
)
from ..db.models.users import User
from ..dependencies.auth import get_strategy, get_user_manager





transport = BearerTransport(tokenUrl='api/auth/jwt/login')

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=transport,
    get_strategy=get_strategy,
)


class FastAPIUsers(APIUsers[User, int]):
    pass


fastapi_users = FastAPIUsers(get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
