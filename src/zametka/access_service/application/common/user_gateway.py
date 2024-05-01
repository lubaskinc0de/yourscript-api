from abc import abstractmethod
from typing import Optional, Protocol

from zametka.access_service.application.dto import UserDTO
from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_id import UserId


class UserReader(Protocol):
    @abstractmethod
    async def get(self, user_id: UserId) -> Optional[User]:
        ...

    @abstractmethod
    async def get_by_email(self, email: UserEmail) -> Optional[User]:
        ...


class UserSaver(Protocol):
    @abstractmethod
    async def save(self, user: User) -> UserDTO:
        ...

    @abstractmethod
    async def delete(self, user_id: UserId) -> None:
        ...
