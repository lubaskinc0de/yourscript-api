from __future__ import annotations

from datetime import datetime
from typing import Optional, Any

from zametka.notes.domain.value_objects.note.note_created_at import (
    NoteCreatedAt,
)
from zametka.notes.domain.value_objects.note.note_id import NoteId
from zametka.notes.domain.value_objects.note.note_text import NoteText
from zametka.notes.domain.value_objects.note.note_title import NoteTitle
from zametka.notes.domain.value_objects.user.user_id import UserId


class Note:
    __slots__ = (
        "title",
        "author_id",
        "text",
        "created_at",
    )

    def __init__(
        self,
        title: NoteTitle,
        author_id: UserId,
        text: Optional[NoteText] = None,
        created_at: Optional[NoteCreatedAt] = None,
    ) -> None:
        self.title = title
        self.author_id = author_id
        self.text = text
        self.created_at = created_at

        if not self.created_at:
            self.created_at = NoteCreatedAt(datetime.now())

    def merge(self, other: Note) -> Note:
        return Note(
            title=other.title,
            text=other.text or self.text,
            author_id=self.author_id,
            created_at=self.created_at,
        )

    def has_access(self, user_id: UserId) -> bool:
        return self.author_id == user_id

    def __str__(self) -> str:
        return f"Note: {self.title}"


class DBNote(Note):
    __slots__ = ("note_id",)

    def __init__(
        self,
        title: NoteTitle,
        author_id: UserId,
        note_id: NoteId,
        text: Optional[NoteText] = None,
        created_at: Optional[NoteCreatedAt] = None,
    ) -> None:
        super().__init__(
            title=title,
            author_id=author_id,
            text=text,
            created_at=created_at,
        )
        self.note_id = note_id

    def merge(self, other: Note) -> DBNote:
        merged = super().merge(other)
        return DBNote(
            title=merged.title,
            author_id=merged.author_id,
            note_id=self.note_id,
            text=merged.text,
            created_at=merged.created_at,
        )

    def __eq__(self, other: DBNote | Any) -> bool:
        if isinstance(other, DBNote) and other.note_id == self.note_id:
            return True
        return False
