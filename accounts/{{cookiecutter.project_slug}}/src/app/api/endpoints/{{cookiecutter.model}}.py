from ...fastapi_crud_toolkit import FastAPICrudToolkit
from fastapi_sqlalchemy_toolkit import ModelManager
from ...dependencies.session import get_async_session
from ...db.models import {{cookiecutter.model_info.upper_name}}
from ...schemas.{{cookiecutter.model}} import {{cookiecutter.model_info.upper_name}}Create, {{cookiecutter.model_info.upper_name}}Update, {{cookiecutter.model_info.upper_name}}Read
from ...authentication.users import fastapi_users

manager = ModelManager({{cookiecutter.model_info.upper_name}})

router = FastAPICrudToolkit(
    manager,
    get_async_session,
    {{cookiecutter.model_info.upper_name}}Create,
    {{cookiecutter.model_info.upper_name}}Update,
    {{cookiecutter.model_info.upper_name}}Read,
    fastapi_users.authenticator
).get_crud_router()

