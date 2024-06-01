from enum import Enum

from zametka.access_service.application.common.exceptions.user import (
    UserEmailAlreadyExistsError,
    UserIsNotExistsError,
)
from zametka.access_service.domain.exceptions.access_token import (
    AccessTokenIsExpiredError,
    UnauthorizedError,
)
from zametka.access_service.domain.exceptions.confirmation_token import (
    ConfirmationTokenAlreadyUsedError,
    ConfirmationTokenIsExpiredError,
    CorruptedConfirmationTokenError,
)
from zametka.access_service.domain.exceptions.user import (
    InvalidCredentialsError,
    InvalidUserEmailError,
    UserIsNotActiveError,
    WeakPasswordError,
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
    USER_EMAIL_ALREADY_EXISTS = UserEmailAlreadyExistsError
