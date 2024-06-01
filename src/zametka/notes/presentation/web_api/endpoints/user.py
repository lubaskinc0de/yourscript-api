from typing import Annotated

from fastapi import APIRouter, Depends

from zametka.notes.application.common.id_provider import IdProvider
from zametka.notes.application.user.create_user import CreateUserInputDTO
from zametka.notes.application.user.dto import UserDTO
from zametka.notes.presentation.interactor_factory import InteractorFactory
from zametka.notes.presentation.web_api.dependencies.id_provider import (
    get_raw_id_provider,
)
from zametka.notes.presentation.web_api.schemas.user import UserSchema

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def create_user(
    data: UserSchema,
    id_provider: Annotated[IdProvider, Depends(get_raw_id_provider)],
    ioc: InteractorFactory = Depends(),
) -> UserDTO:
    async with ioc.create_user(id_provider) as interactor:
        response = await interactor(
            CreateUserInputDTO(
                first_name=data.first_name,
                last_name=data.last_name,
            ),
        )

        return response


@router.get("/me")
async def get_user(
    id_provider: IdProvider = Depends(),
    ioc: InteractorFactory = Depends(),
) -> UserDTO:
    async with ioc.get_user(id_provider) as interactor:
        response = await interactor()

    return response
