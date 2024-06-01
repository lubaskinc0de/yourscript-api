from uuid import UUID

from zametka.access_service.domain.common.value_objects.base import ValueObject


class TimedTokenId(ValueObject[UUID]):
    value: UUID
