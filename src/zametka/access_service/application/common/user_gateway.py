from abc import abstractmethod
from typing import Protocol

from zametka.access_service.application.dto import UserDTO
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_id import UserId


class UserReader(Protocol):
    @abstractmethod
    async def with_id(self, user_id: UserId) -> User | None: ...

    @abstractmethod
    async def with_email(self, email: UserEmail) -> User | None: ...


class UserSaver(Protocol):
    @abstractmethod
    async def save(self, user: User) -> UserDTO: ...

    @abstractmethod
    async def delete(self, user_id: UserId) -> None: ...
