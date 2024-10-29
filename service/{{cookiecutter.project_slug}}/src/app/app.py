from fastapi import FastAPI
from .api.api import api
{% if cookiecutter.is_debug %}
from contextlib import asynccontextmanager
from .conf import engine
from .storage.db.setup import create_db_and_tables

@asynccontextmanager
async def lifespan(app):
    await create_db_and_tables(engine)
    yield

app = FastAPI(lifespan=lifespan)
{% else %}
from contextlib import asynccontextmanager
from .dependencies.redis import get_redis
from .dependencies.session import get_session
from .storage.db_cache_adapter import DbCacheAdapter
from .schemas.users import UserRead
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await create_db_and_tables(engine)
    adapter = DbCacheAdapter(get_redis, get_session, UserRead)
    worker = asyncio.create_task(adapter.listen_for_services_events())
    app.state.worker = worker
    yield
    worker.cancel()

app = FastAPI(root_path="{{cookiecutter.fastapi_root_path}}", lifespan=lifespan){% endif %}

app.include_router(api)
