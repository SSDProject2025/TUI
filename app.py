from datetime import datetime
import getpass
import json
import sys
import textwrap
from typing import Callable, Any, List, Tuple

import requests
from requests import RequestException
from valid8 import ValidationError, validate

from exceptions.primitives.password_exception import PasswordException
from exceptions.primitives.username_exception import UsernameException
from functionalities.description import Description
from functionalities.entry import Entry
from primitives.email import Email
from primitives.game_description import GameDescription
from primitives.game_title import GameTitle
from primitives.genre import Genre
from primitives.global_rating import GlobalRating
from primitives.password import Password
from primitives.pegi import Pegi
from primitives.token import Token
from primitives.username import Username
from functionalities.menu import Menu
from primitives.vote import Vote


class App:

    __base_url: str = "http://localhost:8000/api/v1"
    __token: Token
    def __init__(self):
        self.__menu = ((Menu.Builder(Description("Fiordispino App"), auto_select=lambda: None).
                       with_entry(Entry.create("1", "Login", on_selected=lambda: self.__login()))).
                       with_entry(Entry.create("2", "Register", on_selected=lambda: self.__register())).
                       with_entry(Entry.create("3", "Show Games", on_selected=lambda: self.__show_games())).
                       with_entry(Entry.create("4", "Show Genres", on_selected=lambda: self.__show_genres())).
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

                response1 = requests.get(
                    f"{self.__base_url}/user/me/",
                    headers={"Authorization": f"Token {response.json().get("key")}"},
                )

                if response1.json().get("is_superuser"):
                    print("\nLogged in as admin successfully!")
                    self.__change_tui_for_logged_admin(response.json().get("key"))
                else:
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

    def __change_tui_for_logged_admin(self, token: str) -> None:
        self.__token = Token(token)

        self.__menu = ((Menu.Builder(Description("Fiordispino App"), auto_select=lambda: None).
                        with_entry(Entry.create("1", "Show Games", on_selected=lambda: self.__show_games())).
                        with_entry(Entry.create("2", "Show Genres", on_selected=lambda: self.__show_genres())).
                        with_entry(Entry.create("3", "Add game", on_selected=lambda: self.__add_game())).
                        with_entry(Entry.create("4", "Add genre", on_selected=lambda: self.__add_genre()))).
                        with_entry(Entry.create("5", "Remove game", on_selected=lambda: self.__remove_game())).
                        with_entry(Entry.create("6", "Remove genre", on_selected=lambda: self.__remove_genre())).
                        with_entry(Entry.create("7", "Ban user", on_selected=lambda: self.__ban_user())).
                        with_entry(Entry.create("8", "Logout", on_selected=lambda: None, is_exit=True)).
                        with_entry(Entry.create("0", "Exit", on_selected=lambda: sys.exit("Goodbye!"), is_exit=True)).
                        build())

        self.run()

    def __change_tui_for_logged_user(self, token: str) -> None:
        self.__token = Token(token)

        self.__menu = ((Menu.Builder(Description("Fiordispino App"), auto_select=lambda: None).
                       with_entry(Entry.create("1", "Show Games", on_selected=lambda: self.__show_games())).
                       with_entry(Entry.create("2", "Show Genres", on_selected=lambda: self.__show_genres())).
                       with_entry(Entry.create("3", "Show games to play", on_selected=lambda: self.__show_games_to_play())).
                       with_entry(Entry.create("4", "Show games played", on_selected=lambda: self.__show_games_played()))).
                       with_entry(Entry.create("5", "Add game to games to play", on_selected=lambda: self.__add_game_to_games_to_play())).
                       with_entry(Entry.create("6", "Add game to games played", on_selected=lambda: self.__add_game_to_games_played())).
                       with_entry(Entry.create("7", "Remove game from games to play", on_selected=lambda: self.__remove_game_from_games_to_play())).
                       with_entry(Entry.create("8", "Remove game from games played", on_selected=lambda: self.__remove_game_from_games_played())).
                       with_entry(Entry.create("9", "Move game from games to play to games played", on_selected= lambda: self.__move_game_from_games_to_play_to_games_played())).
                       with_entry(Entry.create("10", "Logout", on_selected=lambda: None, is_exit=True)).
                       with_entry(Entry.create("0", "Exit", on_selected=lambda: sys.exit("Goodbye!"), is_exit=True)).
                       build())

        self.run()

    def __get_genre(self, id: int) -> 'Genre':
        response = requests.get(f"{self.__base_url}/genre/{id}/")

        return Genre(response.json().get("name"))

    def __show_games(self) -> List[int]:
        response = requests.get(f"{self.__base_url}/game/")

        ids = []

        print(
            f"{'INDEX':5} | {'TITLE':30} | {'DESCRIPTION':40} | {'GENRE':20} | {'PEGI':6} | {'RELEASE DATE':12} | {'VOTE BY USERS':13}")
        print("-" * 157)
        for index, game in enumerate(response.json(), start=1):
            ids.append(game.get("id"))
            title = str(GameTitle(game.get("title")))
            description = str(Description(game.get("description")))
            genres = [self.__get_genre(id) for id in game.get("genres")]
            pegi = str(Pegi(game.get("pegi")))
            release_date = game.get("release_date")

            raw_rating = str(game.get("global_rating"))
            if raw_rating == "0.0":
                global_rating = "No votes yet"
            else:
                integer_str, decimal_str = raw_rating.split(".")
                decimal_str = decimal_str.ljust(2, '0')
                global_rating = GlobalRating.create(int(integer_str), int(decimal_str))

            title_lines = textwrap.wrap(title, 30)
            description_lines = textwrap.wrap(description, 40)

            # Decide which number of line is the longest
            num_lines = max(len(title_lines), len(description_lines))

            for i in range(num_lines):
                idx = str(index) if i == 0 else ""
                t = title_lines[i] if i < len(title_lines) else ""
                d = description_lines[i] if i < len(description_lines) else ""
                g = ', '.join(str(g) for g in genres) if i == 0 else ""
                p = pegi if i == 0 else ""
                r = release_date if i == 0 else ""
                print(f"{idx:5} | {t:30} | {d:40} | {g:20} | {p:6} | {r:12} | {str(global_rating)}")
        print()

        return ids

    def __show_genres(self, with_print=True) -> List[int]:
        genres = []
        response = requests.get(f"{self.__base_url}/genre/")

        if with_print:
            print(f"|\t\tGENRES:\t\t\t|")

        for index, genre in enumerate(response.json(), start=1):
            genres.append(genre.get("id"))
            if with_print:
                print(f"{index}: {Genre(genre.get("name"))}")

        if with_print:
            print()

        return genres

    def __get_game(self, id: int) -> tuple[GameTitle, GameDescription, list[Genre], Pegi, str, GlobalRating]:
        response = requests.get(f"{self.__base_url}/game/{id}/")
        data = response.json()

        raw_rating = str(data.get("global_rating"))

        if raw_rating == "0.0":
            rating_obj = "No votes yet"
        else:
            integer_str, decimal_str = raw_rating.split(".")
            decimal_str = decimal_str.ljust(2, '0')

            rating_obj = GlobalRating.create(int(integer_str), int(decimal_str))

        return (
            GameTitle(data.get("title")),
            GameDescription(data.get("description")),
            [self.__get_genre(g_id) for g_id in data.get("genres")],
            Pegi(data.get("pegi")),
            data.get("release_date"),
            rating_obj
        )

    def __show_games_to_play(self, with_print=True) -> Tuple[list[int], list[int]]:
        response1 = requests.get(
            f"{self.__base_url}/games-to-play/",
            headers={"Authorization": f"Token {str(self.__token)}"}
        )

        ids_global = [] # List that saves the ids of the global game
        ids_to_play = [] # List that saves the ids of the games to play

        if with_print:
            print(
                f"{'INDEX':5} | {'TITLE':30} | {'DESCRIPTION':40} | {'GENRE':20} | {'PEGI':6} | {'RELEASE DATE':12} | {'VOTE BY USERS':13}"
            )
            print("-" * 157)

        for index, item in enumerate(response1.json(), start=1):
            ids_global.append(item.get("game").get("id"))
            ids_to_play.append(item.get("id"))
            game_id = item["game"]["id"]
            title, description, genres, pegi, release_date, global_rating = self.__get_game(game_id)

            title_str = str(title)
            description_str = str(description)
            genres_str = ', '.join(str(g) for g in genres)
            pegi_str = str(pegi)

            # Gestione voto
            raw_rating = str(item["game"].get("global_rating", "0.0"))
            if raw_rating == "0.0":
                vote_display = "No votes yet"
            else:
                integer_str, decimal_str = raw_rating.split(".")
                decimal_str = decimal_str.ljust(2, "0")
                vote_display = GlobalRating.create(int(integer_str), int(decimal_str))

            title_lines = textwrap.wrap(title_str, 30)
            description_lines = textwrap.wrap(description_str, 40)
            num_lines = max(len(title_lines), len(description_lines))

            for i in range(num_lines):
                if with_print:
                    print(
                        f"{str(index) if i == 0 else '':5} | "
                        f"{title_lines[i] if i < len(title_lines) else '':30} | "
                        f"{description_lines[i] if i < len(description_lines) else '':40} | "
                        f"{genres_str if i == 0 else '':20} | "
                        f"{pegi_str if i == 0 else '':6} | "
                        f"{release_date if i == 0 else '':12} | "
                        f"{str(vote_display) if i == 0 else ''}"
                    )

        if with_print:
            print()

        return (ids_global, ids_to_play)

    def __show_games_played(self, with_print=True) -> Tuple[list[int], list[int]]:
        response = requests.get(
            f"{self.__base_url}/games-played/",
            headers={"Authorization": f"Token {str(self.__token)}"}
        )

        ids_global = []  # List that saves the ids of the global game
        ids_played = []  # List that saves the ids of the games played

        if with_print:
            print(
                f"{'INDEX':5} | {'TITLE':30} | {'DESCRIPTION':40} | "
                f"{'GENRE':20} | {'PEGI':6} | {'RELEASE DATE':12} | {'VOTE GIVEN':13}"
            )
            print("-" * 157)

        for index, item in enumerate(response.json(), start=1):
            ids_global.append(item.get("game").get("id"))
            ids_played.append(item.get("id"))

            game = item["game"]

            title = GameTitle(game["title"])
            description = GameDescription(game["description"])
            genres = [self.__get_genre(g) for g in game["genres"]]
            pegi = Pegi(game["pegi"])
            release_date = game["release_date"]

            vote = Vote(item["rating"])

            title_str = str(title)
            description_str = str(description)
            g = ', '.join(str(gen) for gen in genres)
            pegi_str = str(pegi)
            vote_str = str(vote)

            title_lines = textwrap.wrap(title_str, 30)
            description_lines = textwrap.wrap(description_str, 40)
            num_lines = max(len(title_lines), len(description_lines))

            if with_print:
                for i in range(num_lines):
                    print(
                        f"{str(index) if i == 0 else '':5} | "
                        f"{title_lines[i] if i < len(title_lines) else '':30} | "
                        f"{description_lines[i] if i < len(description_lines) else '':40} | "
                        f"{g if i == 0 else '':20} | "
                        f"{pegi_str if i == 0 else '':6} | "
                        f"{release_date if i == 0 else '':12} | "
                        f"{vote_str if i == 0 else ''}"
                    )

        if with_print:
            print()
        return (ids_global, ids_played)

    def __add_game(self):
        def builder_year(value: str) -> int:
            validate("value", int(value), min_value=1952, max_value=datetime.now().year)
            return int(value)

        def builder_month(value: str) -> int:
            validate("value", int(value), min_value=1, max_value=12)
            return int(value)

        def builder_day(value: str) -> int:
            validate("value", int(value), min_value=1, max_value=31)
            return int(value)

        def builder_number_of_genres(value: str) -> int:
            validate('value', int(value), min_value=1, max_value=5)
            return int(value)

        def builder_pegi(value: str) -> 'Pegi':
            validate("pegi_ranking_int", int(value), is_in=[3, 7, 12, 16, 18])
            return Pegi(int(value))

        description = self.__read("Description", GameDescription)
        title = self.__read("Title", GameTitle)
        genres_number = self.__read("Number of genres", builder_number_of_genres)
        genres_to_choose = self.__show_genres()
        genres = []

        for i in range(genres_number):
            while True:
                try:
                    index = int(input(f"Index {i + 1}: "))
                    validate("index", index, min_value=1, max_value=len(genres_to_choose))

                    selected_genre = genres_to_choose[index - 1]
                    if selected_genre not in genres:
                        genres.append(selected_genre)
                        break
                    else:
                        print("Genre already selected. Please choose a different one.")
                except ValidationError:
                    print("Invalid index. Please try again")

        pegi = self.__read("Pegi", builder_pegi)

        year = self.__read("Release year", builder_year)
        month = self.__read("Release month", builder_month)
        day = self.__read("Release day", builder_day)

        data = {
            "description": str(description),
            "title": str(title),
            "pegi": pegi.pegi_ranking_int,
            "release_date": f"{year}-{month:02d}-{day:02d}",
            "genres": genres
        }

        # Adding a default image otherwise the backend gets angry
        with open("placeholder_images/useful_formula.png", 'rb') as img_file:
            files = {
                'box_art': img_file
            }

            response = requests.post(
                f"{self.__base_url}/game/",
                data=data,
                files=files,
                headers={"Authorization": f"Token {str(self.__token)}"}
            )

        if response.status_code in [200, 201]:
            print("Game added successfully!")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    def __add_genre(self):
        genre_to_add = self.__read("Genre", Genre)

        genres = self.__show_genres(with_print=False)

        for id in genres:
            if str(self.__get_genre(id)).lower() == str(genre_to_add).lower():
                print("Genre already added")
                return

        response = requests.post(
            f"{self.__base_url}/genre/",
            json={
                "name": str(genre_to_add),
            },
            headers={"Authorization": f"Token {str(self.__token)}"}
        )

        print("Genre added successfully!")

    def __remove_game(self):
        ids = self.__show_games()

        def builder(value: str) -> int:
            validate("value", int(value), min_value=0, max_value=len(ids))
            return int(value)

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!')
            return

        response = requests.delete(
            f"{self.__base_url}/game/{ids[index - 1]}/",
            headers={"Authorization": f"Token {str(self.__token)}"},
        )

        print("Game removed successfully!")

    def __remove_genre(self):
        ids = self.__show_genres()

        def builder(value: str) -> int:
            validate("value", int(value), min_value=0, max_value=len(ids))
            return int(value)

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!')
            return

        response = requests.delete(
            f"{self.__base_url}/genre/{ids[index - 1]}/",
            headers={"Authorization": f"Token {str(self.__token)}"},
        )

        print("Genre removed successfully!")

    def __ban_user(self):
        response = requests.get(
            f"{self.__base_url}/user/",
            headers={"Authorization": f"Token {str(self.__token)}"}
        )

        print(f"{'USER':30} | {'EMAIL':50} |")
        print("-" * 100)

        users_id = []

        for index, user in enumerate(response.json(), start=1):
            users_id.append(user.get("id"))
            username = Username(user.get('username'))
            email = Email(user.get('email'))

            username_str = str(username)
            email_str = str(email)

            username_lines = textwrap.wrap(username_str, 30)
            email_lines = textwrap.wrap(email_str, 50)
            num_lines = max(len(username_lines), len(email_lines))

            for i in range(num_lines):
                print(
                    f"{str(index) if i == 0 else '':5} | "
                    f"{username_lines[i] if i < len(username_lines) else '':30} | "
                    f"{email_lines[i] if i < len(email_lines) else ''}"
                )

        def builder(value: str) -> int:
            validate("value", int(value), min_value=0, max_value=len(users_id))
            return int(value)

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!')
            return

        response = requests.delete(
            f"{self.__base_url}/user/{users_id[index - 1]}/",
            headers={"Authorization": f"Token {str(self.__token)}"},
        )

        print("User banned successfully!")

    def __add_game_to_games_to_play(self) -> None:
        ids = self.__show_games()
        ids_global, ids_to_play = self.__show_games_to_play(with_print=False)

        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=len(ids))
            return int(value)

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!')
            return
        elif ids[index - 1] in ids_global:
            print('Game already in list')
            return

        response = requests.post(
            f"{self.__base_url}/games-to-play/",
            json={
                "game": ids[index - 1],
            },
            headers={"Authorization": f"Token {str(self.__token)}"},
        )

        print("Game added to games to play!")

    def __add_game_to_games_played(self) -> None:
        ids = self.__show_games()
        ids_global, ids_played = self.__show_games_played(with_print=False)

        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=len(ids))
            return int(value)

        def vote_builder(value: str) -> 'Vote':
            return Vote(int(value))

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!')
            return
        elif ids[index - 1] in ids_global:
            print('Game already in list')
            return

        vote = self.__read('Vote', vote_builder)

        response = requests.post(
            f"{self.__base_url}/games-played/",
            json={
                "game": ids[index - 1],
                "rating": vote.vote,
            },
            headers={"Authorization": f"Token {str(self.__token)}"},
        )

        print("Game added to games played!")

    def __remove_game_from_games_to_play(self) -> None:
        ids_global, ids_to_play = self.__show_games_to_play()

        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=len(ids_to_play))
            return int(value)

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!')
            return

        response = requests.delete(
            f"{self.__base_url}/games-to-play/{ids_to_play[index - 1]}/",
            headers={"Authorization": f"Token {str(self.__token)}"},
        )

        print("Game removed from games to play!")

    def __remove_game_from_games_played(self) -> None:
        ids_global, ids_played = self.__show_games_played()

        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=len(ids_played))
            return int(value)

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!')
            return

        response = requests.delete(
            f"{self.__base_url}/games-played/{ids_played[index - 1]}/",
            headers={"Authorization": f"Token {str(self.__token)}"},
        )

        print("Game removed from games played")

    def __move_game_from_games_to_play_to_games_played(self) -> None:
        ids_global, ids_to_play = self.__show_games_to_play()

        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=len(ids_to_play))
            return int(value)

        def vote_builder(value: str) -> 'Vote':
            return Vote(int(value))

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!')
            return

        response = requests.delete(
            f"{self.__base_url}/games-to-play/{ids_to_play[index - 1]}/",
            headers={"Authorization": f"Token {str(self.__token)}"},
        )

        vote = self.__read('Vote', vote_builder)

        response = requests.post(
            f"{self.__base_url}/games-played/",
            json={
                "game": ids_global[index - 1],
                "rating": vote.vote,
            },
            headers={"Authorization": f"Token {str(self.__token)}"},
        )

        print("Game moved to games played!")

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
