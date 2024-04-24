from abc import abstractmethod
from typing import Protocol

from zametka.access_service.domain.entities.user import User
from zametka.access_service.domain.value_objects.user_id import UserId


class IdProvider(Protocol):
    @abstractmethod
    def get_user_id(self) -> UserId:
        raise NotImplementedError


class UserProvider(IdProvider):
    @abstractmethod
    async def get_user(self) -> User:
        raise NotImplementedError
