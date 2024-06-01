
from zametka.notes.application.common.id_provider import IdProvider
from zametka.notes.application.common.repository import NoteRepository
from zametka.notes.application.common.uow import UoW
from zametka.notes.application.note.dto import (
    CreateNoteInputDTO,
    DBNoteDTO,
    DeleteNoteInputDTO,
    ListNotesDTO,
    ListNotesInputDTO,
    ReadNoteInputDTO,
    UpdateNoteInputDTO,
)
from zametka.notes.domain.entities.note import DBNote, Note
from zametka.notes.domain.exceptions.note import (
    NoteAccessDeniedError,
    NoteNotExistsError,
)
from zametka.notes.domain.value_objects.note.note_id import NoteId
from zametka.notes.domain.value_objects.note.note_text import NoteText
from zametka.notes.domain.value_objects.note.note_title import NoteTitle
from zametka.notes.domain.value_objects.user.user_id import UserId


class NoteInteractor:
    def __init__(
        self,
        note_repository: NoteRepository,
        uow: UoW,
        id_provider: IdProvider,
    ):
        self.uow = uow
        self.note_repository = note_repository
        self.id_provider = id_provider

    async def _check_exists(self, note_id: NoteId) -> DBNote:
        """Raises NoteNotExists if note with given id is not exists"""

        note: DBNote | None = await self.note_repository.get(note_id)

        if not note:
            raise NoteNotExistsError()

        return note

    async def _get_note(self, note_id: NoteId) -> DBNote:
        """
        Check can user do actions with this note. These are two checks.

        1. Is note exists
        2. Is user are author of this note
        """

        note: DBNote = await self._check_exists(note_id)

        user_id: UserId = await self.id_provider.get_user_id()

        if not note.has_access(user_id):
            raise NoteAccessDeniedError()

        return note

    async def create(self, data: CreateNoteInputDTO) -> DBNoteDTO:
        user_id: UserId = await self.id_provider.get_user_id()

        title = NoteTitle(data.title)
        text = NoteText(data.text) if data.text else None

        note: Note = Note(title, user_id, text)

        note_dto = await self.note_repository.create(note)
        await self.uow.commit()

        return note_dto

    async def read(self, data: ReadNoteInputDTO) -> DBNoteDTO:
        """Read by id use case"""

        note: DBNote = await self._get_note(NoteId(data.note_id))

        return DBNoteDTO(
            title=note.title.to_raw(),
            text=note.text.to_raw() if note.text else None,
            note_id=note.note_id.to_raw(),
        )

    async def update(self, data: UpdateNoteInputDTO) -> DBNoteDTO:
        note: DBNote = await self._get_note(NoteId(data.note_id))

        title = NoteTitle(data.title)
        text = NoteText(data.text) if data.text else None

        new_note: Note = Note(title, note.author_id, text)
        updated_note: DBNote = note.merge(new_note)

        updated_db_note = await self.note_repository.update(
            NoteId(data.note_id), updated_note,
        )

        if not updated_db_note:
            raise NoteNotExistsError()

        await self.uow.commit()

        return updated_db_note

    async def list(self, data: ListNotesInputDTO) -> ListNotesDTO:
        user_id: UserId = await self.id_provider.get_user_id()

        offset: int = data.offset
        limit: int = data.limit

        if not data.search:
            dto: ListNotesDTO = await self.note_repository.list(
                author_id=user_id,
                limit=limit,
                offset=offset,
            )
        else:
            dto: ListNotesDTO = await self.note_repository.search(  # type:ignore
                author_id=user_id,
                query=data.search,
                limit=limit,
                offset=offset,
            )

        return ListNotesDTO(notes=dto.notes, has_next=dto.has_next)

    async def delete(self, data: DeleteNoteInputDTO) -> None:
        await self._get_note(NoteId(data.note_id))

        await self.note_repository.delete(NoteId(data.note_id))
        await self.uow.commit()
