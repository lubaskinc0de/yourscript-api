
from pydantic import BaseModel


class NoteSchema(BaseModel):
    title: str
    text: str | None = None
