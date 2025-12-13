import pytest

from exceptions.primitives.vote_exception import VoteException
from primitives.vote import Vote


def test_vote_creation_failed_on_min_value():
    with pytest.raises(VoteException):
        Vote(0)

def test_vote_creation_failed_on_max_value():
    with pytest.raises(VoteException):
        Vote(11)

def test_vote_creation_successful():
    valid_values = range(1, 11)
    for value in valid_values:
        Vote(value)

def test_vote_str():
    valid_values = range(1, 11)
    for value in valid_values:
        assert(str(Vote(value)) == str(value))