from datetime import datetime
from typing import Optional, TypeVar
from pydantic import EmailStr, BaseModel
from fastapi_users import schemas
from fastapi_sqlalchemy_toolkit import make_partial_model


class {{cookiecutter.model_info.upper_name}}Base(BaseModel):
    pass

class {{cookiecutter.model_info.upper_name}}Read({{cookiecutter.model_info.upper_name}}Base):
    pass

class {{cookiecutter.model_info.upper_name}}Create({{cookiecutter.model_info.upper_name}}Base):
    pass


{{cookiecutter.model_info.upper_name}}Update = make_partial_model({{cookiecutter.model_info.upper_name}}Create)

