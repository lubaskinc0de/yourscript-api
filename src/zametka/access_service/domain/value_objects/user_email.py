from __future__ import annotations

from string import ascii_letters

from dataclasses import dataclass
from typing import Union

from zametka.access_service.domain.common.value_objects.base import ValueObject
from zametka.access_service.domain.exceptions.user_identity import InvalidUserEmailError


@dataclass(frozen=True)
class UserEmail(ValueObject[str]):
    value: str

    MAX_LENGTH = 100
    MIN_LENGTH = 6

    def _validate(self) -> None:
        if len(self.value) > self.MAX_LENGTH:
            raise InvalidUserEmailError("Слишком длинный e-email!")
        if len(self.value) < self.MIN_LENGTH:
            raise InvalidUserEmailError("Слишком короткий e-email!")

        invalid_email_exc = InvalidUserEmailError("Неправильный e-email!")

        if self.value.isspace():
            raise invalid_email_exc
        if self.value.isdigit():
            raise invalid_email_exc
        if "@" not in self.value:
            raise invalid_email_exc
        if "." not in self.value:
            raise invalid_email_exc
        if " " in self.value:
            raise invalid_email_exc
        if not set(ascii_letters).intersection(self.value):
            raise invalid_email_exc

        address = self.value.split("@")[0]

        if not set(ascii_letters).intersection(address):
            raise invalid_email_exc

        if {"@", "#", ".", "&", "*", "$", "%", "(", ")"}.intersection(address):
            raise invalid_email_exc

    def __eq__(self, other: Union[UserEmail, object]) -> bool:
        if not isinstance(other, UserEmail):
            return other == self.to_raw()
        return self.to_raw() == other.to_raw()
