from unittest.mock import patch

from functionalities.description import Description
from functionalities.entry import Entry
from functionalities.menu import Menu


@patch('builtins.input', side_effect=['1', '0'])
@patch('builtins.print')
def test_menu_selection_call_on_selected(mocked_print, mocked_input):
    menu = (Menu.Builder(Description("A totally normal description")).
            with_entry(Entry.create("1", "Ask the time", on_selected=lambda: print("It's muffin time!"))).
            with_entry(Entry.create("0", "Exit", is_exit=True)).
            build())

    menu.run()
    mocked_print.assert_any_call("It's muffin time!")
    mocked_input.assert_called()

@patch("builtins.input", side_effect=['-1', '0'])
@patch('builtins.print')
def test_menu_selection_on_wrong_key(mocked_print, mocked_input):
    menu = (Menu.Builder(Description("A totally normal description")).
            with_entry(Entry.create("1", "Ask the time", on_selected=lambda: print("It's muffin time!"))).
            with_entry(Entry.create("0", "Exit", is_exit=True)).
            build())

    menu.run()
    mocked_print.assert_any_call("Invalid key, please try again")
    mocked_input.assert_called()