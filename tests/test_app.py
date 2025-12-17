import pytest

from app import App
from main import main
from unittest.mock import patch, Mock

from primitives.game_description import GameDescription
from primitives.game_title import GameTitle
from primitives.genre import Genre
from primitives.global_rating import GlobalRating
from primitives.pegi import Pegi
from primitives.token import Token


@patch("builtins.input", side_effect=["0"])
@patch("builtins.print")
def test_app_main(mocked_print, mocked_input):
    main()
    mocked_print.assert_any_call("*** Fiordispino App ***")
    mocked_print.assert_any_call("0:\tExit")
    mocked_print.assert_any_call("Goodbye!")
    mocked_input.assert_called()

@patch("getpass.getpass", side_effect=["string12"])
@patch("requests.post")
@patch("builtins.input", side_effect=["1", "user@gmail.com", "4"])
@patch("builtins.print")
def test_app_login(mocked_print, mocked_input, mocked_post, mocked_getpass):
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"key": "a" * 40}
    mocked_post.return_value = response

    App().run()

    mocked_print.assert_any_call("\nLogged in successfully!")

@patch("getpass.getpass", side_effect=["string12"])
@patch("requests.get")
@patch("requests.post")
@patch("builtins.input", side_effect=["1", "admin@gmail.com", "4"])
@patch("builtins.print")
def test_app_login_as_admin(mocked_print, mocked_input, mocked_post, mocked_get, mocked_getpass):
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"key": "a" * 40}
    mocked_post.return_value = response

    response1 = Mock()
    response1.json.return_value = {"is_superuser": True}
    mocked_get.return_value = response1

    App().run()

    mocked_print.assert_any_call("\nLogged in as admin successfully!")


@patch("getpass.getpass", side_effect=["string12"])
@patch("requests.post")
@patch("builtins.input", side_effect=["1", "user@gmail.com", "0"])
@patch("builtins.print")
def test_app_login_failed_response(mocked_print, mocked_input, mocked_post, mocked_getpass):
    response = Mock()
    response.status_code = 403
    response.text = '{"error": "Invalid credentials"}'
    mocked_post.return_value = response

    App().run()

    assert any("Invalid credentials" in str(call.args[0]) for call in mocked_print.call_args_list)

@patch("getpass.getpass", side_effect=["string12"])
@patch("builtins.input", side_effect=["1", "user@"])
@patch("builtins.print")
def test_app_login_wrong_email(mocked_print, mocked_input, mocked_getpass):
    App().run()

    assert any("There must be something after the @-sign." in str(call.args[0]) for call in mocked_print.call_args_list)


@patch("getpass.getpass", side_effect=["s"])
@patch("builtins.input", side_effect=["1", "user@gmail.com"])
@patch("builtins.print")
def test_app_login_wrong_password_format(mocked_print, mocked_input, mocked_getpass):
    App().run()

    mocked_print.assert_any_call("The password format is not valid, please try again")

@patch("getpass.getpass", side_effect=["string12", "string12"])
@patch("requests.post")
@patch("builtins.input", side_effect=["2", "giovanni", "giovanni@gmail.com", "4"])
@patch("builtins.print")
def test_app_register(mocked_print, mocked_input, mocked_post, mocked_getpass):
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"key": "a" * 40}
    mocked_post.return_value = response

    App().run()

    mocked_print.assert_any_call("\nLogged in successfully!")

@patch("getpass.getpass", side_effect=["password", "password"])
@patch("requests.post")
@patch("builtins.input", side_effect=["2", "giovanni", "giovanni@gmail.com", "0"])
@patch("builtins.print")
def test_app_register_failed_response(mocked_print, mocked_input, mocked_post, mocked_getpass):
    response = Mock()
    response.status_code = 400
    response.text = '{"password": ["This password is too common"]}'
    mocked_post.return_value = response

    App().run()

    assert any("This password is too common" in str(call.args[0]) for call in mocked_print.call_args_list)


@patch("builtins.input", side_effect=["2", "", "giovanni@gmail.com", "0"])
@patch("builtins.print")
def test_app_register_invalid_username(mocked_print, mocked_input):
    App().run()

    mocked_print.assert_any_call("Invalid username: it should have between 1 and 150 characters and can include numbers and special characters in [_@+.-]. Please try again")

