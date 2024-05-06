import re

from dataclasses import dataclass

from zametka.notes.domain.common.value_objects.base import ValueObject
from zametka.notes.domain.exceptions.user import InvalidUserLastNameError


@dataclass(frozen=True)
class UserLastName(ValueObject[str]):
    value: str

    MAX_LENGTH = 60
    MIN_LENGTH = 2

    def _validate(self) -> None:
        if len(self.value) > self.MAX_LENGTH:
            raise InvalidUserLastNameError(
                "Фамилия пользователя слишком длинная!"
            )
        if len(self.value) < self.MIN_LENGTH:
            raise InvalidUserLastNameError(
                "Фамилия пользователя слишком короткая!"
            )
        if not self.value:
            raise InvalidUserLastNameError("Поле не может быть пустым!")
        if bool(re.search(r"\d", self.value)):
            raise InvalidUserLastNameError(
                "Фамилия пользователя не может содержать цифр!"
            )
