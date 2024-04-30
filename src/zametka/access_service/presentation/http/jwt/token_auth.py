from fastapi import Request, Response

from zametka.access_service.domain.entities.access_token import AccessToken
from zametka.access_service.domain.entities.config import AccessTokenConfig
from zametka.access_service.domain.exceptions.access_token import UnauthorizedError
from zametka.access_service.domain.value_objects.expires_in import ExpiresIn
from zametka.access_service.domain.value_objects.user_id import UserId
from zametka.access_service.infrastructure.jwt.access_token_processor import (
    AccessTokenProcessor,
)
from zametka.access_service.infrastructure.jwt.jwt_processor import JWTToken
from zametka.access_service.presentation.http.jwt.config import TokenAuthConfig


class TokenAuth:
    def __init__(
        self,
        req: Request,
        token_processor: AccessTokenProcessor,
        config: TokenAuthConfig,
        access_token_config: AccessTokenConfig,
    ):
        self.req = req
        self.token_processor = token_processor
        self.config = config
        self.access_token_config = access_token_config

    def get_access_token(self) -> AccessToken:
        cookies = self.req.cookies
        headers = self.req.headers
        token_key = self.config.token_key

        cookies_token = cookies.get(token_key)
        headers_token = headers.get(token_key)

        if not cookies_token or not headers_token or cookies_token != headers_token:
            raise UnauthorizedError

        token = self.token_processor.decode(cookies_token)
        access_token = AccessToken.load(
            UserId(token.uid), ExpiresIn(token.expires_in), self.access_token_config
        )

        return access_token

    def set_access_cookie(self, token: JWTToken, response: Response) -> Response:
        response.set_cookie(self.config.token_key, token)
        return response
