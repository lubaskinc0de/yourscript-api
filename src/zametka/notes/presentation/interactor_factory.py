from abc import ABC, abstractmethod

from typing import AsyncContextManager, Awaitable, Callable, TypeAlias, TypeVar

from zametka.notes.application.common.id_provider import IdProvider
from zametka.notes.application.note.note_interactor import NoteInteractor
from zametka.notes.application.user.create_user import CreateUser
from zametka.notes.application.user.get_user import GetUser

# G means generic
GInputDTO = TypeVar("GInputDTO")
GOutputDTO = TypeVar("GOutputDTO")

InteractorCallable: TypeAlias = Callable[[GInputDTO], Awaitable[GOutputDTO]]
InteractorPicker: TypeAlias = Callable[
    [NoteInteractor], InteractorCallable[GInputDTO, GOutputDTO]
]


class InteractorFactory(ABC):
    @abstractmethod
    def pick_note_interactor(
        self,
        id_provider: IdProvider,
        picker: InteractorPicker[GInputDTO, GOutputDTO],
    ) -> AsyncContextManager[InteractorCallable[GInputDTO, GOutputDTO]]:
        raise NotImplementedError

    @abstractmethod
    def create_user(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[CreateUser]:
        raise NotImplementedError

    @abstractmethod
    def get_user(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[GetUser]:
        raise NotImplementedError
