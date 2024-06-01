from types import MappingProxyType
from typing import Final

from zametka.access_service.infrastructure.error_code import ErrorCode


class ErrorMessage:
    def __init__(self) -> None:
        self._msg: Final[MappingProxyType[ErrorCode, str]] = MappingProxyType(
            {
                ErrorCode.WEAK_PASSWORD: "Слабый пароль!",
                ErrorCode.INVALID_EMAIL: "Неккоректный адрес e-mail!",
                ErrorCode.INVALID_CREDENTIALS: "Неправильно введены данные для входа!",
                ErrorCode.USER_NOT_EXISTS: "Пользователя не существует.",
                ErrorCode.USER_NOT_ACTIVE: "Пользователь не активен. Сначала вы "
                "должны верифицировать свою почту.",
                ErrorCode.ACCESS_TOKEN_EXPIRED: "Токен истёк.",
                ErrorCode.UNAUTHORIZED: "Вы не авторизованы.",
                ErrorCode.CONFIRMATION_TOKEN_EXPIRED: "Токен истёк.",
                ErrorCode.CONFIRMATION_TOKEN_ALREADY_USED: "Токен уже использован.",
                ErrorCode.CORRUPTED_CONFIRMATION_TOKEN: "Токен повреждён.",
                ErrorCode.USER_EMAIL_ALREADY_EXISTS: "Такой пользователь уже "
                "существует",
            },
        )

    def get_error_message(self, error_code: ErrorCode) -> str:
        return self._msg[error_code]
