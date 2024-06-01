from dataclasses import dataclass

from zametka.access_service.domain.common.base_error import BaseError


@dataclass(frozen=True)
class HTTPError(BaseError):
    http_code: int


@dataclass(frozen=True)
class CSRFError(HTTPError):
    http_code: int = 401


class CSRFMismatchError(CSRFError): ...


class CSRFCorruptedError(CSRFError): ...


class CSRFMissingError(CSRFError): ...


class CSRFExpiredError(CSRFError): ...
