from abc import abstractmethod
from typing import Protocol

from zametka.access_service.domain.value_objects.user_hashed_password import (
    UserHashedPassword,
)
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)


class PasswordHasher(Protocol):
    @abstractmethod
    def hash_password(self, password: UserRawPassword) -> UserHashedPassword: ...

    @abstractmethod
    def verify_password(
        self,
        raw_password: UserRawPassword,
        hashed_password: UserHashedPassword,
    ) -> None: ...
