from zametka.access_service.domain.exceptions.base import DomainError


class UnauthorizedError(DomainError): ...


class AccessTokenIsExpiredError(UnauthorizedError): ...
