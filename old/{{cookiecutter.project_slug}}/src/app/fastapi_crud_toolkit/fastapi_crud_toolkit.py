from fastapi_sqlalchemy_toolkit import ModelManager
from fastapi_users.authentication import Authenticator
from pydantic import BaseModel
from .crud import get_crud_router
class FastAPICrudToolkit:

    def __init__(self, manager: ModelManager, get_session, read_scheme: type[BaseModel],
                 create_scheme: type[BaseModel], update_scheme: type[BaseModel],
                 authenticator: Authenticator):
        self.authenticator = authenticator
        self.update_scheme = update_scheme
        self.read_scheme = read_scheme
        self.get_session = get_session
        self.create_scheme = create_scheme
        self.model_manager = manager

    def get_crud_router(self):
        return get_crud_router(
            self.model_manager,
            self.get_session,
            self.read_scheme,
            self.create_scheme,
            self.update_scheme,
            self.authenticator,
        )

