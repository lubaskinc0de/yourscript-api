from zametka.access_service.domain.exceptions.base import DomainError


class ConfirmationTokenAlreadyUsedError(DomainError):
    ...


class ConfirmationTokenIsExpiredError(DomainError):
    ...


class CorruptedConfirmationTokenError(DomainError):
    ...
