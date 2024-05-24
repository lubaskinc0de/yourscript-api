from typing import Optional

from fastapi import APIRouter, Depends

from zametka.notes.application.note.dto import (
    CreateNoteInputDTO,
    DeleteNoteInputDTO,
    ReadNoteInputDTO,
    ListNotesInputDTO,
    UpdateNoteInputDTO,
    DBNoteDTO,
    ListNotesDTO,
)

from zametka.notes.application.common.id_provider import IdProvider
from zametka.notes.presentation.interactor_factory import InteractorFactory
from zametka.notes.presentation.web_api.schemas.note import NoteSchema

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def create(
    note: NoteSchema,
    ioc: InteractorFactory = Depends(),
    id_provider: IdProvider = Depends(),
) -> DBNoteDTO:
    async with ioc.pick_note_interactor(id_provider, lambda i: i.create) as interactor:
        response = await interactor(
            CreateNoteInputDTO(
                text=note.text,
                title=note.title,
            )
        )

        return response


@router.get("/{note_id}")
async def read(
    note_id: int,
    ioc: InteractorFactory = Depends(),
    id_provider: IdProvider = Depends(),
) -> DBNoteDTO:
    async with ioc.pick_note_interactor(id_provider, lambda i: i.read) as interactor:
        response = await interactor(
            ReadNoteInputDTO(
                note_id=note_id,
            )
        )

        return response


@router.put("/{note_id}")
async def update(
    new_note: NoteSchema,
    note_id: int,
    ioc: InteractorFactory = Depends(),
    id_provider: IdProvider = Depends(),
) -> DBNoteDTO:
    async with ioc.pick_note_interactor(id_provider, lambda i: i.update) as interactor:
        response = await interactor(
            UpdateNoteInputDTO(
                note_id=note_id,
                title=new_note.title,
                text=new_note.text,
            )
        )

        return response


@router.get("/")
async def list_notes(
    limit: int,
    offset: int,
    search: Optional[str] = None,
    ioc: InteractorFactory = Depends(),
    id_provider: IdProvider = Depends(),
) -> ListNotesDTO:
    if search and len(search) > 50:
        raise ValueError("Слишком длинный поисковый запрос!")

    async with ioc.pick_note_interactor(id_provider, lambda i: i.list) as interactor:
        response = await interactor(
            ListNotesInputDTO(
                limit=limit,
                offset=offset,
                search=search,
            )
        )

        return response


@router.delete("/{note_id}")
async def delete(
    note_id: int,
    ioc: InteractorFactory = Depends(),
    id_provider: IdProvider = Depends(),
) -> None:
    async with ioc.pick_note_interactor(id_provider, lambda i: i.delete) as interactor:
        await interactor(
            DeleteNoteInputDTO(
                note_id=note_id,
            )
        )
