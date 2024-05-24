from dishka import AsyncContainer
from fastapi import Request
from fastapi.responses import JSONResponse

from zametka.access_service.domain.common.app_error import AppError
from zametka.access_service.infrastructure.error_code import ErrorCode
from zametka.access_service.presentation.error_message import ErrorMessage
from zametka.access_service.presentation.http.http_error_code import (
    HTTP_ERROR_CODE,
)


def get_http_error_response(err: AppError, error_message: ErrorMessage) -> JSONResponse:
    err_type = type(err)
    err_code = ErrorCode(err_type)
    err_message = error_message.get_error_message(err_code)
    err_http_code = HTTP_ERROR_CODE[ErrorCode(err_type)]

    return JSONResponse(
        status_code=err_http_code,
        content={
            "error_code": err_code.name,
            "message": err_message,
        },
    )


async def app_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, AppError):
        ...  # TODO: handle unknown exc
        return JSONResponse(status_code=500, content={})

    di_container: AsyncContainer = request.state.dishka_container
    error_message = await di_container.get(ErrorMessage)

    return get_http_error_response(exc, error_message)