@patch("getpass.getpass", side_effect=[""])
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

@patch("builtins.input", side_effect=["3", "0"])
@patch("builtins.print")
@patch("requests.get")
@patch("app.App._App__get_genre", side_effect=[Genre("MMO"), Genre("RPG")])
def test_app_show_games(mock_get_genre, mocked_get, mocked_print, mock_input):
    response = Mock()
    response.json.return_value = [
        {
            "id": 1,
            "title": "GoodGame",
            "description": "A fantastic game",
            "genres": [1, 2],
            "pegi": 3,
            "release_date": "2025-01-01",
            "global_rating": "0.0"
        }
    ]

    mocked_get.return_value = response

    App().run()

    mocked_print.assert_any_call(
        "1     | "
        "GoodGame                       | "
        "A fantastic game                         | "
        "MMO, RPG             | "
        "PEGI 3 | "
        "2025-01-01   | "
        "No votes yet"
    )


@patch("app.requests.get")
def test_app_get_genre(mocked_get):
    response = Mock()
    response.json.return_value = {"name": "Action"}
    mocked_get.return_value = response

    app = App()
    genre = app._App__get_genre(1)
    assert isinstance(genre, Genre)

@patch("builtins.input", side_effect=["4", "0"])
@patch("builtins.print")
@patch("requests.get")
@patch("app.App._App__get_genre", side_effect=[Genre("MMO"), Genre("RPG")])
def test_app_get_genres(mocked_get_genre, mocked_get, mocked_print, mocked_input):
    response = Mock()
    response.json.return_value = [
      {
        "id": 1,
        "name": "MMO"
      },
      {
        "id": 2,
        "name": "RPG"
      }
    ]

    mocked_get.return_value = response

    App().run()

    # retrieve all printed strings
    printed_messages = [call.args[0] for call in mocked_print.call_args_list if call.args]
    assert any("MMO" in msg for msg in printed_messages), "MMO was not printed"
    assert any("RPG" in msg for msg in printed_messages), "RPG was not printed"


@patch("builtins.print")
@patch("requests.get")
@patch("app.App._App__get_game", side_effect=[(
        GameTitle("GoodGame"),
        GameDescription("A fantastic game"),
        [Genre("MMO"), Genre("RPG")],
        Pegi(3),
        "2025-01-01",
        GlobalRating.create(4, 50)
    )])
def test_show_games_to_play(mocked_get_game, mocked_get, mocked_print):
    app = App()
    app._App__token = Token("a" * 40)

    response_games_to_play = Mock()
    response_games_to_play.json.return_value = [
        {
            "id": 10,
            "game": {
                "id": 1,
                "global_rating": "4.5"
            }
        }
    ]


    mocked_get.return_value = response_games_to_play
    ids_global, ids_to_play = app._App__show_games_to_play()

    assert ids_global == [1]
    assert ids_to_play == [10]

    printed_output = "".join([str(call.args[0]) if call.args else "\n" for call in mocked_print.call_args_list])

    assert "GoodGame" in printed_output
    assert "MMO, RPG" in printed_output
    assert "A fantastic game" in printed_output

@patch("app.GlobalRating.create")
@patch("app.requests.get")
@patch("app.App._App__get_genre")
def test_get_game_success(mock_get_genre, mock_requests_get, mock_rating_create):
    mock_get_genre.return_value = Genre("Action")
    mock_rating_create.return_value = "Rated 4.50"

    mock_response = Mock()
    mock_response.json.return_value = {
        "id": 1,
        "title": "Super Game",
        "description": "Description",
        "genres": [1],
        "pegi": 18,
        "release_date": "2023-10-10",
        "global_rating": 4.5
    }
    mock_requests_get.return_value = mock_response

    app = App()
    result = app._App__get_game(1)
    mock_rating_create.assert_called_with(4, 50)

    assert result[5] == "Rated 4.50"

    assert str(result[0]) == "Super Game"


@patch("app.requests.get")
@patch("app.App._App__get_genre")
def test_get_game_no_votes(mock_get_genre, mock_requests_get):
    mock_get_genre.return_value = Genre("Action")

    mock_response = Mock()
    mock_response.json.return_value = {
        "id": 1,
        "title": "New Game",
        "description": "Desc",
        "genres": [1],
        "pegi": 3,
        "release_date": "2024-01-01",
        "global_rating": "0.0"  # Caso 0.0
    }
    mock_requests_get.return_value = mock_response

    app = App()
    result = app._App__get_game(1)

    assert result[5] == "No votes yet"


