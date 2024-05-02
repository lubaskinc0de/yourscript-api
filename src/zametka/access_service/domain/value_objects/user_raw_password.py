import re
from dataclasses import dataclass

from zametka.access_service.domain.common.value_objects.base import ValueObject
from zametka.access_service.domain.exceptions.user import WeakPasswordError


@dataclass(frozen=True)
class UserRawPassword(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        """Validate password"""

        special_symbols_regex = re.compile("[@_!#$%^&*()<>?/}{~:]")

        error_messages = {
            "Пароль должен содержать заглавную букву.": lambda s: any(
                x.isupper() for x in s
            ),
            "Пароль не должен состоять только из заглавных букв.": lambda s: any(
                x.islower() for x in s
            ),
            "Пароль должен содержать число.": lambda s: any(x.isdigit() for x in s),
            "Пароль не должен содержать пробелы.": lambda s: not any(
                x.isspace() for x in s
            ),
            "Пароль должен содержать в себе специальный символ (@, #, $, %)": lambda s: re.search(
                special_symbols_regex, s
            )
            is not None,
        }

        for message, password_validator in error_messages.items():
            if not password_validator(self.value):  # type:ignore
                raise WeakPasswordError(message)
