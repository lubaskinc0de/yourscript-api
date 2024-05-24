import logging

from fastapi import FastAPI
from asyncpg import UniqueViolationError

from zametka.notes.domain.exceptions.note import (
    NoteAccessDeniedError,
    NoteNotExistsError,
    NoteDataError,
)
from zametka.notes.domain.exceptions.user import (
    UserDataError,
    IsNotAuthorizedError,
    UserIsNotExistsError,
)

from zametka.notes.presentation.web_api.endpoints import note, user

from zametka.notes.presentation.web_api.exception_handlers.note import (
    note_access_denied_exception_handler,
    note_not_exists_exception_handler,
    note_data_exception_handler,
)

from zametka.notes.presentation.web_api.exception_handlers.user import (
    user_data_exception_handler,
    is_not_authorized_exception_handler,
    user_is_not_exists_exception_handler,
    unique_exception_handler,
)


def include_routers(app: FastAPI) -> None:
    """Include endpoints APIRouters to the bootstrap app"""

    logging.info("Routers was included.")

    app.include_router(note.router)
    app.include_router(user.router)


def include_exception_handlers(app: FastAPI) -> None:
    """Include exceptions handlers to the bootstrap app"""

    logging.info("Exception handlers was included.")

    app.add_exception_handler(
        NoteAccessDeniedError, note_access_denied_exception_handler
    )
    app.add_exception_handler(NoteNotExistsError, note_not_exists_exception_handler)
    app.add_exception_handler(NoteDataError, note_data_exception_handler)
    app.add_exception_handler(UserDataError, user_data_exception_handler)
    app.add_exception_handler(
        UserIsNotExistsError, user_is_not_exists_exception_handler
    )
    app.add_exception_handler(IsNotAuthorizedError, is_not_authorized_exception_handler)
    app.add_exception_handler(UniqueViolationError, unique_exception_handler)
