import pytest

from exceptions.functionalities.key_exception import KeyException
from functionalities.key import Key


def test_key_creation_failed_on_min_length():
    with pytest.raises(KeyException):
        Key("")

def test_key_creation_failed_on_max_length():
    with pytest.raises(KeyException):
        Key("a" * 11)

def test_key_creation_failed_on_invalid_characters():
    with pytest.raises(KeyException):
        Key(".a")

def test_key_creation_successful():
    Key("1")

def test_key_str():
    assert str(Key("1")) == "1"