import os

ALEMBIC_CONFIG = os.path.join(  # noqa: PTH118
    os.path.dirname(os.path.abspath(__file__)),  # noqa: PTH100, PTH120
    "alembic.ini",
)
