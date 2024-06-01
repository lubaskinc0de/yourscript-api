import sys

import alembic.config

from zametka.access_service.infrastructure.persistence.alembic.config import (
    ALEMBIC_CONFIG as ACCESS_SERVICE_ALEMBIC,
)
from zametka.notes.infrastructure.db.alembic.config import (
    ALEMBIC_CONFIG as NOTES_ALEMBIC,
)


def notes_alembic_handler(args: list[str]) -> None:
    alembic.config.main(
        argv=["-c", NOTES_ALEMBIC, *args],
    )


def access_service_alembic_handler(args: list[str]) -> None:
    alembic.config.main(
        argv=["-c", ACCESS_SERVICE_ALEMBIC, *args],
    )


def all_alembic_handler(args: list[str]) -> None:
    notes_alembic_handler(args)
    access_service_alembic_handler(args)


def main() -> None:
    print(">> zametka CLI <<")

    argv = sys.argv[1:]

    if not argv:
        print(">> Hi, my friend.")
        return

    try:
        module = argv[0]
        option = argv[1]
        args = argv[2:]
    except IndexError:
        print(">> Invalid option!")
        return

    modules = {
        "notes": {
            "alembic": notes_alembic_handler,
        },
        "access_service": {
            "alembic": access_service_alembic_handler,
        },
        "all": {
            "alembic": all_alembic_handler,
        },
    }

    if module not in modules:
        print(">> No such module.")
        return

    if option not in modules[module]:
        print(">> No such option.")
        return

    modules[module][option](args)
