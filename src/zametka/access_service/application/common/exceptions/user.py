from zametka.access_service.application.common.exceptions.base import ApplicationError


class UserIsNotExistsError(ApplicationError): ...


class UserEmailAlreadyExistsError(ApplicationError): ...
