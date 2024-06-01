import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from zametka.notes.infrastructure.config_loader import DB


async def get_engine(settings: DB) -> AsyncGenerator[AsyncEngine, None]:
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
        engine, expire_on_commit=False, class_=AsyncSession,
    )

    logging.info("Session provider was initialized")

    return session_factory
