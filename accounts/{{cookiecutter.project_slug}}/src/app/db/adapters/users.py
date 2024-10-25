from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from sqlalchemy import select
from ...db.models.users import User


class TokenAdapter(SQLAlchemyAccessTokenDatabase[int]):
    pass


class UserAdapter(SQLAlchemyUserDatabase[int, User]):
    {% if cookiecutter.required_username %}
    async def get_by_username(self, username: str):
        stmt = select(self.user_table).where(self.user_table.username == username)
        return await self._get_user(stmt)
    {% else %}
    pass

    {% endif %}


