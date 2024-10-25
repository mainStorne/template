from fastapi import Depends
from ..managers.user import UserManager
from ..db.adapters.users import UserAdapter, TokenAdapter
from sqlalchemy.ext.asyncio import AsyncSession
from .session import get_async_session
from ..db.models.users import User, Token
from fastapi_users.authentication.strategy import DatabaseStrategy


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield UserAdapter(session, User)


async def get_token_db(session: AsyncSession = Depends(get_async_session)):
    yield TokenAdapter(session, Token)


async def get_strategy(token=Depends(get_token_db)):
    return DatabaseStrategy(token, lifetime_seconds=3600)


async def get_user_manager(user_db: UserAdapter = Depends(get_user_db)):
    yield UserManager(user_db)
