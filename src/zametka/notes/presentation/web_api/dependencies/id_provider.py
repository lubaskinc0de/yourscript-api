from typing import Annotated, Optional

from aiohttp import ClientSession
from fastapi import Cookie, Request, Depends

from zametka.notes.domain.exceptions.user import IsNotAuthorizedError
from zametka.notes.domain.value_objects.user.user_id import UserId
from zametka.notes.infrastructure.id_provider import (
    TokenIdProvider,
    RawIdProvider,
)
from zametka.notes.infrastructure.access_api_client import AccessAPIClient
from zametka.notes.presentation.web_api.dependencies.stub import Stub
from zametka.notes.presentation.web_api.schemas.user import IdentitySchema


async def get_token_id_provider(
    request: Request,
    aiohttp_session: Annotated[ClientSession, Depends(Stub(ClientSession))],
    csrf_access_token: Annotated[Optional[str], Cookie()] = None,
    access_token_cookie: Annotated[Optional[str], Cookie()] = None,
) -> TokenIdProvider:
    csrf_methods = {"POST", "PUT", "PATCH", "DELETE"}

    if not access_token_cookie:
        raise IsNotAuthorizedError()

    api_client = AccessAPIClient(access_token_cookie, session=aiohttp_session)

    if request.method in csrf_methods:
        if not csrf_access_token:
            raise IsNotAuthorizedError()

        api_client = AccessAPIClient(
            access_token_cookie, aiohttp_session, csrf_access_token
        )
        await api_client.ensure_can_edit(
            headers={"X-CSRF-Token": request.headers.get("X-CSRF-Token", "")}
        )

    id_provider = TokenIdProvider(api_client)

    return id_provider


async def get_raw_id_provider(identity_data: IdentitySchema) -> RawIdProvider:
    return RawIdProvider(user_id=UserId(identity_data.identity_id))
