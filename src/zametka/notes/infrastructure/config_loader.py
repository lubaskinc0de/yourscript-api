import logging
import os
from dataclasses import dataclass


@dataclass
class BaseDB:
    """Base database config"""

    host: str
    db_name: str
    user: str
    password: str

    def get_connection_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.db_name}"


@dataclass
class DB(BaseDB):
    """App database config"""


@dataclass
class AlembicDB(BaseDB):
    """Alembic database config"""


@dataclass
class CORSSettings:
    """CORS Allowed Domains Settings"""

    frontend_url: str


@dataclass
class Settings:
    """App settings"""

    db: DB
    cors: CORSSettings


def load_settings() -> Settings:
    """Get app settings"""

    db = DB(
        db_name=os.environ["NOTES_POSTGRES_DB"],
        host=os.environ["DB_HOST"],
        password=os.environ["POSTGRES_PASSWORD"],
        user=os.environ["POSTGRES_USER"],
    )

    cors = CORSSettings(frontend_url=os.environ["FRONTEND"])

    logging.info("Notes config was loaded")

    return Settings(
        db=db,
        cors=cors,
    )


def load_alembic_settings() -> AlembicDB:
    """Get alembic settings"""

    return AlembicDB(
        db_name=os.environ["NOTES_POSTGRES_DB"],
        host=os.environ["DB_HOST"],
        password=os.environ["POSTGRES_PASSWORD"],
        user=os.environ["POSTGRES_USER"],
    )
