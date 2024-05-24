from dataclasses import dataclass
from uuid import UUID

from zametka.access_service.domain.common.value_objects.base import ValueObject


class UserId(ValueObject[UUID]):
    value: UUID
