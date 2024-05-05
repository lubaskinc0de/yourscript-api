import jwt

from typing import Protocol, TypeAlias, Any
from abc import abstractmethod

from zametka.access_service.infrastructure.jwt.config import JWTConfig

JWTPayload: TypeAlias = dict[str, Any]
JWTToken: TypeAlias = str


class JWTDecodeError(Exception): ...


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
            return jwt.decode(token, self.key, algorithms=[self.algorithm])  # type:ignore
        except jwt.DecodeError as exc:
            raise JWTDecodeError from exc
