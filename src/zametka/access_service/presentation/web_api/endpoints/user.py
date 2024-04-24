from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends
from fastapi_another_jwt_auth import AuthJWT

from zametka.access_service.application.authorize import Authorize
from zametka.access_service.application.create_user import CreateUser
from zametka.access_service.application.delete_user import DeleteUser
from zametka.access_service.application.get_user import GetUser
from zametka.access_service.application.verify_email import VerifyEmail

from zametka.access_service.application.dto import UserDTO
from zametka.access_service.application.verify_email import TokenInputDTO
from zametka.access_service.application.authorize import AuthorizeInputDTO
from zametka.access_service.application.create_user import CreateUserInputDTO

from zametka.access_service.presentation.web_api.schemas.user import (
    AuthorizeSchema,
    CreateIdentitySchema,
)

router = APIRouter(
    prefix="/access",
    tags=["access"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
@inject
async def create_identity(
    data: CreateIdentitySchema,
    interactor: FromDishka[CreateUser],
) -> UserDTO:
    response = await interactor(
        CreateUserInputDTO(
            email=data.email,
            password=data.password,
        )
    )

    return response


@router.post("/authorize")
@inject
async def authorize(
    data: AuthorizeSchema,
    interactor: FromDishka[Authorize],
    token_processor: AuthJWT = Depends(),
) -> UserDTO:
    response = await interactor(
        AuthorizeInputDTO(
            email=data.email,
            password=data.password,
        )
    )

    subject = response.user_id
    access = token_processor.create_access_token(subject=str(subject))
    token_processor.set_access_cookies(access)

    return response


@router.get("/me")
@inject
async def get_identity(
    interactor: FromDishka[GetUser]
) -> UserDTO:
    response = await interactor()
    return response


# @router.get("/verify/{token}")
# @inject
# async def verify_email(token: str, interactor: VerifyEmail) -> None:
#     await interactor(
#         TokenInputDTO(
#             token=token,
#         )
#     )
