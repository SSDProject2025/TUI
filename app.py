import getpass
import json
import sys
from typing import Callable, Any

import requests
from requests import RequestException
from valid8 import ValidationError, validate

from exceptions.primitives.password_exception import PasswordException
from exceptions.primitives.username_exception import UsernameException
from functionalities.description import Description
from functionalities.entry import Entry
from primitives.email import Email
from primitives.password import Password
from primitives.token import Token
from primitives.username import Username
from functionalities.menu import Menu


class App:

    __base_url: str = "http://localhost:8000/api/v1"
    __token: Token
    def __init__(self):
        self.__menu = ((Menu.Builder(Description("Fiordispino App"), auto_select=lambda: None).
                       with_entry(Entry.create("1", "Login", on_selected=lambda: self.__login()))).
                       with_entry(Entry.create("2", "Register", on_selected=lambda: self.__register())).
                       with_entry(Entry.create("3", "Show Games", on_selected=lambda: self.__show_games())).
                       with_entry(Entry.create("0", "Exit", on_selected=lambda: print("Goodbye!"), is_exit=True)).
                       build())

        self.__token = Token("a" * 40)    # Temporary token

    def __login(self) -> None:
        while True:
            try:
                email = self.__read("Email", Email)
                password = self.__read_password("Password", Password)

                response = requests.post(
                    f"{self.__base_url}/auth/login/",
                    json={
                          "email": email.email,
                          "password": password.password,
                          }
                )

                if response.status_code != 200 and response.status_code != 201:
                    raise RequestException(response.text)

                print("\nLogged in successfully!")
                self.__change_tui_for_logged_user(response.json().get("key"))
                return

            except PasswordException:
                print("The password format is not valid, please try again")
            except RequestException as e:
                error_json = json.loads(str(e))
                print(error_json.get("error"))



    def __register(self) -> None:
        while True:
            try:
                username = self.__read("Username", Username)
                email = self.__read("Email", Email)
                password = self.__read_password("Password", Password)
                confirm_password = self.__read_password("Confirm Password", Password)

                validate("Confirm Password", confirm_password, equals=password)

                response = requests.post(
                    f"{self.__base_url}/auth/registration/",
                    json={"username": username.username,
                          "email": email.email,
                          "password": password.password,
                          "password2": confirm_password.password,
                          }
                )

                if response.status_code != 200 and response.status_code != 201:
                    raise RequestException(response.text)

                print("\nLogged in successfully!")
                self.__change_tui_for_logged_user(response.json().get("key"))
                return
            except UsernameException:
                print(UsernameException.help_message + ". Please try again")
            except PasswordException:
                print(PasswordException.help_message + ". Please try again")
            except ValidationError:
                print("The two passwords do not match. Please try again")
            except RequestException as e:
                error_json = json.loads(str(e))
                msg = next(iter(error_json.values()))

                # It may happen that Django decides that the error message is in a list
                if isinstance(msg, list):
                    msg = msg[0]

                print(msg)


    def __change_tui_for_logged_user(self, token: str) -> None:
        self.__token = Token(token)
        self.__menu = ((Menu.Builder(Description("Fiordispino App"), auto_select=lambda: None).
                       with_entry(Entry.create("1", "Show Games", on_selected=lambda: self.__show_games())).
                       with_entry(Entry.create("2", "Show games to play", on_selected=lambda: self.__show_games_to_play())).
                       with_entry(Entry.create("3", "Show games played", on_selected=lambda: self.__show_games_played()))).
                       with_entry(Entry.create("4", "Logout", on_selected=lambda: None, is_exit=True)).
                       with_entry(Entry.create("0", "Exit", on_selected=lambda: sys.exit("Goodbye!"), is_exit=True)).
                       build())

        self.run()

    def __show_games(self) -> None:
        pass

    def __show_games_to_play(self):
        pass

    def __show_games_played(self):
        pass

    @staticmethod
    def __read_password(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                line = getpass.getpass(prompt=f"{prompt}: ")
                res = builder(line.strip())
                return res
            except (TypeError, ValueError, ValidationError) as e:
                print(e)

    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                line = input(f"{prompt}: ")
                res = builder(line.strip())
                return res
            except (TypeError, ValueError, ValidationError) as e:
                print(e)

    def __run(self) -> None:
        self.__menu.run()

    def run(self) -> None:
        try:
            self.__run()
        except Exception as e:
            print(e)
