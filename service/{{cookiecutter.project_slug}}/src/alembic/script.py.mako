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
import app.managers.{{cookiecutter.model}} import {{cookiecutter.model_info.upper_name}}Manager
import app.schemas.{{cookiecutter.model}} import {{cookiecutter.model_info.upper_name}}Read
import app.db.models.{{cookiecutter.model}} import {{cookiecutter.model_info.upper_name}}
from polyfactory.factories.pydantic_factory import ModelFactory{% endif %}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    {% if cookiecutter.need_test_data %}
    class Factory(ModelFactory[{{cookiecutter.model_info.upper_name}}Read]): ...

    manager = {{cookiecutter.model_info.upper_name}}Manager({{cookiecutter.model_info.upper_name}})

    def generate_seeds(loops: int) -> list[{{cookiecutter.model_info.upper_name}}Read]:
        seeds = []
        for _ in range(loops):
            seeds.append(
                Factory.build()
            )
        return seeds
    seeds = generate_seeds(30)

    async def generate(session):
        await manager.bulk_create(session, seeds, returning=False)

    op.run_async(generate)
    {% endif %}
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
