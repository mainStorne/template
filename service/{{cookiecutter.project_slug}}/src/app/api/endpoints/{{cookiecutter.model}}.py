from ...dependencies.session import get_session
from ...db.models import {{cookiecutter.model_info.upper_name}}
from ...schemas.{{cookiecutter.model}} import {{cookiecutter.model_info.upper_name}}Create, {{cookiecutter.model_info.upper_name}}Update, {{cookiecutter.model_info.upper_name}}Read
from fastapi_sqlalchemy_toolkit import ModelManager
from ...fastapi_crud_toolkit import FastAPICrudToolkit
from ...authenticator import Authenticator
from ...managers.{{cookiecutter.model}} import {{cookiecutter.model}}Manager

authenticator = Authenticator()
manager = {{cookiecutter.model}}Manager({{cookiecutter.model_info.upper_name}})

r = FastAPICrudToolkit(
    manager,
    get_session,
{{cookiecutter.model_info.upper_name}}Create, {{cookiecutter.model_info.upper_name}}Update, {{cookiecutter.model_info.upper_name}}Read,
    authenticator,
).get_crud_router()