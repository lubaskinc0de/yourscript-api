
from sqlalchemy import delete, func, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession

from zametka.notes.application.common.repository import NoteRepository
from zametka.notes.application.note.dto import DBNoteDTO, ListNotesDTO
from zametka.notes.domain.entities.note import DBNote
from zametka.notes.domain.entities.note import Note as NoteEntity
from zametka.notes.domain.value_objects.note.note_id import NoteId
from zametka.notes.domain.value_objects.user.user_id import UserId
from zametka.notes.infrastructure.db.models.note import Note
from zametka.notes.infrastructure.repositories.converters.note import (
    note_db_data_to_db_note_dto,
    note_db_model_to_db_note_dto,
    note_db_model_to_db_note_entity,
    note_entity_to_db_model,
    notes_to_dto,
)


class NoteRepositoryImpl(NoteRepository):
    """Repository of notes part of app"""

    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        note: NoteEntity,
    ) -> DBNoteDTO:
        """Create"""

        db_note = note_entity_to_db_model(note)

        self.session.add(db_note)
        await self.session.flush(objects=[db_note])

        return note_db_model_to_db_note_dto(db_note)

    async def get(self, note_id: NoteId) -> DBNote | None:
        """Get by id"""

        q = select(Note).where(Note.note_id == note_id.to_raw())

        res = await self.session.execute(q)

        note: Note | None = res.scalar()

        if not note:
            return None

        return note_db_model_to_db_note_entity(note)

    async def update(
        self, note_id: NoteId, updated_note: DBNote,
    ) -> DBNoteDTO | None:
        """Update"""

        q = (
            update(Note)
            .where(Note.note_id == note_id.to_raw())
            .values(
                title=updated_note.title.to_raw(),
                text=updated_note.text.to_raw() if updated_note.text else None,
            )
            .returning(
                Note.note_id,
                Note.title,
                Note.text,
            )
        )

        res = await self.session.execute(q)

        note: tuple[int, str, str | None] | None = res.first()  # type:ignore

        if not note:
            return None

        return note_db_data_to_db_note_dto(note)

    async def list(self, limit: int, offset: int, author_id: UserId) -> ListNotesDTO:
        """List"""

        q = (
            select(Note.title, Note.note_id)
            .where(Note.author_id == author_id.to_raw())
            .limit(limit + 1)
            .offset(offset)
            .order_by(Note.created_at)
        )

        res = await self.session.execute(q)
        db_notes = res.all()

        notes = notes_to_dto(db_notes)

        has_next = False

        if len(notes) > limit:
            has_next = True

            notes.pop()

        return ListNotesDTO(notes=notes, has_next=has_next)

    async def search(
        self, query: str, limit: int, offset: int, author_id: UserId,
    ) -> ListNotesDTO:
        """FTS"""

        columns = func.coalesce(Note.title, "")
        columns = columns.self_group()  # type:ignore

        await self.session.execute(text("SET pg_trgm.similarity_threshold=0.2"))

        q = (
            select(Note.title, Note.note_id, func.similarity(columns, query))
            .where(Note.author_id == author_id.to_raw())
            .where(columns.bool_op("%")(query))
            .limit(limit + 1)
            .offset(offset)
            .order_by(func.similarity(columns, query).desc())
            .order_by(Note.created_at)
        )

        res = await self.session.execute(q)
        db_notes = res.all()

        notes = notes_to_dto(db_notes)

        has_next = False

        if len(notes) > limit:
            has_next = True

            notes.pop()

        return ListNotesDTO(notes=notes, has_next=has_next)

    async def delete(self, note_id: NoteId) -> None:
        """Delete"""

        q = delete(Note).where(Note.note_id == note_id.to_raw())

        await self.session.execute(q)
