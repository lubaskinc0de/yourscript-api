from datetime import UTC, datetime
from uuid import UUID

from zametka.access_service.application.dto import UserConfirmationTokenDTO
from zametka.access_service.domain.exceptions.confirmation_token import (
    ConfirmationTokenIsExpiredError,
    CorruptedConfirmationTokenError,
)
from zametka.access_service.infrastructure.jwt.exceptions import (
    JWTDecodeError,
    JWTExpiredError,
)
from zametka.access_service.infrastructure.jwt.jwt_processor import (
    JWTProcessor,
    JWTToken,
)


class ConfirmationTokenProcessor:
    def __init__(self, jwt_processor: JWTProcessor):
        self.jwt_processor = jwt_processor

    def encode(self, token: UserConfirmationTokenDTO) -> JWTToken:
        jwt_token_payload = {
            "sub": {
                "uid": str(token.uid),
                "token_id": str(token.token_id),
            },
            "exp": token.expires_in,
        }
        jwt_token = self.jwt_processor.encode(jwt_token_payload)

        return jwt_token

    def decode(self, token: JWTToken) -> UserConfirmationTokenDTO:
        try:
            payload = self.jwt_processor.decode(token)
            sub = payload["sub"]

            uid = UUID(sub["uid"])
            token_id = UUID(sub["token_id"])
            expires_in = datetime.fromtimestamp(float(payload["exp"]), UTC)

            confirmation_token = UserConfirmationTokenDTO(
                uid=uid,
                expires_in=expires_in,
                token_id=token_id,
            )
        except JWTExpiredError as exc:
            raise ConfirmationTokenIsExpiredError from exc
        except (JWTDecodeError, ValueError, TypeError, KeyError) as exc:
            raise CorruptedConfirmationTokenError from exc
        else:
            return confirmation_token
