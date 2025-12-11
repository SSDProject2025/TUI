import pytest

from exceptions.primitives.genre_exception import GenreException
from primitives.genre import Genre

def test_genre_creation_failed_on_min_lenght():
    with pytest.raises(GenreException):
        Genre("")

def test_genre_creation_failed_on_max_lenght():
    string = "a" * 101
    with pytest.raises(GenreException):
        Genre(string)

def test_genre_creation_failed_on_invalid_title():
    with pytest.raises(GenreException):
        Genre("Shooter.")

def test_genre_creation_successful():
    Genre("Shooter")

def test_genre_str():
    assert str(Genre("Shooter")) == "Shooter"