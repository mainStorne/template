from httpx import AsyncClient
from sqlalchemy.sql.annotation import Annotated

from .utils import validate
from .conf import settings
from .schemas.users import UserRead
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

auth_scheme = OAuth2PasswordBearer(tokenUrl=settings.SERVICE_AUTH_URL + '/api/jwt')


def current_user(
        optional: bool = False,
        active: bool = False,
        verified: bool = False,
        superuser: bool = False,
):
    async def get_user_info(
            token: Annotated[str, Depends(auth_scheme)]
    ) -> UserRead:

        async with AsyncClient() as cli:
            user = validate(UserRead,
                            await cli.get(settings.SERVICE_AUTH_URL + '/api/users/me', headers={'Bearer': token}))

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
