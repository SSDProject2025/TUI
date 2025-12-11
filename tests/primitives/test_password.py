import pytest

from exceptions.primitives.password_exception import PasswordException
from primitives.password import Password


def test_password_creation_failed():
    with pytest.raises(PasswordException):
        Password("")

def test_password_creation_successful():
    Password("Abcde12345!_X")

def test_password_str():
    assert str(Password("Abcde12345!_X")) == "Abcde12345!_X"