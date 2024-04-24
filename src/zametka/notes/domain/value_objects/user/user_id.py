from __future__ import annotations

from typing import Any
from dataclasses import dataclass
from uuid import UUID

from zametka.notes.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class UserId(ValueObject[UUID]):
    value: UUID

    def __eq__(self, other: UserId | Any) -> bool:
        if not isinstance(other, UserId):
            raise ValueError(f"Expected UserIdentityId, got {type(other)}")
        return str(self.to_raw()) == str(other.to_raw())
