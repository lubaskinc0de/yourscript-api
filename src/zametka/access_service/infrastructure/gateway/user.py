from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from zametka.access_service.application.dto import UserDTO
from zametka.access_service.application.common.user_gateway import (
    UserReader,
    UserSaver,
)

from zametka.access_service.domain.entities.user import (
    User,
)
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_id import UserId

from zametka.access_service.infrastructure.persistence.models.user_identity import (
    DBUser,
)
from zametka.access_service.infrastructure.gateway.converters.user import (
    convert_db_user_to_dto,
    convert_db_user_to_entity,
    convert_user_entity_to_db_user,
)


class UserGatewayImpl(UserSaver, UserReader):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(
        self,
        user: User,
    ) -> UserDTO:
        db_user = convert_user_entity_to_db_user(user)

        await self.session.merge(db_user)
        await self.session.flush(objects=[db_user])

        return convert_db_user_to_dto(db_user)

    async def with_id(self, user_id: UserId) -> Optional[User]:
        q = select(DBUser).where(DBUser.user_id == user_id.to_raw())

        res = await self.session.execute(q)
        user: Optional[DBUser] = res.scalar()

        if not user:
            return None

        return convert_db_user_to_entity(user)

    async def with_email(self, email: UserEmail) -> Optional[User]:
        q = select(DBUser).where(DBUser.email == email.to_raw())

        res = await self.session.execute(q)

        user: Optional[DBUser] = res.scalar()

        if not user:
            return None

        return convert_db_user_to_entity(user)

    async def delete(self, user_id: UserId) -> None:
        q = delete(DBUser).where(DBUser.user_id == user_id.to_raw())

        await self.session.execute(q)
