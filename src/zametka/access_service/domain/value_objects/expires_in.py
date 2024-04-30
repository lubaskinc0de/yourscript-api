from dataclasses import dataclass
from datetime import datetime, timezone

from zametka.access_service.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class ExpiresIn(ValueObject[datetime]):
    value: datetime

    @property
    def is_expired(self) -> bool:
        now = datetime.now(tz=timezone.utc)

        if now > self.value:
            return True

        return False
