from dataclasses import dataclass

from typeguard import typechecked
from valid8 import validate, ValidationError

from exceptions.primitives.genre_exception import GenreException
from utils.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class Genre:
    genre: str

    def __post_init__(self):
        try:
            validate("genre", self.genre, min_len=1, max_len=100, custom=pattern(r'[a-zA-Z\s]*'))
        except ValidationError:
            raise GenreException

    def __str__(self):
        return self.genre