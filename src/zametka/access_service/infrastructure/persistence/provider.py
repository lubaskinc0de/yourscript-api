import logging

from typing import AsyncIterable
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)

from zametka.access_service.infrastructure.persistence.config import DBConfig

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def get_engine(settings: DBConfig) -> AsyncGenerator[AsyncEngine, None]:
    """Get async SA engine"""

    engine = create_async_engine(
        settings.get_connection_url(),
        future=True,
    )

    logging.info("Engine was created.")

    yield engine

    await engine.dispose()

    logging.info("Engine was disposed.")


async def get_async_sessionmaker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """Get async SA sessionmaker"""

    session_factory = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    logging.info("Session provider was initialized")

    return session_factory


async def get_async_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterable[AsyncSession]:
    async with session_factory() as session:
        yield session
