from dataclasses import dataclass
from typing import Union
from uuid import UUID

from zametka.access_service.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class UserId(ValueObject[UUID]):
    value: UUID

    def __eq__(self, other: Union["UserId", object]) -> bool:
        if not isinstance(other, UserId):
            return self.to_raw() == other
        return self.to_raw() == other.to_raw()
