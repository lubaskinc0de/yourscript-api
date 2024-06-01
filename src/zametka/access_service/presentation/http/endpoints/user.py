from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response

from zametka.access_service.application.authorize import Authorize, AuthorizeInputDTO
from zametka.access_service.application.create_user import (
    CreateUser,
    CreateUserInputDTO,
)
from zametka.access_service.application.dto import UserDTO
from zametka.access_service.application.get_user import GetUser
from zametka.access_service.application.verify_email import VerifyEmail
from zametka.access_service.infrastructure.email.confirmation_token_processor import (
    ConfirmationTokenProcessor,
)
from zametka.access_service.infrastructure.jwt.jwt_processor import JWTToken
from zametka.access_service.presentation.http.auth.token_auth import TokenAuth
from zametka.access_service.presentation.http.schemas.user import (
    AuthorizeSchema,
    CreateIdentitySchema,
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Не найдено"}},
    route_class=DishkaRoute,
)


@router.post("/")
async def create_identity(
    data: CreateIdentitySchema,
    action: FromDishka[CreateUser],
) -> UserDTO:
    response = await action(
        CreateUserInputDTO(
            email=data.email,
            password=data.password,
        ),
    )

    return response


@router.post("/authorize")
async def authorize(
    data: AuthorizeSchema,
    action: FromDishka[Authorize],
    token_auth: FromDishka[TokenAuth],
) -> Response:
    access_token = await action(
        AuthorizeInputDTO(
            email=data.email,
            password=data.password,
        ),
    )

    http_response = JSONResponse(status_code=201, content={})
    return token_auth.set_session(access_token, http_response)


@router.get("/me")
async def get_identity(action: FromDishka[GetUser]) -> UserDTO:
    response = await action()
    return response


@router.get("/verify/{token}")
async def verify_email(
    token: JWTToken,
    action: FromDishka[VerifyEmail],
    token_processor: FromDishka[ConfirmationTokenProcessor],
) -> None:
    decoded_token = token_processor.decode(token)
    await action(decoded_token)
