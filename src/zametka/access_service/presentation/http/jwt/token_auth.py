from datetime import datetime, timezone
from uuid import UUID

from fastapi import Request

from zametka.access_service.domain.entities.access_token import AccessToken
from zametka.access_service.domain.entities.config import AccessTokenConfig
from zametka.access_service.domain.exceptions.access_token import UnauthorizedError
from zametka.access_service.domain.value_objects.user_id import UserId
from zametka.access_service.infrastructure.jwt.jwt_processor import (
    JWTProcessor,
    JWTPayload,
    JWTToken,
    JWTDecodeError,
)
from zametka.access_service.presentation.http.jwt.config import TokenAuthConfig


class TokenAuth:
    def __init__(
        self,
        req: Request,
        jwt_processor: JWTProcessor,
        config: TokenAuthConfig,
        access_token_config: AccessTokenConfig,
    ):
        self.req = req
        self.jwt_processor = jwt_processor
        self.config = config
        self.access_token_config = access_token_config

    def _decode_jwt(self, token: str) -> JWTPayload:
        try:
            return self.jwt_processor.decode(token)
        except JWTDecodeError:
            raise UnauthorizedError

    def get_access_token(self) -> AccessToken:
        cookies = self.req.cookies
        headers = self.req.headers
        token_key = self.config.token_key

        cookies_token = cookies.get(token_key)
        headers_token = headers.get(token_key)

        if not cookies_token or not headers_token or cookies_token != headers_token:
            raise UnauthorizedError

        jwt_payload = self._decode_jwt(cookies_token)
        subject = jwt_payload.get("sub")
        exp = jwt_payload.get("exp")

        if not subject:
            raise UnauthorizedError

        if not isinstance(subject, str) or not isinstance(exp, int):
            raise UnauthorizedError

        try:
            user_id = UserId(UUID(subject))
        except (ValueError, TypeError):
            raise UnauthorizedError

        expires_in = datetime.fromtimestamp(exp, timezone.utc)
        access_token = AccessToken.load(user_id, expires_in, self.access_token_config)

        return access_token

    def create_access_token(self, token: AccessToken) -> JWTToken:
        to_encode = {
            "sub": str(token.uid.to_raw()),
            "exp": token.expires_in,
        }

        return self.jwt_processor.encode(to_encode)
