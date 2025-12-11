import pytest

from exceptions.primitives.game_description_exception import GameDescriptionException
from primitives.game_description import GameDescription


def test_game_description_creation_failed_on_min_len():
    with pytest.raises(GameDescriptionException):
        GameDescription("")

def test_game_description_creation_failed_on_max_len():
    with pytest.raises(GameDescriptionException):
        GameDescription("a" * 201)

def test_game_description_creation_failed_on_invalid_name():
    with pytest.raises(GameDescriptionException):
        GameDescription("<script>alert(42)</script>")

def test_game_description_creation_successful():
    GameDescription("A very intuitive and engaging game to play with your friends")

def test_game_description_str():
    assert (str(GameDescription("A very intuitive and engaging game to play with your friends")) ==
            "A very intuitive and engaging game to play with your friends")