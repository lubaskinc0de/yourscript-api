import os
from dataclasses import dataclass


@dataclass
class BaseDBConfig:
    """Base database config"""

    host: str
    db_name: str
    user: str
    password: str

    def get_connection_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.db_name}"


@dataclass
class DBConfig(BaseDBConfig):
    """App database config"""


@dataclass
class AlembicDBConfig(BaseDBConfig):
    """Alembic database config"""


def load_alembic_config() -> AlembicDBConfig:
    return AlembicDBConfig(
        db_name=os.environ["ACCESS_POSTGRES_DB"],
        host=os.environ["DB_HOST"],
        password=os.environ["POSTGRES_PASSWORD"],
        user=os.environ["POSTGRES_USER"],
    )
