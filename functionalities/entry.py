from dataclasses import dataclass, field
from typing import Callable

from typeguard import typechecked

from exceptions.functionalities.entry_exception import EntryException
from functionalities.description import Description
from functionalities.key import Key
from utils.dataclasses import validate_dataclass


@typechecked
@dataclass(frozen=True)
class Entry:
    key: Key
    description: Description
    on_selected: Callable[[], None] = field(default=lambda: None)
    is_exit: bool = field(default=False)

    def __post_init__(self):
        try:
            validate_dataclass(self)
        except:
            raise EntryException

    @staticmethod
    def create(key: str, description: str, on_selected: Callable[[], None] = lambda: None, is_exit: bool = False) -> 'Entry':
        return Entry(Key(key), Description(description), on_selected, is_exit)