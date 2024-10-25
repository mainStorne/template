from fastapi import FastAPI
from .api.api import api
{% if cookiecutter.is_debug %}
from contextlib import asynccontextmanager
from .conf import engine
from .db.setup import create_db_and_tables

@asynccontextmanager
async def lifespan(app):
    await create_db_and_tables(engine)
    yield

app = FastAPI(lifespan=lifespan)
{% else %}
app = FastAPI(){% endif %}

app.include_router(api, prefix='/api')
