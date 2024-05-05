from typing import Final
from types import MappingProxyType

from zametka.access_service.infrastructure.error_code import ErrorCode

HTTP_ERROR_CODE: Final[MappingProxyType[ErrorCode, int]] = MappingProxyType(
    {
        ErrorCode.WEAK_PASSWORD: 400,
        ErrorCode.INVALID_EMAIL: 400,
        ErrorCode.INVALID_CREDENTIALS: 403,
        ErrorCode.USER_NOT_EXISTS: 404,
        ErrorCode.USER_NOT_ACTIVE: 403,
        ErrorCode.ACCESS_TOKEN_EXPIRED: 401,
        ErrorCode.UNAUTHORIZED: 401,
        ErrorCode.CONFIRMATION_TOKEN_EXPIRED: 408,
        ErrorCode.CONFIRMATION_TOKEN_ALREADY_USED: 409,
        ErrorCode.CORRUPTED_CONFIRMATION_TOKEN: 400,
    }
)
