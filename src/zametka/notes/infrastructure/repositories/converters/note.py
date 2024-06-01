from collections.abc import Sequence

from sqlalchemy import Row

from zametka.notes.application.note.dto import DBNoteDTO, ListNoteDTO
from zametka.notes.domain.entities.note import DBNote
from zametka.notes.domain.entities.note import Note as NoteEntity
from zametka.notes.domain.value_objects.note.note_created_at import (
    NoteCreatedAt,
)
from zametka.notes.domain.value_objects.note.note_id import NoteId
from zametka.notes.domain.value_objects.note.note_text import NoteText
from zametka.notes.domain.value_objects.note.note_title import NoteTitle
from zametka.notes.domain.value_objects.user.user_id import UserId
from zametka.notes.infrastructure.db.models.note import Note


def note_db_data_to_db_note_dto(
    note: tuple[int, str, str | None],
) -> DBNoteDTO:
    return DBNoteDTO(
        note_id=note[0],
        title=note[1],
        text=note[2],
    )


def note_db_model_to_db_note_dto(note: Note) -> DBNoteDTO:
    return DBNoteDTO(
        title=note.title,
        text=note.text,
        note_id=note.note_id,
    )


def note_db_model_to_db_note_entity(note: Note) -> DBNote:
    return DBNote(
        note_id=NoteId(note.note_id),
        title=NoteTitle(note.title),
        text=NoteText(note.text) if note.text else None,
        author_id=UserId(note.author_id),
        created_at=NoteCreatedAt(note.created_at),
    )


def note_db_model_to_list_note_dto(note: Row[tuple[str, int]]) -> ListNoteDTO:
    return ListNoteDTO(
        title=note[0],
        note_id=note[1],
    )


def notes_to_dto(notes: Sequence[Row[tuple[str, int]]]) -> list[ListNoteDTO]:
    return [note_db_model_to_list_note_dto(note) for note in notes]


def note_entity_to_db_model(note: NoteEntity) -> Note:
    db_note = Note(
        title=note.title.to_raw(),
        text=note.text.to_raw() if note.text else None,
        created_at=note.created_at.to_raw(),
        author_id=note.author_id.to_raw(),
    )

    return db_note
