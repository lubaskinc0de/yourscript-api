from zametka.access_service.domain.exceptions.base import DomainError


class UserIsNotExistsError(DomainError):
    ...


class IsNotAuthorizedError(DomainError):
    ...


class UserIsNotActiveError(DomainError):
    ...


class InvalidCredentialsError(DomainError):
    ...


class WeakPasswordError(DomainError):
    ...


class InvalidUserEmailError(DomainError):
    ...
