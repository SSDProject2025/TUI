from dataclasses import dataclass

from typeguard import typechecked
from valid8 import validate, ValidationError

from exceptions.primitives.game_description_exception import GameDescriptionException
from utils.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class GameDescription:
    description: str

    def __post_init__(self):
        try:
            validate("description", self.description, min_len=1, max_len=200, custom=pattern(r'^[\w\s!,;:.?\'"()-]*$'))
        except ValidationError:
            raise GameDescriptionException

    def __str__(self):
        return self.description