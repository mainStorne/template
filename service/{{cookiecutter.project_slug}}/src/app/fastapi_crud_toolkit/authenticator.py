from typing import Protocol, Coroutine, Callable, Any

from fastapi_sqlalchemy_toolkit import ModelManager


class BaseAuthenticator(Protocol):
    def __init__(self, manager: ModelManager):
        self.manager = manager
