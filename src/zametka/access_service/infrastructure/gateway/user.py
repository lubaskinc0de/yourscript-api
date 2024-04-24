from typing import Optional

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from zametka.access_service.application.dto import UserDTO
from zametka.access_service.application.common.repository import (
    UserGateway,
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


class UserGatewayImpl(UserGateway):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        user: User,
    ) -> UserDTO:
        db_user = convert_user_entity_to_db_user(user)

        self.session.add(db_user)

        await self.session.flush(objects=[db_user])

        return convert_db_user_to_dto(db_user)

    async def get(self, user_id: UserId) -> Optional[User]:
        q = select(DBUser).where(DBUser.user_id == user_id.to_raw())

        res = await self.session.execute(q)
        user: Optional[DBUser] = res.scalar()

        if not user:
            return None

        return convert_db_user_to_entity(user)

    async def get_by_email(self, email: UserEmail) -> Optional[User]:
        q = select(DBUser).where(DBUser.email == email.to_raw())

        res = await self.session.execute(q)

        user: Optional[DBUser] = res.scalar()

        if not user:
            return None

        return convert_db_user_to_entity(user)

    async def update(self, user_id: UserId, updated_user: User) -> None:
        q = (
            update(DBUser)
            .where(DBUser.user_id == user_id.to_raw())
            .values(is_active=updated_user.is_active)
        )

        await self.session.execute(q)

    async def delete(self, user_id: UserId) -> None:
        q = delete(DBUser).where(DBUser.user_id == user_id.to_raw())

        await self.session.execute(q)
