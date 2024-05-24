from dataclasses import dataclass

from zametka.access_service.domain.common.entities.timed_user_token import (
    TimedUserToken,
)
from zametka.access_service.domain.exceptions.confirmation_token import (
    ConfirmationTokenIsExpiredError,
)


class UserConfirmationToken(TimedUserToken):
    def verify(self) -> None:
        if self.expires_in.is_expired:
            raise ConfirmationTokenIsExpiredError
        return None
