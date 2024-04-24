from adaptix.conversion import get_converter, link, coercer
from adaptix import P

from zametka.access_service.domain.entities.user import (
    User,
)

from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_hashed_password import (
    UserHashedPassword,
)
from zametka.access_service.domain.value_objects.user_id import UserId

from zametka.access_service.infrastructure.persistence.models.user_identity import (
    DBUser,
)
from zametka.access_service.application.dto import UserDTO

convert_db_user_to_entity = get_converter(DBUser, User, recipe=[
    link(P[DBUser].user_id, P[User].user_id, coercer=lambda x: UserId(x)),
    link(P[DBUser].email, P[User].email, coercer=lambda x: UserEmail(x)),
    link(P[DBUser].hashed_password, P[User].hashed_password, coercer=lambda x: UserHashedPassword(x)),
])

convert_db_user_to_dto = get_converter(DBUser, UserDTO)

convert_user_entity_to_db_user = get_converter(User, DBUser, recipe=[
    coercer(P[User]['.*'] & ~P[User].is_active, P[DBUser]['.*'] & ~P[DBUser].is_active,
            lambda x: x.to_raw())
])
