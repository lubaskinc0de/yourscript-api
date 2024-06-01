from datetime import UTC, datetime
from uuid import UUID

from zametka.access_service.application.dto import AccessTokenDTO
from zametka.access_service.domain.exceptions.access_token import (
    AccessTokenIsExpiredError,
    UnauthorizedError,
)
from zametka.access_service.infrastructure.jwt.exceptions import (
    JWTDecodeError,
    JWTExpiredError,
)
from zametka.access_service.infrastructure.jwt.jwt_processor import (
    JWTProcessor,
    JWTToken,
)


class AccessTokenProcessor:
    def __init__(self, jwt_processor: JWTProcessor):
        self.jwt_processor = jwt_processor

    def encode(self, token: AccessTokenDTO) -> JWTToken:
        jwt_token_payload = {
            "sub": {
                "uid": str(token.uid),
                "token_id": str(token.token_id),
            },
            "exp": token.expires_in,
        }
        jwt_token = self.jwt_processor.encode(jwt_token_payload)

        return jwt_token

    def decode(self, token: JWTToken) -> AccessTokenDTO:
        try:
            payload = self.jwt_processor.decode(token)
            sub = payload["sub"]

            uid = UUID(sub["uid"])
            token_id = UUID(sub["token_id"])
            expires_in = datetime.fromtimestamp(float(payload["exp"]), UTC)
            access_token = AccessTokenDTO(
                uid=uid,
                expires_in=expires_in,
                token_id=token_id,
            )
        except JWTExpiredError as exc:
            raise AccessTokenIsExpiredError from exc
        except (JWTDecodeError, ValueError, TypeError, KeyError) as exc:
            raise UnauthorizedError from exc
        else:
            return access_token
