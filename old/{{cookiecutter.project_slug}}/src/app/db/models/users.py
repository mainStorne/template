from fastapi_users.db import SQLAlchemyBaseUserTable
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTable
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import mapped_column, Mapped
from .base import Base, IDMixin


class User(IDMixin, SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'
    {% if cookiecutter.required_username %}
    username: Mapped[str] = mapped_column(String(length=256), unique=True) {% endif %}



class Token(SQLAlchemyBaseAccessTokenTable[int], Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='cascade'), nullable=False)
