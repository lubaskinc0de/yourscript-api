from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScriptSchema:
    id: int
    title: str
    text: str
    created_at: datetime
    author_id: int


@dataclass
class ScriptReaderSuccessResponse:
    script: ScriptSchema


@dataclass
class CreateScriptSuccessResponse(ScriptReaderSuccessResponse):
    pass


@dataclass
class ReadScriptSuccessResponse(ScriptReaderSuccessResponse):
    pass


@dataclass
class UpdateScriptSuccessResponse(ScriptReaderSuccessResponse):
    pass


@dataclass
class DeleteScriptSuccessResponse:
    pass
