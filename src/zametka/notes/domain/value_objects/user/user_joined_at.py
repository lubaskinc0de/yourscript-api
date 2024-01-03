from dataclasses import dataclass
from datetime import datetime, date

from zametka.notes.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class UserJoinedAt(ValueObject[datetime]):
    value: datetime

    def read(self) -> date:
        return self.value.date()
