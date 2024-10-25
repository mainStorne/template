from ...dependencies.session import get_session
from ...db.models import {{cookiecutter.model_info.upper_name}}
from ...schemas.{{cookiecutter.model}} import {{cookiecutter.model_info.upper_name}}Create, {{cookiecutter.model_info.upper_name}}Update, {{cookiecutter.model_info.upper_name}}Read
from ..schemas.error import ErrorModel
from fastapi import Depends, Request, status, Response, APIRouter
from fastapi_sqlalchemy_toolkit import ModelManager
from sqlalchemy.ext.asyncio import AsyncSession


not_a_superuser_response = {
    status.HTTP_403_FORBIDDEN: {
        "description": "Not a superuser.",
    },
}

missing_token_or_inactive_user_response = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Missing token or inactive user.",
    },
}

auth_responses = {**not_a_superuser_response, **missing_token_or_inactive_user_response}

not_found_response = {
    status.HTTP_404_NOT_FOUND: {
        'model': ErrorModel,
    }
}


manager = ModelManager({{cookiecutter.model_info.upper_name}})

read_scheme = {{cookiecutter.model_info.upper_name}}Read
update_scheme = {{cookiecutter.model_info.upper_name}}Update
create_scheme = {{cookiecutter.model_info.upper_name}}Create


name = manager.model.__tablename__
get_current_active_user = authenticator.current_user(
    active=True
)

get_current_superuser = authenticator.current_user(
    active=True, superuser=True
)

r = APIRouter()

@r.get('/', response_model=list[read_scheme], name=f'{name}:all',
       dependencies=[Depends(get_current_active_user)],
       responses={**missing_token_or_inactive_user_response})
async def objs(request: Request, session: AsyncSession = Depends(get_session), ):
    return await manager.list(session)


@r.post("/", response_model=read_scheme, responses={
    **missing_token_or_inactive_user_response,
    status.HTTP_409_CONFLICT: {
        "model": ErrorModel,
    }
}, status_code=status.HTTP_201_CREATED, name=f"{name}:new one",
        dependencies=[Depends(get_current_active_user)],
        )
async def obj(request: Request, objs: create_scheme, session: AsyncSession = Depends(get_session)):
    return await manager.create(session, objs)


@r.patch("/{id}", response_model=read_scheme, responses={
    **auth_responses,
    **not_found_response,
}, name=f'{name}:patch one',
         dependencies=[Depends(get_current_superuser)])
async def obj(request: Request, id: int, scheme: update_scheme, session: AsyncSession = Depends(get_session)):
    model = await manager.get_or_404(session, id=id)
    return await manager.update(session, model, scheme)


@r.get("/{id}",
       dependencies=[Depends(get_current_active_user)],
       response_model=read_scheme,
       responses={
              **missing_token_or_inactive_user_response,
              **not_found_response
          },
       name=f'{name}:one',
       )
async def obj(request: Request, id: int, session: AsyncSession = Depends(get_session)):
    return await manager.get_or_404(session, id=id)


@r.delete("/{id}",
          dependencies=[Depends(get_current_superuser)],
          response_class=Response,
          responses={
                 **auth_responses,
                 **not_found_response
             }, status_code=status.HTTP_204_NO_CONTENT, name=f'{name}:delete one')
async def obj(request: Request, id: int, session: AsyncSession = Depends(get_session)):
    obj_in_db = await manager.get_or_404(session, id=id)
    await manager.delete(session, obj_in_db)
    return