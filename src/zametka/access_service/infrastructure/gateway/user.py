from typing import NoReturn

from sqlalchemy import delete, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from zametka.access_service.application.common.exceptions.repo_error import RepoError
from zametka.access_service.application.common.exceptions.user import (
    UserEmailAlreadyExistsError,
)
from zametka.access_service.application.common.user_gateway import (
    UserReader,
    UserSaver,
)
from zametka.access_service.application.dto import UserDTO
from zametka.access_service.domain.entities.user import (
    User,
)
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_id import UserId
from zametka.access_service.infrastructure.gateway.converters.user import (
    convert_db_user_to_dto,
    convert_db_user_to_entity,
    convert_user_entity_to_db_user,
)
from zametka.access_service.infrastructure.persistence.models.user_identity import (
    DBUser,
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

        try:
            await self.session.merge(db_user)
        except IntegrityError as err:
            self._process_error(err)

        return convert_db_user_to_dto(db_user)

    async def with_id(self, user_id: UserId) -> User | None:
        q = select(DBUser).where(DBUser.user_id == user_id.to_raw())

        res = await self.session.execute(q)
        user: DBUser | None = res.scalar()

        if not user:
            return None

        return convert_db_user_to_entity(user)

    async def with_email(self, email: UserEmail) -> User | None:
        q = select(DBUser).where(DBUser.email == email.to_raw())

        res = await self.session.execute(q)

        user: DBUser | None = res.scalar()

        if not user:
            return None

        return convert_db_user_to_entity(user)

    async def delete(self, user_id: UserId) -> None:
        q = delete(DBUser).where(DBUser.user_id == user_id.to_raw())

        await self.session.execute(q)

    @staticmethod
    def _process_error(error: DBAPIError) -> NoReturn:
        match error.__cause__.__cause__.constraint_name:
            case "uq_users_email":
                raise UserEmailAlreadyExistsError from error
            case _:
                raise RepoError from error