@patch("app.requests.post")
@patch("builtins.input")
@patch("app.App._App__show_games")
@patch("app.App._App__show_games_to_play")
def test_add_game_to_games_to_play_success(mock_show_to_play, mock_show_games, mock_input, mock_post):
    mock_show_games.return_value = [10, 20]
    mock_show_to_play.return_value = ([], [])

    mock_input.return_value = "2"

    mock_response = Mock()
    mock_response.status_code = 201
    mock_post.return_value = mock_response

    app = App()
    app._App__add_game_to_games_to_play()

    args, kwargs = mock_post.call_args
    assert kwargs['json']['game'] == 20


@patch("app.requests.post")
@patch("builtins.print")
@patch("builtins.input")
@patch("app.App._App__show_games")
@patch("app.App._App__show_games_to_play")
def test_add_game_to_games_to_play_cancel(mock_show_to_play, mock_show_games, mock_input, mock_print, mock_post):
    mock_show_games.return_value = [10, 20, 30]
    mock_show_to_play.return_value = ([], [])

    mock_input.return_value = "0"

    app = App()
    app._App__add_game_to_games_to_play()

    printed_messages = [str(call.args[0]) for call in mock_print.call_args_list if call.args]
    assert "Cancelled!" in printed_messages

    mock_post.assert_not_called()


@patch("app.requests.post")
@patch("builtins.print")
@patch("builtins.input")
@patch("app.App._App__show_games")
@patch("app.App._App__show_games_to_play")
def test_add_game_to_games_to_play_invalid_input_retry(mock_show_to_play, mock_show_games, mock_input, mock_print,
                                                       mock_post):
    mock_show_games.return_value = [10, 20]
    mock_show_to_play.return_value = ([], [])

    mock_input.side_effect = ["5", "1"]

    mock_response = Mock()
    mock_response.status_code = 201
    mock_post.return_value = mock_response

    app = App()
    app._App__add_game_to_games_to_play()

    args, kwargs = mock_post.call_args
    assert kwargs['json']['game'] == 10

    printed_messages = [str(call.args[0]) for call in mock_print.call_args_list if call.args]
    assert any("Game added to games to play!" in msg for msg in printed_messages)


@patch("app.requests.get")
@patch("builtins.print")
@patch("app.App._App__get_game")
def test_show_games_to_play_no_votes(mocked_get_game, mocked_print, mocked_get):
    app = App()
    app._App__token = Token("a" * 40)

    response_list = Mock()
    response_list.json.return_value = [
        {
            "id": 100,
            "game": {
                "id": 1,
                "global_rating": "0.0"
            }
        }
    ]
    mocked_get.return_value = response_list

    mocked_get_game.return_value = (
        GameTitle("Unrated Game"),
        GameDescription("Test description"),
        [Genre("Indie")],
        Pegi(3),
        "2025-01-01",
        "No votes yet"
    )

    app._App__show_games_to_play()

    printed_output = "".join([str(call.args[0]) if call.args else "" for call in mocked_print.call_args_list])

    assert "No votes yet" in printed_output
    assert "Unrated Game" in printed_output


@patch("app.requests.get")
@patch("builtins.print")
@patch("app.App._App__get_genre")
def test_show_games_rating_parsing(mocked_get_genre, mocked_print, mocked_get):
    app = App()

    # rating to forse else branch
    response_mock = Mock()
    response_mock.json.return_value = [
        {
            "id": 1,
            "title": "Rated Game",
            "description": "A game with a rating",
            "genres": [1],
            "pegi": 12,
            "release_date": "2023-10-10",
            "global_rating": "4.5"
        }
    ]
    mocked_get.return_value = response_mock
    mocked_get_genre.return_value = Genre("Action")

    app._App__show_games()

    printed_output = "".join([str(call.args[0]) if call.args else "" for call in mocked_print.call_args_list])

    assert "4.50" in printed_output or "4.5" in printed_output
    assert "Rated Game" in printed_output

