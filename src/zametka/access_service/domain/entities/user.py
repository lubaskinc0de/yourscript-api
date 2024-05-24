from dataclasses import dataclass
from typing import Union

from zametka.access_service.domain.entities.confirmation_token import (
    UserConfirmationToken,
)
from zametka.access_service.domain.exceptions.confirmation_token import (
    ConfirmationTokenAlreadyUsedError,
    CorruptedConfirmationTokenError,
)
from zametka.access_service.domain.exceptions.password_hasher import (
    PasswordMismatchError,
)
from zametka.access_service.domain.exceptions.user import (
    UserIsNotActiveError,
    InvalidCredentialsError,
)
from zametka.access_service.domain.common.services.password_hasher import PasswordHasher
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_hashed_password import (
    UserHashedPassword,
)
from zametka.access_service.domain.value_objects.user_id import UserId
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)


@dataclass
class User:
    user_id: UserId
    email: UserEmail
    hashed_password: UserHashedPassword
    is_active: bool = False

    @classmethod
    def create_with_raw_password(
        cls,
        user_id: UserId,
        email: UserEmail,
        raw_password: UserRawPassword,
        password_hasher: PasswordHasher,
    ) -> "User":
        hashed_password = password_hasher.hash_password(raw_password)
        return cls(user_id, email, hashed_password)

    def ensure_is_active(self) -> None:
        if not self.is_active:
            raise UserIsNotActiveError

    def authenticate(
        self, raw_password: UserRawPassword, password_hasher: PasswordHasher
    ) -> None:
        try:
            password_hasher.verify_password(raw_password, self.hashed_password)
        except PasswordMismatchError as exc:
            raise InvalidCredentialsError from exc

    def _activate(self) -> None:
        self.is_active = True

    def activate(self, token: UserConfirmationToken) -> None:
        token.verify()

        if self.is_active:
            raise ConfirmationTokenAlreadyUsedError
        if token.uid != self.user_id:
            raise CorruptedConfirmationTokenError

        self._activate()

    def __hash__(self) -> int:
        return hash(self.user_id)

    def __eq__(self, other: Union[object, "User"]) -> bool:
        if not isinstance(other, User):
            return False

        return self.user_id == other.user_id

    def __repr__(self) -> str:
        return "{} object(id={}, is_active={})".format(
            self.__class__.__qualname__, self.user_id, bool(self)
        )

    def __str__(self) -> str:
        return "{} <{}>".format(self.__class__.__qualname__, self.user_id)
