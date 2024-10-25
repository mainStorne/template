from fastapi import APIRouter

from ..schemas.users import UserCreate, UserRead, UserUpdate
from ..authentication.users import auth_backend, fastapi_users
from .endpoints import {{cookiecutter.model}}


api = APIRouter()

api.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
api.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
api.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
api.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
api.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
api.include_router(
    {{cookiecutter.model}}.router,
    prefix='/{{cookiecutter.model_plural}}',
    tags=['{{cookiecutter.model_plural}}']
)