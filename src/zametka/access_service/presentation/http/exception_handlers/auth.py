import jwt

from asyncpg import UniqueViolationError
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi_another_jwt_auth.exceptions import AuthJWTException
from jwt.exceptions import ExpiredSignatureError

from zametka.access_service.domain.exceptions.confirmation_token import (
    CorruptedConfirmationTokenError,
    ConfirmationTokenAlreadyUsedError,
)
from zametka.access_service.domain.exceptions.user import (
    InvalidCredentialsError,
    UserIsNotActiveError,
    UserIsNotExistsError,
    WeakPasswordError,
    IsNotAuthorizedError,
)


async def unique_exception_handler(
    _request: Request, _exc: UniqueViolationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"message": "Такая запись уже существует!"},
    )


async def weak_password_exception_handler(
    _request: Request, exc: WeakPasswordError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"message": f"Слабый пароль! {exc.message}"},
    )


async def user_not_active_exception_handler(
    _request: Request, _exc: UserIsNotActiveError
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={
            "message": "Пользователь не активен. Сначала вы должны верифицировать свою почту."
        },
    )


async def user_not_exists_exception_handler(
    _request: Request, _exc: UserIsNotExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"message": "Пользователя не существует."},
    )


async def is_not_authorized_exception_handler(
    _request: Request, _exc: IsNotAuthorizedError
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={},
    )


async def invalid_credentials_exception_handler(
    _request: Request, _exc: InvalidCredentialsError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"message": "Неправильно введены данные для входа!"},
    )


async def expired_token_exception_handler(
    _request: Request, _exc: ExpiredSignatureError
) -> JSONResponse:
    return JSONResponse(
        status_code=408,
        content={"message": "Токен истёк."},
    )


async def corrupted_token_exception_handler(
    _request: Request, _exc: CorruptedConfirmationTokenError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"message": "Токен повреждён."},
    )


async def invalid_encoded_token_exception_handler(
    _request: Request, _exc: jwt.exceptions.DecodeError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"message": "Токен повреждён."},
    )


async def token_already_used_exception_handler(
    _request: Request, _exc: ConfirmationTokenAlreadyUsedError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"message": "Токен уже использован."},
    )


async def authjwt_exception_handler(
    _request: Request, exc: AuthJWTException
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"detail": exc.message},
    )
