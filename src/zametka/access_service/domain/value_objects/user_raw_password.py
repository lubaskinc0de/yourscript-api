import re

from zametka.access_service.domain.common.value_objects.base import ValueObject
from zametka.access_service.domain.exceptions.user import WeakPasswordError


def has_special_symbols(string: str) -> bool:
    regex = re.compile("[@_!#$%^&*()<>?/}{~:]")

    if re.search(regex, string) is None:
        return False

    return True


class UserRawPassword(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        """Validate password"""

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
            "Пароль должен содержать в себе специальный \
            символ (@, #, $, %)": has_special_symbols,
        }

        for message, password_validator in error_messages.items():
            if not password_validator(self.value):
                raise WeakPasswordError(message)