@patch("builtins.open")
@patch("app.requests.post")
@patch("builtins.input", side_effect = ["A fantastic game", "GoodGame", "1", "1", "16", "2025", "1", "10"])
@patch("builtins.print")
@patch("app.App._App__show_genres", side_effect=[[1]])
def test_app_add_game_successful(mock_show_genres, mock_print, mock_input, mock_post, mock_open):

    fake_file = Mock()  # A fake file must be inserted in the post
    mock_open.return_value.__enter__.return_value = fake_file

    response = Mock()
    response.status_code = 201
    mock_post.return_value = response

    app = App()
    app._App__add_game()

    mock_print.assert_any_call("Game added successfully!")


@patch("builtins.open")
@patch("app.requests.post")
@patch("builtins.input", side_effect = ["A fantastic game", "GoodGame", "1", "1", "16", "2025", "1", "10"])
@patch("builtins.print")
@patch("app.App._App__show_genres", side_effect=[[1]])
def test_app_add_game_failed_on_wrong_response_code(mocked_show_genres, mocked_print, mocked_input, mocked_post, mocked_open):
    fake_file = Mock() # A fake file must be inserted in the post
    mocked_open.return_value.__enter__.return_value = fake_file

    response = Mock()
    response.status_code = 403
    mocked_post.return_value = response

    app = App()
    app._App__add_game()

    mocked_print.assert_any_call(f"Error: {response.status_code}")

@patch("builtins.open")
@patch("builtins.input", side_effect=["A fantastic game", "GoodGame", "2", "1", "1", "2", "16", "2025", "1", "10"])
@patch("builtins.print")
@patch("app.App._App__show_genres", return_value=[1, 2])
@patch("app.requests.post")
def test_app_add_game_failed_on_genre_already_selected(mocked_post, mocked_show_genres, mocked_print, mocked_input, mocked_open):
    fake_file = Mock()
    mocked_open.return_value.__enter__.return_value = fake_file

    response = Mock()
    response.status_code = 201
    mocked_post.return_value = response

    app = App()
    app._App__token = Token("a" * 40)

    app._App__add_game()

    mocked_print.assert_any_call(
        "Genre already selected. Please choose a different one."
    )


@patch("builtins.open")
@patch("builtins.input", side_effect=["A fantastic game", "GoodGame", "1", "5", "1", "16", "2025", "1", "10"])
@patch("builtins.print")
@patch("app.App._App__show_genres", return_value=[1])
@patch("app.requests.post")
def test_app_add_game_invalid_genre_index(mocked_post, mocked_show_genres, mocked_print, mocked_input, mocked_open):
    fake_file = Mock()
    mocked_open.return_value.__enter__.return_value = fake_file

    response = Mock()
    response.status_code = 201
    mocked_post.return_value = response

    app = App()
    app._App__token = Token("a" * 40)

    app._App__add_game()

    mocked_print.assert_any_call(
        "Invalid index. Please try again"
    )


@patch("builtins.input")
@patch("builtins.print")
@patch("app.App._App__show_genres")
@patch("app.App._App__get_genre")
def test_add_genre_already_exists(mock_get_genre, mock_show_genres, mock_print, mock_input):
    app = App()
    mock_input.return_value = "RPG"
    mock_show_genres.return_value = [1, 2]

    mock_get_genre.side_effect = [Genre("Action"), Genre("RPG")]

    app._App__add_genre()

    printed_messages = [str(call.args[0]) for call in mock_print.call_args_list if call.args]
    assert "Genre already added" in printed_messages


@patch("app.requests.post")
@patch("builtins.input")
@patch("builtins.print")
@patch("app.App._App__show_genres")
@patch("app.App._App__get_genre")
def test_add_genre_success(mock_get_genre, mock_show_genres, mock_print, mock_input, mock_post):
    app = App()
    app._App__token = Token("a" * 40)

    mock_input.return_value = "Strategy"

    mock_show_genres.return_value = [1]
    mock_get_genre.return_value = Genre("Racing")

    mock_post.return_value = Mock(status_code=201)

    app._App__add_genre()

    args, kwargs = mock_post.call_args
    assert kwargs['json']['name'] == "Strategy"

    printed_messages = [str(call.args[0]) for call in mock_print.call_args_list if call.args]
    assert "Genre added successfully!" in printed_messages