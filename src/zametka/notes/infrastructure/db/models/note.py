from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from zametka.notes.infrastructure.db.models.base import Base


class Note(Base):
    """The user notes"""

    __tablename__ = "notes"

    note_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str | None] = mapped_column(String(60000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    author_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("users.identity_id"), nullable=False,
    )
