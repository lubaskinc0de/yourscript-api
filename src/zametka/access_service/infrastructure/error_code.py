from enum import Enum

from zametka.access_service.domain.exceptions.user import (
    WeakPasswordError,
    InvalidUserEmailError,
    InvalidCredentialsError,
    UserIsNotActiveError,
    UserIsNotExistsError,
)

from zametka.access_service.domain.exceptions.access_token import (
    AccessTokenIsExpiredError,
    UnauthorizedError,
)

from zametka.access_service.domain.exceptions.confirmation_token import (
    ConfirmationTokenIsExpiredError,
    ConfirmationTokenAlreadyUsedError,
    CorruptedConfirmationTokenError,
)


class ErrorCode(Enum):
    WEAK_PASSWORD = WeakPasswordError
    INVALID_EMAIL = InvalidUserEmailError
    INVALID_CREDENTIALS = InvalidCredentialsError
    USER_NOT_EXISTS = UserIsNotExistsError
    USER_NOT_ACTIVE = UserIsNotActiveError
    ACCESS_TOKEN_EXPIRED = AccessTokenIsExpiredError
    UNAUTHORIZED = UnauthorizedError
    CONFIRMATION_TOKEN_EXPIRED = ConfirmationTokenIsExpiredError
    CONFIRMATION_TOKEN_ALREADY_USED = ConfirmationTokenAlreadyUsedError
    CORRUPTED_CONFIRMATION_TOKEN = CorruptedConfirmationTokenError
