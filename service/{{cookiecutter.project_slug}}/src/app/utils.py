from pydantic import BaseModel, ValidationError
from fastapi import HTTPException, status
from httpx import Response


def validate(model: type[BaseModel], response: Response):
    if response.status_code > 400:
        raise HTTPException(status_code=response.status_code, detail=response.content)

    try:
        return model.model_validate_json(response.content)
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

