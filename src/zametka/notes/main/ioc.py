from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from zametka.notes.application.common.id_provider import IdProvider
from zametka.notes.application.note.note_interactor import NoteInteractor
from zametka.notes.application.user.create_user import CreateUser
from zametka.notes.application.user.get_user import GetUser
from zametka.notes.domain.services.note_service import NoteService
from zametka.notes.domain.services.user_service import UserService
from zametka.notes.infrastructure.db.provider import (
    get_note_repository,
    get_uow,
    get_user_repository,
)
from zametka.notes.presentation.interactor_factory import (
    GInputDTO,
    GOutputDTO,
    InteractorCallable,
    InteractorFactory,
    InteractorPicker,
)


class IoC(InteractorFactory):
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ):
        self._session_factory = session_factory
        self._note_service = NoteService()
        self._user_service = UserService()

    def _construct_note_interactor(
        self, session: AsyncSession, id_provider: IdProvider
    ) -> NoteInteractor:
        note_repository = get_note_repository(session)
        uow = get_uow(session)

        note_service = self._note_service

        return NoteInteractor(
            note_repository=note_repository,
            uow=uow,
            note_service=note_service,
            id_provider=id_provider,
        )

    @asynccontextmanager
    async def pick_note_interactor(
        self,
        id_provider: IdProvider,
        picker: InteractorPicker[GInputDTO, GOutputDTO],
    ) -> AsyncIterator[InteractorCallable[GInputDTO, GOutputDTO]]:
        async with self._session_factory() as session:
            interactor = self._construct_note_interactor(session, id_provider)
            yield picker(interactor)

    @asynccontextmanager
    async def create_user(self, id_provider: IdProvider) -> AsyncIterator[CreateUser]:
        async with self._session_factory() as session:
            interactor = CreateUser(
                user_repository=get_user_repository(session),
                uow=get_uow(session),
                id_provider=id_provider,
                user_service=self._user_service,
            )

            yield interactor

    @asynccontextmanager
    async def get_user(self, id_provider: IdProvider) -> AsyncIterator[GetUser]:
        async with self._session_factory() as session:
            interactor = GetUser(
                user_repository=get_user_repository(session),
                id_provider=id_provider,
            )

            yield interactor
