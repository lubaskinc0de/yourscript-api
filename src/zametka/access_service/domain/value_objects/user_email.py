from __future__ import annotations

from email_validator import EmailNotValidError, validate_email

from dataclasses import dataclass
from typing import Union

from zametka.access_service.domain.common.value_objects.base import ValueObject
from zametka.access_service.domain.exceptions.user import InvalidUserEmailError


@dataclass(frozen=True)
class UserEmail(ValueObject[str]):
    value: str

    MAX_LENGTH = 100
    MIN_LENGTH = 6

    def _validate(self) -> None:
        try:
            validate_email(self.value, check_deliverability=False)
        except EmailNotValidError as exc:
            raise InvalidUserEmailError from exc

    def __eq__(self, other: Union[UserEmail, object]) -> bool:
        if not isinstance(other, UserEmail):
            return other == self.to_raw()
        return self.to_raw() == other.to_raw()
