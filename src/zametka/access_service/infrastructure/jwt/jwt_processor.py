from abc import abstractmethod
from typing import Any, Protocol, TypeAlias

import jwt

from zametka.access_service.infrastructure.jwt.config import JWTConfig
from zametka.access_service.infrastructure.jwt.exceptions import (
    JWTDecodeError,
    JWTExpiredError,
)

JWTPayload: TypeAlias = dict[str, Any]
JWTToken: TypeAlias = str


class JWTProcessor(Protocol):
    @abstractmethod
    def encode(self, payload: JWTPayload) -> JWTToken: ...

    @abstractmethod
    def decode(self, token: JWTToken) -> JWTPayload: ...


class PyJWTProcessor(JWTProcessor):
    def __init__(self, config: JWTConfig) -> None:
        self.key = config.key
        self.algorithm = config.algorithm

    def encode(self, payload: JWTPayload) -> JWTToken:
        return jwt.encode(payload, self.key, self.algorithm)

    def decode(self, token: JWTToken) -> JWTPayload:
        try:
            return jwt.decode(token, self.key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError as exc:
            raise JWTExpiredError from exc
        except jwt.DecodeError as exc:
            raise JWTDecodeError from exc
