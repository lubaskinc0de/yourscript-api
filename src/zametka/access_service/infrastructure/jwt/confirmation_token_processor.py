import logging
from datetime import timezone, datetime
from uuid import UUID

from zametka.access_service.domain.entities.confirmation_token import (
    UserConfirmationToken,
)
from zametka.access_service.domain.exceptions.confirmation_token import (
    CorruptedConfirmationTokenError,
)
from zametka.access_service.domain.value_objects.user_id import UserId
from zametka.access_service.infrastructure.jwt.jwt_processor import (
    JWTToken,
    JWTProcessor,
    JWTDecodeError,
)


class ConfirmationTokenProcessor:
    def __init__(self, jwt_processor: JWTProcessor):
        self.jwt_processor = jwt_processor

    def encode(self, token: UserConfirmationToken) -> JWTToken:
        jwt_token_payload = {
            "sub": {
                "uid": str(token.uid.to_raw()),
                "timestamp": token.timestamp.timestamp()
            },
        }
        jwt_token = self.jwt_processor.encode(jwt_token_payload)

        return jwt_token

    def decode(self, token: JWTToken) -> UserConfirmationToken:
        try:
            payload = self.jwt_processor.decode(token)["sub"]
            uid = UserId(UUID(payload["uid"]))
            timestamp = datetime.fromtimestamp(
                float(payload["timestamp"]), timezone.utc
            )

            token = UserConfirmationToken.load(uid, timestamp)
            return token
        except (JWTDecodeError, ValueError, TypeError, KeyError) as exc:
            logging.exception(exc)
            raise CorruptedConfirmationTokenError from exc
