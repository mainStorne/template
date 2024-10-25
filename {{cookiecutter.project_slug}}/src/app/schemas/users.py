from typing import Optional, TypeVar
from pydantic import EmailStr, ConfigDict
from fastapi_users.schemas import CreateUpdateDictModel
from fastapi_sqlalchemy_toolkit import make_partial_model

class UserBase(CreateUpdateDictModel):
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    {% if cookiecutter.required_username %}
    username: str
    email: Optional[EmailStr] = None
    {% else %}
    email: EmailStr{% endif %}
    model_config = ConfigDict(from_attributes=True)




class UserRead(UserBase):
    id: int


class UserCreate(UserBase):
    password: str


UserUpdate = make_partial_model(UserCreate)

UC = TypeVar('UC', bound=UserCreate)
