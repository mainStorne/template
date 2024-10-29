from .base import Base
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
{% if cookiecutter.model_id == 'int' %}
from .base import IDMixin
{% endif %}

class {{cookiecutter.model_info.upper_name}}(IDMixin, Base):
    __tablename__ = '{{cookiecutter.model_plural}}'


