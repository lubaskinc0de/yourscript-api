import logging

from fastapi import FastAPI

from zametka.access_service.presentation.http.exception_handlers import (
    app_exception_handler,
)

from ..domain.common.base_error import BaseError
from .http.endpoints import user


def include_routers(app: FastAPI) -> None:
    app.include_router(user.router)
    logging.info("Routers was included.")


def include_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(BaseError, app_exception_handler)
    logging.info("Exception handlers was included.")


__all__ = [
    "include_exception_handlers",
    "include_routers",
]
