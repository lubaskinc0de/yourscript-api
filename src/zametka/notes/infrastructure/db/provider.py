from sqlalchemy.ext.asyncio import AsyncSession

from zametka.notes.infrastructure.db.uow import SAUnitOfWork
from zametka.notes.infrastructure.repositories.note import NoteRepositoryImpl
from zametka.notes.infrastructure.repositories.user import UserRepositoryImpl


def get_uow(session: AsyncSession) -> SAUnitOfWork:
    return SAUnitOfWork(session=session)


def get_note_repository(session: AsyncSession) -> NoteRepositoryImpl:
    return NoteRepositoryImpl(session=session)


def get_user_repository(session: AsyncSession) -> UserRepositoryImpl:
    return UserRepositoryImpl(session=session)
