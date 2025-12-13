from unittest.mock import Mock, patch, call

import pytest

from exceptions.functionalities.entry_exception import EntryException
from functionalities.description import Description
from functionalities.entry import Entry
from functionalities.key import Key

@patch('builtins.print')
def test_entry_on_selected(mocked_print):
    entry = Entry(Key("1"), Description("test"), on_selected=lambda: print("test"))
    entry.on_selected()
    assert mocked_print.mock_calls == [call("test")]

def test_entry_creation_failure():
    with pytest.raises(EntryException):
        Entry(Key("1"), "test", on_selected=lambda: None)

def test_entry_create():
    mocked_on_select = Mock()
    Entry.create("1", "test", on_selected=lambda: mocked_on_select())