from dataclasses import dataclass
from typing import Union

from passlib.handlers.pbkdf2 import pbkdf2_sha256

from zametka.access_service.domain.entities.access_token import AccessToken
from zametka.access_service.domain.entities.confirmation_token import (
    UserConfirmationToken,
)
from zametka.access_service.domain.exceptions.access_token import UnauthorizedError
from zametka.access_service.domain.exceptions.confirmation_token import (
    ConfirmationTokenAlreadyUsedError,
    CorruptedConfirmationTokenError,
)
from zametka.access_service.domain.exceptions.user_identity import (
    UserIsNotActiveError,
    InvalidCredentialsError,
)
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
    ) -> "User":
        hashed_password = UserHashedPassword(pbkdf2_sha256.hash(raw_password.to_raw()))
        return cls(user_id, email, hashed_password)

    def ensure_can_authorize(self) -> None:
        if not self.is_active:
            raise UserIsNotActiveError from UnauthorizedError

    def ensure_authorized(self, access_token: AccessToken) -> None:
        self.ensure_can_authorize()
        access_token.verify()

        if not access_token.uid == self.user_id:
            raise UnauthorizedError

    def ensure_authenticated(self, raw_password: UserRawPassword) -> None:
        passwords_match = pbkdf2_sha256.verify(
            raw_password.to_raw(), self.hashed_password.to_raw()
        )

        if not passwords_match:
            raise InvalidCredentialsError

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
