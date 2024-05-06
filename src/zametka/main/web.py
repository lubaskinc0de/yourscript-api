import logging

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from zametka.access_service import presentation as access_presentation
from zametka.access_service.bootstrap import di as access_di

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

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
