
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from zametka.notes.application.common.repository import (
    UserRepository,
)
from zametka.notes.application.user.dto import UserDTO
from zametka.notes.domain.entities.user import User as UserEntity
from zametka.notes.domain.value_objects.user.user_id import UserId
from zametka.notes.infrastructure.db.models.user import User
from zametka.notes.infrastructure.repositories.converters.user import (
    user_db_model_to_user_dto,
    user_entity_to_db_model,
)


class UserRepositoryImpl(UserRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        user: UserEntity,
    ) -> UserDTO:
        db_user = user_entity_to_db_model(user)

        self.session.add(db_user)

        await self.session.flush(objects=[db_user])

        return user_db_model_to_user_dto(db_user)

    async def get(self, user_id: UserId) -> UserDTO | None:
        q = select(User).where(User.identity_id == user_id.to_raw())

        res = await self.session.execute(q)
        user: User | None = res.scalar()

        if not user:
            return None

        return user_db_model_to_user_dto(user)
