from typing import Callable, Any, Coroutine, Annotated
from httpx import AsyncClient
from .utils import validate
from .conf import settings
from .schemas.users import UserRead
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from .fastapi_crud_toolkit.authenticator import BaseAuthenticator

auth_scheme = OAuth2PasswordBearer(tokenUrl=settings.SERVICE_ACCOUNTS_URL + '/api/jwt')


class Authenticator(BaseAuthenticator):

    def current_user(self, optional: bool = False,
                     active: bool = False,
                     verified: bool = False,
                     superuser: bool = False) -> Callable[[Any], Coroutine[Any, Any, Any]]:
        async def get_user_info(
                token: Annotated[str, Depends(auth_scheme)]
        ) -> UserRead:

            async with AsyncClient() as cli:
                user = validate(UserRead,
                                await cli.get(settings.SERVICE_ACCOUNTS_URL + '/users/me', headers={'Bearer': token}))

            status_code = status.HTTP_403_FORBIDDEN
            if active and not user.is_active:
                status_code = status.HTTP_401_UNAUTHORIZED
                user = None
            elif (
                    verified and not user.is_verified or superuser and not user.is_superuser
            ):
                user = None
            if not user and not optional:
                raise HTTPException(status_code=status_code)
            return user

        return get_user_info
