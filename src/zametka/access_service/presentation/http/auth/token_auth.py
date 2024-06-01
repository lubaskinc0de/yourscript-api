from uuid import UUID

from fastapi import Request, Response
from starlette.datastructures import Headers

from zametka.access_service.application.dto import AccessTokenDTO
from zametka.access_service.domain.common.entities.timed_user_token import (
    TimedTokenMetadata,
)
from zametka.access_service.domain.common.value_objects.timed_token_id import (
    TimedTokenId,
)
from zametka.access_service.domain.entities.access_token import AccessToken
from zametka.access_service.domain.exceptions.access_token import (
    UnauthorizedError,
)
from zametka.access_service.domain.value_objects.expires_in import ExpiresIn
from zametka.access_service.domain.value_objects.user_id import UserId
from zametka.access_service.infrastructure.auth.access_token_processor import (
    AccessTokenProcessor,
)
from zametka.access_service.infrastructure.jwt.exceptions import JWTDecodeError
from zametka.access_service.infrastructure.jwt.jwt_processor import JWTProcessor
from zametka.access_service.presentation.http.auth.config import TokenAuthConfig
from zametka.access_service.presentation.http.exceptions import (
    CSRFCorruptedError,
    CSRFExpiredError,
    CSRFMismatchError,
    CSRFMissingError,
)


class TokenAuth:
    def __init__(
        self,
        req: Request,
        token_processor: AccessTokenProcessor,
        csrf_processor: JWTProcessor,
        config: TokenAuthConfig,
    ):
        self.req = req
        self.token_processor = token_processor
        self.config = config
        self.csrf_processor = csrf_processor

    def _get_csrf_session(self, cookies: dict[str, str], headers: Headers) -> UUID:
        csrf_key = self.config.csrf_cookie_key
        csrf_cookie = cookies.get(csrf_key)
        csrf_header = headers.get(self.config.csrf_headers_key)

        if not csrf_cookie or not csrf_header:
            raise CSRFMissingError from UnauthorizedError

        if not csrf_cookie == csrf_header:  # double submit (see https://clck.ru/3AqsjZ)
            raise CSRFMismatchError from UnauthorizedError

        try:
            csrf_session_id = UUID(self.csrf_processor.decode(csrf_cookie)["sub"])
        except (KeyError, ValueError, JWTDecodeError) as exc:
            raise CSRFCorruptedError from exc

        return csrf_session_id

    def get_access_token(self) -> AccessToken:
        unsafe_http_methods = {"POST", "PUT", "DELETE"}

        cookies = self.req.cookies
        headers = self.req.headers
        token_key = self.config.token_cookie_key
        cookies_token = cookies.get(token_key)
        is_unsafe_request = self.req.method in unsafe_http_methods

        if not cookies_token:
            raise UnauthorizedError

        csrf_session_id = None
        if is_unsafe_request:
            csrf_session_id = self._get_csrf_session(cookies, headers)

        token = self.token_processor.decode(cookies_token)
        metadata = TimedTokenMetadata(
            uid=UserId(token.uid),
            expires_in=ExpiresIn(token.expires_in),
        )

        access_token = AccessToken(metadata, token_id=TimedTokenId(token.token_id))

        if csrf_session_id and csrf_session_id != access_token.token_id:
            raise CSRFExpiredError

        return access_token

    def set_session(self, token: AccessTokenDTO, response: Response) -> Response:
        jwt_token = self.token_processor.encode(token)
        csrf_token = self.csrf_processor.encode({"sub": token.uid})

        response.set_cookie(self.config.token_cookie_key, jwt_token, httponly=True)
        response.set_cookie(self.config.csrf_cookie_key, csrf_token, httponly=False)

        return response
