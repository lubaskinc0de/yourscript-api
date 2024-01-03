from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class NoteDTO:
    title: str
    text: Optional[str]


@dataclass(frozen=True, kw_only=True)
class DBNoteDTO(NoteDTO):
    note_id: int


@dataclass(frozen=True, kw_only=True)
class ListNoteDTO:
    title: str
    note_id: int


@dataclass(frozen=True)
class CreateNoteInputDTO:
    title: str
    text: Optional[str] = None


@dataclass(frozen=True)
class UpdateNoteInputDTO:
    note_id: int
    title: str
    text: Optional[str] = None


@dataclass(frozen=True)
class ReadNoteInputDTO:
    note_id: int


@dataclass(frozen=True)
class ListNotesInputDTO:
    limit: int
    offset: int
    search: Optional[str] = None


@dataclass(frozen=True)
class ListNotesDTO:
    notes: list[ListNoteDTO]
    has_next: bool


@dataclass(frozen=True)
class DeleteNoteInputDTO:
    note_id: int
