import re
from dataclasses import dataclass

from zametka.notes.domain.common.value_objects.base import ValueObject
from zametka.notes.domain.exceptions.user import InvalidUserFirstNameError


@dataclass(frozen=True)
class UserFirstName(ValueObject[str]):
    value: str

    MAX_LENGTH = 40
    MIN_LENGTH = 2
    ALLOW_DIGITS = False

    def _validate(self) -> None:
        if len(self.value) > self.MAX_LENGTH:
            raise InvalidUserFirstNameError("Имя пользователя слишком длинное!")
        if len(self.value) < self.MIN_LENGTH:
            raise InvalidUserFirstNameError("Имя пользователя слишком короткое!")
        if not self.value:
            raise InvalidUserFirstNameError("Поле не может быть пустым!")
        if bool(re.search(r"\d", self.value)) and not self.ALLOW_DIGITS:
            raise InvalidUserFirstNameError("Имя пользователя не может содержать цифр!")
