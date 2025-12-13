import pytest
from exceptions.primitives.game_title_exception import GameTitleException
from primitives.game_title import GameTitle


def test_game_title_creation_failed_on_min_lenght():
    with pytest.raises(GameTitleException):
        GameTitle("")

def test_game_title_creation_failed_on_max_lenght():
    with pytest.raises(GameTitleException):
        GameTitle("a"*101)

def test_game_title_creation_failed_on_invalid_title():
    with pytest.raises(GameTitleException):
        GameTitle("a#")

def test_game_title_creation_successful():
    GameTitle("Call Of Duty: Black Ops III")

def test_game_title_str():
    assert str(GameTitle("Call Of Duty: Black Ops III")) == "Call Of Duty: Black Ops III"