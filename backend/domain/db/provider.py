from fastapi import Depends

from sqlalchemy.orm import sessionmaker, Session

from adapters.repository.auth import AuthRepository
from adapters.repository.script import ScriptRepository

from adapters.repository.uow import UnitOfWork

from core.dependencies import SessionDependency


def get_uow(session: SessionDependency = Depends()):
    yield UnitOfWork(session=session)


def get_auth_repository(session: SessionDependency = Depends()):
    yield AuthRepository(session=session)


def get_script_repository(session: SessionDependency = Depends()):
    yield ScriptRepository(session=session)


class DbProvider:
    """Database session management"""

    def __init__(self, pool: sessionmaker):
        self.pool = pool

    async def get_session(self) -> Session:
        """Get session"""

        async with self.pool() as session:
            yield session
