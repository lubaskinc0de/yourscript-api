from typing import Callable, Any


class Stub:
    """
    This class is used to prevent fastapi from digging into
    real dependencies attributes detecting them as request data

    So instead of
    `interactor: Annotated[Interactor, Depends()]`
    Write
    `interactor: Annotated[Interactor, Depends(Stub(Interactor))]`

    And then you can declare how to create it:
    `app.dependency_overridess[Interactor] = some_real_factory`

    """

    def __init__(
        self, dependency: Callable[[Any], Any], **kwargs: dict[str, Any]
    ) -> None:
        self._dependency = dependency
        self._kwargs = kwargs

    def __call__(self) -> None:
        raise NotImplementedError

    def __eq__(self, other: "Stub | Any") -> bool:
        if isinstance(other, Stub):
            return (
                self._dependency == other._dependency and self._kwargs == other._kwargs
            )
        else:
            if not self._kwargs:
                return self._dependency == other  # type:ignore
            return False

    def __hash__(self) -> int:
        if not self._kwargs:
            return hash(self._dependency)
        serial = (
            self._dependency,
            *self._kwargs.items(),
        )
        return hash(serial)
