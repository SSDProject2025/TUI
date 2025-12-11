import pytest

from exceptions.primitives.username_exception import UsernameException
from primitives.username import Username


def test_username_creation_failed_on_min_length():
    with pytest.raises(UsernameException):
        Username('')

def test_username_creation_failed_on_max_length():
    with pytest.raises(UsernameException):
        Username('a' * 151)

def test_username_creation_failed_on_invalid_username():
    with pytest.raises(UsernameException):
        Username('<script>alert(42)</script>')

def test_username_creation_successful():
    Username("maborroto98_@+.-")

def test_username_str():
    assert str(Username("maborroto98_@+.-")) == "maborroto98_@+.-"