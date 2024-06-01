from fastapi import Request
from fastapi.responses import JSONResponse

from zametka.notes.domain.exceptions.note import (
    NoteAccessDeniedError,
    NoteDataError,
    NoteNotExistsError,
)


async def note_access_denied_exception_handler(
    _request: Request, _exc: NoteAccessDeniedError,
) -> JSONResponse:
    return JSONResponse(
        status_code=403,
        content={"message": "Доступ закрыт."},
    )


async def note_not_exists_exception_handler(
    _request: Request, _exc: NoteNotExistsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"message": "Такой записи не существует."},
    )


async def note_data_exception_handler(
    _request: Request, exc: NoteDataError,
) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": exc.message})
