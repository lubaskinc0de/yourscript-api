from abc import abstractmethod
from typing import Protocol

from zametka.notes.domain.value_objects.user.user_id import UserId


class IdProvider(Protocol):
    @abstractmethod
    async def get_user_id(self) -> UserId:
        raise NotImplementedError
