from zametka.notes.application.user.dto import UserDTO
from zametka.notes.domain.entities.user import User as UserEntity
from zametka.notes.infrastructure.db.models.user import User


def user_db_model_to_user_dto(user: User) -> UserDTO:
    return UserDTO(
        first_name=user.first_name,
        last_name=user.last_name,
        joined_at=user.joined_at,
    )


def user_entity_to_db_model(user: UserEntity) -> User:
    db_user = User(
        first_name=user.first_name.to_raw(),
        last_name=user.last_name.to_raw(),
        joined_at=user.joined_at.to_raw(),
        identity_id=user.identity_id.to_raw(),
    )

    return db_user
