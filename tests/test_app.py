import pytest

from app import App
from main import main
from unittest.mock import patch, Mock


@patch("builtins.input", side_effect=["0"])
@patch("builtins.print")
def test_app_main(mocked_print, mocked_input):
    main()
    mocked_print.assert_any_call("*** Fiordispino App ***")
    mocked_print.assert_any_call("0:\tExit")
    mocked_print.assert_any_call("Goodbye!")
    mocked_input.assert_called()

@patch("getpass.getpass", return_value="string12")
@patch("requests.post")
@patch("builtins.input", side_effect=["1", "user@gmail.com", "4", "0"])
@patch("builtins.print")
def test_app_login(mocked_print, mocked_input, mocked_post, mocked_getpass):
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"key": "a" * 40}
    mocked_post.return_value = response

    App().run()

    mocked_print.assert_any_call("\nLogged in successfully!")


@patch("getpass.getpass", return_value="string12")
@patch("requests.post")
@patch("builtins.input", side_effect=["1", "user@gmail.com", "0"])
@patch("builtins.print")
def test_app_login_failed_response(mocked_print, mocked_input, mocked_post, mocked_getpass):
    response = Mock()
    response.status_code = 403
    response.text = '{"error": "Invalid credentials"}'
    response.json.return_value = {"error": "Invalid credentials"}
    mocked_post.return_value = response

    App().run()

    assert any("Invalid credentials" in str(call.args[0]) for call in mocked_print.call_args_list)

@patch("getpass.getpass", return_value="string12")
@patch("builtins.input", side_effect=["1", "user@"])
@patch("builtins.print")
def test_app_login_wrong_email(mocked_print, mocked_input, mocked_getpass):
    App().run()

    assert any("There must be something after the @-sign." in str(call.args[0]) for call in mocked_print.call_args_list)


@patch("getpass.getpass", return_value="s")
@patch("builtins.input", side_effect=["1", "user@gmail.com"])
@patch("builtins.print")
def test_app_login_wrong_password_format(mocked_print, mocked_input, mocked_getpass):
    App().run()

    mocked_print.assert_any_call("The password format is not valid, please try again")

@patch("getpass.getpass", side_effect=["string12", "string12"])
@patch("requests.post")
@patch("builtins.input", side_effect=["2", "giovanni", "giovanni@gmail.com", "4", "0"])
@patch("builtins.print")
def test_app_register(mocked_print, mocked_input, mocked_post, mocked_getpass):
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"key": "a" * 40}
    mocked_post.return_value = response

    App().run()

    mocked_print.assert_any_call("\nLogged in successfully!")

@patch("getpass.getpass", return_value="string12")
@patch("requests.post")
@patch("builtins.input", side_effect=["2", "giovanni", "giovanni@gmail.com", "0"])
@patch("builtins.print")
def test_app_register_failed_response(mocked_print, mocked_input, mocked_post, mocked_getpass):
    response = Mock()
    response.status_code = 400
    response.text = '{"password": ["This password is too common"]}'
    response.json.return_value = {"password": ["This password is too common"]}
    mocked_post.return_value = response

    App().run()

    assert any("This password is too common" in str(call.args[0]) for call in mocked_print.call_args_list)


@patch("builtins.input", side_effect=["2", "", "giovanni@gmail.com", "0"])
@patch("builtins.print")
def test_app_register_invalid_username(mocked_print, mocked_input):
    App().run()

    mocked_print.assert_any_call("Invalid username: it should have between 1 and 150 characters and can include numbers and special characters in [_@+.-]. Please try again")

@patch("getpass.getpass", return_value="")
@patch("builtins.input", side_effect=["2", "gino", "giovanni@gmail.com", "0"])
@patch("builtins.print")
def test_app_register_invalid_password(mocked_print, mocked_input, mocked_getpass):
    App().run()

    mocked_print.assert_any_call("Error in creating password. Please try again")

@patch("getpass.getpass", side_effect=["string12", "string13"])
@patch("builtins.input", side_effect=["2", "gino", "giovanni@gmail.com", "0"])
@patch("builtins.print")
def test_app_register_passwords_dont_match(mocked_print, mocked_input, mocked_getpass):
    App().run()

    mocked_print.assert_any_call("The two passwords do not match. Please try again")
