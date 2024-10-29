from typing import Callable, Any, Coroutine, Annotated
from .conf import settings
from .dependencies.session import get_session
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from .fastapi_crud_toolkit.authenticator import BaseAuthenticator
from fastapi_sqlalchemy_toolkit import ModelManager
from .storage.db.models import User
import jwt

auth_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)


class Authenticator(BaseAuthenticator):

    def current_user(self,
                     role: str | None = False,
                     optional: bool = False,
                     active: bool = False,
                     verified: bool = False,
                     superuser: bool = False,
                     ) -> Callable[[Any], Coroutine[Any, Any, Any]]:
        async def get_user_info(
                token: Annotated[str, Depends(auth_scheme)], session=Depends(get_session)
        ) -> User:
            try:
                payload = jwt.decode(
                    token,
                    settings.JWT_PRIVATE_KEY,
                    audience=settings.JWT_AUDIENCE,
                    algorithms=settings.JWT_ALGORITHM,
                )
                user_id = int(payload['sub'])
            except (KeyError, jwt.PyJWTError, ValueError):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            user: User = await self.manager.get(session, id=user_id)
            status_code = status.HTTP_401_UNAUTHORIZED
            if user:
                status_code = status.HTTP_403_FORBIDDEN
                if active and not user.is_active or user.role != role:
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
