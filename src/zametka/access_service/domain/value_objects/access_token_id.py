from uuid import UUID

from zametka.access_service.domain.common.value_objects.base import ValueObject


class AccessTokenId(ValueObject[UUID]):
    value: UUID
