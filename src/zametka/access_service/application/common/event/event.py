from abc import ABC
from typing import TypeVar


class Event(ABC):
    def __str__(self) -> str:
        return self.__class__.__name__


EventT = TypeVar("EventT", bound=Event)  # e.g Event1
EventsT = TypeVar("EventsT", bound=Event)  # e.g Event1 | Event 2
