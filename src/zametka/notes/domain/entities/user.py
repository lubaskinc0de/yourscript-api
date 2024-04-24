from __future__ import annotations

from datetime import datetime
from typing import Any

from zametka.notes.domain.value_objects.user.user_first_name import UserFirstName
from zametka.notes.domain.value_objects.user.user_id import UserId
from zametka.notes.domain.value_objects.user.user_joined_at import UserJoinedAt
from zametka.notes.domain.value_objects.user.user_last_name import UserLastName


class User:
    __slots__ = (
        "first_name",
        "last_name",
        "joined_at",
        "user_id",
    )

    def __init__(
        self,
        user_id: UserId,
        first_name: UserFirstName,
        last_name: UserLastName,
    ) -> None:
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.joined_at = UserJoinedAt(datetime.now())

    def __eq__(self, other: User | Any) -> bool:
        if isinstance(other, User) and other.user_id == self.user_id:
            return True
        return False

    def __str__(self):
        return f"User <{self.user_id}>"
