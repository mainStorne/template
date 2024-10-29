from typing import Optional, TypeVar
from pydantic import EmailStr, BaseModel

class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
