import logging
import uvicorn

from typing import Any

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_another_jwt_auth import AuthJWT

from zametka.access_service.presentation.web_api.config import (
    load_authjwt_config,
)

from zametka.access_service import presentation as access_presentation
from zametka.access_service.main import di as access_di

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
logger.propagate = False

app = FastAPI()

logging.info("App was created.")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.info("Initialized app middlewares.")

access_presentation.include_exception_handlers(app)
access_presentation.include_routers(app)

setup_dishka(access_di.setup_http_di(), app)


@AuthJWT.load_config  # type:ignore
def load_authjwt_module_config() -> list[tuple[str, Any]]:
    authjwt_config = load_authjwt_config()

    return [
        ("authjwt_secret_key", authjwt_config.authjwt_secret_key),
        ("authjwt_token_location", authjwt_config.authjwt_token_location),
        ("authjwt_access_token_expires", authjwt_config.authjwt_access_token_expires),
        ("authjwt_cookie_max_age", authjwt_config.authjwt_cookie_expires),
    ]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", reload=False, port=80)
