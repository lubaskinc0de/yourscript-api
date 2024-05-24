from dataclasses import dataclass

from zametka.access_service.domain.common.entities.timed_user_token import (
    TimedUserToken,
)
from zametka.access_service.domain.exceptions.access_token import (
    AccessTokenIsExpiredError,
)


class AccessToken(TimedUserToken):
    def verify(self) -> None:
        if self.expires_in.is_expired:
            raise AccessTokenIsExpiredError
        return None
