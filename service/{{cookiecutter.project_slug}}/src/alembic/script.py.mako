"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy
${imports if imports else ""}
{% if cookiecutter.need_test_data %}
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from app.managers.{{cookiecutter.model}} import {{cookiecutter.model_info.upper_name}}Manager
from app.schemas.{{cookiecutter.model}} import {{cookiecutter.model_info.upper_name}}Read
from app.db.models.{{cookiecutter.model}} import {{cookiecutter.model_info.upper_name}}
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

class MFactory(ModelFactory[{{cookiecutter.model_info.upper_name}}Read]): ...

class Factory(SQLAlchemyFactory):
    __is_base_factory__ = True
    # __set_relationships__ = True{% endif %}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}



def upgrade() -> None:
    ${upgrades if upgrades else "pass"}
    {% if cookiecutter.need_test_data %}


    async def seed_db(connection: AsyncConnection):
        session = AsyncSession(bind=connection, expire_on_commit=False)
        Factory.__async_session__ = session
        u_factory = Factory.create_factory({{cookiecutter.model_info.upper_name}})
        for i in range(10):
            await u_factory.create_async()


    op.run_async(seed_db)
    {% endif %}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
