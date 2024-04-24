from zametka.access_service.domain.exceptions.base import DomainError


class ConfirmationTokenAlreadyUsedError(DomainError):
    pass


class ConfirmationTokenIsExpiredError(DomainError):
    pass


class CorruptedConfirmationTokenError(DomainError):
    pass
