from asyncpg import UniqueViolationError
from fastapi import Request, responses

from zametka.notes.domain.exceptions.user import (
    UserDataError,
    UserIsNotExistsError,
    IsNotAuthorizedError,
)


async def unique_exception_handler(
    _request: Request, _exc: UniqueViolationError
) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=422,
        content={"message": "Такая запись уже существует!"},
    )


async def user_data_exception_handler(
    _request: Request, exc: UserDataError
) -> responses.JSONResponse:
    return responses.JSONResponse(status_code=422, content={"detail": exc.message})


async def user_is_not_exists_exception_handler(
    _request: Request, _exc: UserIsNotExistsError
) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=401, content={"detail": "Пользователя не существует"}
    )


async def is_not_authorized_exception_handler(
    _request: Request, _exc: IsNotAuthorizedError
) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=401, content={"detail": "Вы не авторизованы"}
    )
