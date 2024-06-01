from datetime import UTC, datetime

from zametka.access_service.domain.common.value_objects.base import ValueObject


class ExpiresIn(ValueObject[datetime]):
    value: datetime

    @property
    def is_expired(self) -> bool:
        now = datetime.now(tz=UTC)

        if now > self.value:
            return True

        return False
