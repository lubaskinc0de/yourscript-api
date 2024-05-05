from datetime import timezone, datetime
from uuid import UUID

from zametka.access_service.application.dto import UserConfirmationTokenDTO
from zametka.access_service.domain.exceptions.confirmation_token import (
    CorruptedConfirmationTokenError,
)

from zametka.access_service.infrastructure.jwt.jwt_processor import (
    JWTToken,
    JWTProcessor,
    JWTDecodeError,
)


class ConfirmationTokenProcessor:
    def __init__(self, jwt_processor: JWTProcessor):
        self.jwt_processor = jwt_processor

    def encode(self, token: UserConfirmationTokenDTO) -> JWTToken:
        jwt_token_payload = {
            "sub": str(token.uid),
            "exp": token.expires_in,
        }
        jwt_token = self.jwt_processor.encode(jwt_token_payload)

        return jwt_token

    def decode(self, token: JWTToken) -> UserConfirmationTokenDTO:
        try:
            payload = self.jwt_processor.decode(token)
            uid = UUID(payload["sub"])
            expires_in = datetime.fromtimestamp(
                float(payload["exp"]), timezone.utc
            )

            confirmation_token = UserConfirmationTokenDTO(
                uid=uid, expires_in=expires_in
            )
            return confirmation_token
        except (JWTDecodeError, ValueError, TypeError, KeyError) as exc:
            raise CorruptedConfirmationTokenError from exc
