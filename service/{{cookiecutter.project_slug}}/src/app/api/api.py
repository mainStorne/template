from fastapi import APIRouter
from .endpoints import {{cookiecutter.model}}


api = APIRouter()

api.include_router(
    {{cookiecutter.model}}.r,
    prefix='/{{cookiecutter.model_plural}}',
    tags=['{{cookiecutter.model_plural}}']
)