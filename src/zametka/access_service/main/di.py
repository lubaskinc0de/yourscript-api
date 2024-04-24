from aiosmtplib import SMTP
from dishka import Provider, Scope, AsyncContainer, make_async_container, provide, from_context
from fastapi import Request

from fastapi_another_jwt_auth import AuthJWT
from jinja2 import Environment, PackageLoader, select_autoescape

from zametka.access_service.application.authorize import Authorize
from zametka.access_service.application.common.event import EventEmitter
from zametka.access_service.application.common.id_provider import IdProvider, UserProvider
from zametka.access_service.application.common.repository import UserGateway
from zametka.access_service.application.common.token_sender import TokenSender
from zametka.access_service.application.common.uow import UoW
from zametka.access_service.application.create_user import CreateUser
from zametka.access_service.application.delete_user import DeleteUser
from zametka.access_service.application.get_user import GetUser
from zametka.access_service.application.verify_email import VerifyEmail
from zametka.access_service.infrastructure.email.aio_email_client import AioSMTPEmailClient
from zametka.access_service.infrastructure.email.email_token_sender import EmailTokenSender
from zametka.access_service.infrastructure.event_bus.event_emitter import EventEmitterImpl

from zametka.access_service.infrastructure.id_provider import JWTTokenProcessor, TokenIdProvider, UserProviderImpl

from zametka.access_service.infrastructure.persistence.provider import (
    get_async_session,
    get_engine,
    get_async_sessionmaker,
)
from zametka.access_service.infrastructure.persistence.uow import SAUnitOfWork
from zametka.access_service.infrastructure.gateway.user import UserGatewayImpl

from zametka.access_service.main.config_loader import (
    load_all_config,
    DBConfig,
    AMQPConfig,
    MailConfig
)


def gateway_provider() -> Provider:
    provider = Provider()

    provider.provide(UserGatewayImpl, scope=Scope.REQUEST, provides=UserGateway)
    provider.provide(SAUnitOfWork, scope=Scope.REQUEST, provides=UoW)

    return provider


def db_provider() -> Provider:
    provider = Provider()

    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_async_sessionmaker, scope=Scope.APP)
    provider.provide(get_async_session, scope=Scope.REQUEST)

    return provider


def interactor_provider() -> Provider:
    provider = Provider()

    provider.provide(CreateUser, scope=Scope.REQUEST)
    provider.provide(DeleteUser, scope=Scope.REQUEST)
    provider.provide(GetUser, scope=Scope.REQUEST)
    provider.provide(Authorize, scope=Scope.REQUEST)
    provider.provide(VerifyEmail, scope=Scope.REQUEST)

    return provider


def infrastructure_provider() -> Provider:
    provider = Provider()

    provider.provide(UserProviderImpl, scope=Scope.REQUEST, provides=UserProvider)
    provider.provide(EventEmitterImpl, scope=Scope.REQUEST, provides=EventEmitter)

    return provider


def config_provider() -> Provider:
    provider = Provider()
    config = load_all_config()

    provider.provide(lambda: config.db, scope=Scope.APP, provides=DBConfig)
    provider.provide(lambda: config.mail, scope=Scope.APP, provides=MailConfig)
    provider.provide(lambda: config.amqp, scope=Scope.APP, provides=AMQPConfig)

    return provider


class HTTPProvider(Provider):
    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    def get_idp(self, request: Request) -> IdProvider:
        jwt_auth = AuthJWT(request)
        jwt_auth.jwt_required()  # TODO: workaround on this dirty move

        token_processor = JWTTokenProcessor(token_processor=jwt_auth)
        id_provider = TokenIdProvider(token_processor=token_processor)

        return id_provider

    @provide(scope=Scope.APP)
    def get_token_sender(self, config: MailConfig) -> TokenSender:
        jinja_env: Environment = Environment(
            loader=PackageLoader("zametka.access_service.presentation.web_api"),
            autoescape=select_autoescape(),
        )
        email_client = AioSMTPEmailClient(SMTP(hostname=config.mail_server, port=config.mail_port))
        token_sender = EmailTokenSender(email_client, jinja_env)

        return token_sender


def setup_providers() -> list[Provider]:
    providers = [
        gateway_provider(),
        db_provider(),
        interactor_provider(),
        infrastructure_provider(),
        config_provider(),
    ]
    return providers


def setup_di() -> AsyncContainer:
    providers = setup_providers()
    container = make_async_container(*providers)

    return container


def setup_http_di() -> AsyncContainer:
    providers = setup_providers()
    providers += [HTTPProvider()]

    container = make_async_container(*providers, skip_validation=True)
    return container
