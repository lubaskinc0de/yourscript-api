import argon2

from zametka.access_service.domain.exceptions.password_hasher import (
    PasswordMismatchError,
)
from zametka.access_service.domain.common.services.password_hasher import PasswordHasher
from zametka.access_service.domain.value_objects.user_hashed_password import (
    UserHashedPassword,
)
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)


class ArgonPasswordHasher(PasswordHasher):
    def __init__(self, password_hasher: argon2.PasswordHasher) -> None:
        self.ph = password_hasher

    def hash_password(self, password: UserRawPassword) -> UserHashedPassword:
        return UserHashedPassword(self.ph.hash(password.value))

    def verify_password(
        self,
        raw_password: UserRawPassword,
        hashed_password: UserHashedPassword,
    ) -> None:
        try:
            self.ph.verify(hashed_password.value, raw_password.value)
        except argon2.exceptions.VerifyMismatchError as exc:
            raise PasswordMismatchError from exc
