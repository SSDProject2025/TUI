import pytest
from valid8 import ValidationError

from app import App
from exceptions.primitives.game_title_exception import GameTitleException
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

@patch("builtins.input", side_effect=["1", "user@gmail.com"])
@patch("getpass.getpass", side_effect=["string12"])
@patch("requests.get")
@patch("requests.post")
@patch("builtins.print")
def test_app_login(mocked_print, mocked_post, mocked_get, mocked_getpass, mocked_input):
    login_response = Mock()
    login_response.status_code = 200
    login_response.json.return_value = {"key": "a" * 40}
    mocked_post.return_value = login_response

    me_response = Mock()
    me_response.json.return_value = {"is_superuser": False}
    mocked_get.return_value = me_response

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
            "genres": [{"name":"MMO"},{"name": "RPG"}],
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
def test_show_games_to_play(mocked_get, mocked_print):
    app = App()
    app._App__token = Token("a" * 40)

    response_games_to_play = Mock()
    response_games_to_play.json.return_value = [
        {
            "id": 10,
            "game":         {
            "id": 1,
            "title": "GoodGame",
            "description": "A fantastic game",
            "genres": [{"name":"MMO"},{"name": "RPG"}],
            "pegi": 3,
            "release_date": "2025-01-01",
            "global_rating": "0.0"
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
def test_show_games_to_play_no_votes(mocked_print, mocked_get):
    app = App()
    app._App__token = Token("a" * 40)

    response_list = Mock()
    response_list.json.return_value = [
        {
            "id": 100,
            "game": {
                "id": 1,
                "title": "GoodGame",
                "description": "A fantastic game",
                "genres": [{"name":"MMO"},{"name": "RPG"}],
                "pegi": 3,
                "release_date": "2025-01-01",
                "global_rating": "0.0"
            }
        }
    ]
    mocked_get.return_value = response_list

    app._App__show_games_to_play()

    printed_output = "".join([str(call.args[0]) if call.args else "" for call in mocked_print.call_args_list])

    assert "No votes yet" in printed_output


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
            "genres": [{"name": "MMO"}, {"name": "RPG"}],
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
@patch("app.App._App__show_genres", side_effect=[[1, 2]])
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

    mocked_print.assert_any_call("Genre already selected. Please choose a different one.")


@patch("builtins.open")
@patch("builtins.input", side_effect=["A fantastic game", "GoodGame", "1", "5", "1", "16", "2025", "1", "10"])
@patch("builtins.print")
@patch("app.App._App__show_genres", side_effect=[[1]])
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

    mocked_print.assert_any_call("Invalid index. Please try again")


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

@patch("builtins.print")
@patch("builtins.input", side_effect=["1"])
@patch("requests.delete")
@patch("app.App._App__show_games_to_play", side_effect=[([10], [1])])
def test_remove_game_from_games_to_play_success(mocked_show_games_to_play, mocked_delete, mocked_input, mocked_print):

    response = Mock()
    response.status_code = 204
    mocked_delete.return_value = response

    app = App()
    app._App__remove_game_from_games_to_play()


    mocked_print.assert_any_call("Game removed from games to play!")


@patch("builtins.print")
@patch("builtins.input", side_effect=["0"])
@patch("requests.delete")
@patch("app.App._App__show_games_to_play", side_effect=[([10], [1])])
def test_remove_game_from_games_to_play_cancelled(mocked_show_games_to_play, mocked_delete, mocked_input, mocked_print):

    response = Mock()
    response.status_code = 204
    mocked_delete.return_value = response

    app = App()
    app._App__remove_game_from_games_to_play()


    mocked_print.assert_any_call("Cancelled!")

@patch("builtins.print")
@patch("builtins.input", side_effect=["1"])
@patch("requests.delete")
@patch("app.App._App__show_games_played", side_effect=[([10], [1])])
def test_remove_game_from_games_played_success(mocked_show_games_played, mocked_delete, mocked_input, mocked_print):
    response = Mock()
    response.status_code = 204
    mocked_delete.return_value = response

    app = App()
    app._App__remove_game_from_games_played()

    mocked_print.assert_any_call("Game removed from games played")

@patch("builtins.print")
@patch("builtins.input", side_effect=["0"])
@patch("requests.delete")
@patch("app.App._App__show_games_played", side_effect=[([10], [1])])
def test_remove_game_from_games_played_cancelled(mocked_show_games_played, mocked_delete, mocked_input, mocked_print):
    response = Mock()
    response.status_code = 204
    mocked_delete.return_value = response

    app = App()
    app._App__remove_game_from_games_played()

    mocked_print.assert_any_call("Cancelled!")

@patch("builtins.print")
@patch("builtins.input", side_effect=["1"])
@patch("requests.post")
@patch("app.App._App__show_games", return_value=[1, 2, 3])
@patch("app.App._App__show_games_to_play", return_value=([1], [1]))
def test_add_game_to_games_to_play_already_in_list(mocked_show_games_to_play, mocked_show_games, mocked_post, mocked_input, mocked_print):
    app = App()

    app._App__add_game_to_games_to_play()

    mocked_print.assert_any_call("Game already in list")

@patch("builtins.print")
@patch("builtins.input", side_effect=["1", "5"])
@patch("requests.delete")
@patch("requests.post")
@patch("app.App._App__show_games_to_play", return_value=([10], [1]))
def test_move_game_from_games_to_play_to_games_played_success(mocked_show_games_to_play, mocked_post, mocked_delete, mocked_input, mocked_print):
    delete_response = Mock()
    delete_response.status_code = 204
    mocked_delete.return_value = delete_response

    post_response = Mock()
    post_response.status_code = 201
    mocked_post.return_value = post_response

    app = App()
    app._App__move_game_from_games_to_play_to_games_played()

    mocked_print.assert_any_call("Game moved to games played!")

@patch("builtins.print")
@patch("builtins.input", side_effect=["0"])
@patch("app.App._App__show_games_to_play", return_value=([10], [1]))
def test_move_game_from_games_to_play_to_games_played_game_cancelled(mocked_show_games_to_play, mocked_input, mocked_print):
    app = App()

    app._App__move_game_from_games_to_play_to_games_played()

    mocked_print.assert_any_call("Cancelled!")


@patch("app.requests.get")
@patch("builtins.print")
@patch("app.App._App__get_genre")
def test_show_games_played(mocked_get_genre, mocked_print, mocked_get):
    app = App()
    app._App__token = Token("a" * 40)



    response_mock = Mock()
    response_mock.json.return_value = [
        {
            "id": 500,
            "rating": 5,
            "game": {
                "id": 1,
                "title": "Played Masterpiece",
                "description": "A game I have finished",
                "genres": [{"name": "MMO"}, {"name": "RPG"}],
                "pegi": 18,
                "release_date": "2024-05-20"
            }
        }
    ]
    mocked_get.return_value = response_mock

    mocked_get_genre.return_value = Genre("RPG")

    ids_global, ids_played = app._App__show_games_played()

    assert ids_global == [1]
    assert ids_played == [500]

    printed_output = "".join([str(call.args[0]) if call.args else "\n" for call in mocked_print.call_args_list])

    assert "Played Masterpiece" in printed_output
    assert "RPG" in printed_output
    assert "5" in printed_output


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


@patch("app.requests.post")
@patch("builtins.print")
@patch("builtins.input")
@patch("app.App._App__show_games")
@patch("app.App._App__show_games_to_play")
def test_add_game_to_games_to_play_already_in_list(mock_show_to_play, mock_show_games, mock_input, mock_print,
                                                   mock_post):
    app = App()
    mock_show_games.return_value = [10, 20]

    mock_show_to_play.return_value = ([20], [1])
    mock_input.return_value = "2"

    app._App__add_game_to_games_to_play()

    printed_messages = [str(call.args[0]) for call in mock_print.call_args_list if call.args]
    assert "Game already in list" in printed_messages
    mock_post.assert_not_called()


@patch("getpass.getpass")
@patch("builtins.print")
def test_read_password_error(mock_print, mock_getpass):
    mock_builder = Mock()
    mock_builder.side_effect = [ValueError("invalid password"), "valid_password123"]

    mock_getpass.side_effect = ["input1", "input2"]

    result = App._App__read_password("Password", mock_builder)
    printed_messages = [str(call.args[0]) for call in mock_print.call_args_list if call.args]
    assert "invalid password" in printed_messages

    assert result == "valid_password123"


@patch("builtins.input")
@patch("builtins.print")
def test_read_custom_exception(mock_print, mock_input):
    mock_builder = Mock()
    custom_error = GameTitleException()
    custom_error.help_message = "Invalid title" # first attempt fails

    mock_builder.side_effect = [custom_error, "valid title"] # first attempt ok -> exit loop

    mock_input.side_effect = ["invalid", "valid"]

    result = App._App__read("insert title", mock_builder)

    printed_messages = [str(call.args[0]) for call in mock_print.call_args_list if call.args]

    assert "Invalid title" in printed_messages

    assert result == "valid title"


@patch("app.requests.delete")
@patch("builtins.print")
@patch("builtins.input")
@patch("app.App._App__show_games")
def test_remove_game_success(mock_show_games, mock_input, mock_print, mock_delete):
    app = App()
    app._App__token = Token("a" * 40)

    mock_show_games.return_value = [10, 20, 30]
    mock_input.return_value = "2"

    mock_delete.return_value = Mock(status_code=204)

    app._App__remove_game()

    # Verify DELETE call was made to the correct URL with correct ID
    args, kwargs = mock_delete.call_args
    assert "/game/20/" in args[0]

    # Verify success message
    printed_messages = [str(call.args[0]) for call in mock_print.call_args_list if call.args]
    assert "Game removed successfully!" in printed_messages


@patch("app.requests.delete")
@patch("builtins.print")
@patch("builtins.input")
@patch("app.App._App__show_games")
def test_remove_game_cancel(mock_show_games, mock_input, mock_print, mock_delete):
    app = App()
    mock_show_games.return_value = [10, 20]
    mock_input.return_value = "0"

    app._App__remove_game()

    printed_messages = [str(call.args[0]) for call in mock_print.call_args_list if call.args]
    assert "Cancelled!" in printed_messages

    mock_delete.assert_not_called()


@patch("app.requests.delete")
@patch("builtins.print")
@patch("builtins.input")
@patch("app.App._App__show_games")
def test_remove_game_cancel(mock_show_games, mock_input, mock_print, mock_delete):
    app = App()

    mock_show_games.return_value = [10, 20]
    mock_input.return_value = "0"

    app._App__remove_game()

    # Verify cancellation message
    printed_messages = [str(call.args[0]) for call in mock_print.call_args_list if call.args]
    assert "Cancelled!" in printed_messages

    mock_delete.assert_not_called()


@patch("app.requests.delete")
@patch("builtins.print")
@patch("builtins.input")
@patch("app.App._App__show_genres")
def test_remove_genre_success(mock_show_genres, mock_input, mock_print, mock_delete):
    app = App()
    app._App__token = Token("a" * 40)

    mock_show_genres.return_value = [5, 9]
    mock_input.return_value = "2"

    mock_delete.return_value = Mock(status_code=204)

    app._App__remove_genre()

    args, kwargs = mock_delete.call_args
    assert "/genre/9/" in args[0]
    assert kwargs['headers']['Authorization'] == f"Token {str(app._App__token)}"

    printed_messages = [str(call.args[0]) for call in mock_print.call_args_list if call.args]
    assert "Genre removed successfully!" in printed_messages


@patch("app.requests.delete")
@patch("builtins.print")
@patch("builtins.input")
@patch("app.App._App__show_genres")
def test_remove_genre_cancel(mock_show_genres, mock_input, mock_print, mock_delete):
    app = App()

    mock_show_genres.return_value = [5, 9]
    mock_input.return_value = "0"

    app._App__remove_genre()

    printed_messages = [str(call.args[0]) for call in mock_print.call_args_list if call.args]
    assert "Cancelled!" in printed_messages

    mock_delete.assert_not_called()


@patch("app.requests.get")
@patch("app.requests.delete")
@patch("builtins.print")
@patch("builtins.input")
def test_ban_user_success(mock_input, mock_print, mock_delete, mock_get):
    app = App()
    app._App__token = Token("a" * 40)

    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.json.return_value = [
        {
            "id": 101,
            "username": "nameuser",
            "email": "nameuser.very.long.email.address@gmail.com"
        },
        {
            "id": 102,
            "username": "admin",
            "email": "admin@gmail.com"
        }
    ]

    mock_input.return_value = "1"
    mock_delete.return_value = Mock(status_code=204)

    app._App__ban_user()

    args, _ = mock_delete.call_args
    assert "/user/101/" in args[0]

    printed_output = "".join([str(call.args[0]) for call in mock_print.call_args_list if call.args])
    assert "User banned successfully!" in printed_output


@patch("app.requests.get")
@patch("app.requests.delete")
@patch("builtins.print")
@patch("builtins.input")
def test_ban_user_cancel(mock_input, mock_print, mock_delete, mock_get):
    app = App()

    # 1. Mock the user list
    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.json.return_value = [{"id": 101, "username": "test", "email": "test@gmail.com"}]

    # 2. User enters "0" to cancel the operation
    mock_input.return_value = "0"

    app._App__ban_user()

    # Verify "Cancelled!" message
    printed_output = "".join([str(call.args[0]) for call in mock_print.call_args_list if call.args])
    assert "Cancelled!" in printed_output

    mock_delete.assert_not_called()


@patch("app.requests.post")
@patch("builtins.print")
@patch("builtins.input")
@patch("app.App._App__show_games")
@patch("app.App._App__show_games_played")
def test_add_game_to_games_played_success(mock_show_played, mock_show_games, mock_input, mock_print, mock_post):
    app = App()
    app._App__token = Token("a" * 40)

    # 1. Setup available games (ID 10, 20) and empty played list
    mock_show_games.return_value = [10, 20]
    mock_show_played.return_value = ([], [])  # (ids_global, ids_played)

    # 2. Mock user input: "2" (for game ID 20) and then "5" (for the Vote)
    mock_input.side_effect = ["2", "5"]

    # 3. Mock successful POST response
    mock_post.return_value = Mock(status_code=201)

    # Execution
    app._App__add_game_to_games_played()

    # Verify POST request contains both the game ID and the rating
    args, kwargs = mock_post.call_args
    assert kwargs['json']['game'] == 20
    assert kwargs['json']['rating'] == 5

    # Verify success message
    printed_output = "".join([str(call.args[0]) for call in mock_print.call_args_list if call.args])
    assert "Game added to games played!" in printed_output


@patch("app.requests.post")
@patch("builtins.print")
@patch("builtins.input")
@patch("app.App._App__show_games")
@patch("app.App._App__show_games_played")
def test_add_game_to_games_played_already_exists(mock_show_played, mock_show_games, mock_input, mock_print, mock_post):
    app = App()

    # 1. Setup games: ID 10 is already in the played list
    mock_show_games.return_value = [10, 20]
    mock_show_played.return_value = ([10], [500])  # ID 10 is already played

    # 2. User selects index "1" (ID 10)
    mock_input.return_value = "1"

    # Execution
    app._App__add_game_to_games_played()

    # Verify duplicate message and ensure no POST was made
    printed_output = "".join([str(call.args[0]) for call in mock_print.call_args_list if call.args])
    assert "Game already in list" in printed_output
    mock_post.assert_not_called()


@patch("app.requests.post")
@patch("builtins.print")
@patch("builtins.input")
@patch("app.App._App__show_games")
@patch("app.App._App__show_games_played")
def test_add_game_to_games_played_cancel(mock_show_played, mock_show_games, mock_input, mock_print, mock_post):
    app = App()

    # 1. Setup games
    mock_show_games.return_value = [10, 20]
    mock_show_played.return_value = ([], [])

    # 2. User enters "0" to cancel
    mock_input.return_value = "0"

    # Execution
    app._App__add_game_to_games_played()

    # Verify cancellation
    printed_output = "".join([str(call.args[0]) for call in mock_print.call_args_list if call.args])
    assert "Cancelled!" in printed_output
    mock_post.assert_not_called()

@patch("builtins.input", side_effect=["0"])
@patch("builtins.print")
@patch("requests.get")
@patch("app.GlobalRating.create", side_effect=["7.50"])
def test_app_show_games_to_play_with_vote(mocked_create, mocked_get, mocked_print, mock_input):
    response = Mock()
    response.json.return_value = [
        {
            "id": 10,
            "game": {
                "id": 1,
                "title": "RatedGame",
                "description": "A rated game",
                "genres": [{"name": "Action"}, {"name": "RPG"}],
                "pegi": 18,
                "release_date": "2025-05-01",
                "global_rating": "7.5"
            }
        }
    ]

    mocked_get.return_value = response

    app = App()
    app._App__show_games_to_play()


    mocked_print.assert_any_call(
        "1     | "
        "RatedGame                      | "
        "A rated game                             | "
        "Action, RPG          | "
        "PEGI 18 | "
        "2025-05-01   | "
        "7.50"
    )

@patch("builtins.input", side_effect=["testuser"])
@patch("builtins.print")
@patch("requests.get")
@patch("app.GlobalRating.create", side_effect=["6.20"])
def test_show_games_to_play_given_user(mocked_create, mocked_get, mocked_print, mocked_input):
    response = Mock()
    response.json.return_value = [
        {
            "id": 50,
            "game": {
                "id": 1,
                "title": "UserGame",
                "description": "Game for user",
                "genres": [{"name": "MMO"}, {"name": "RPG"}],
                "pegi": 16,
                "release_date": "2025-03-01",
                "global_rating": "6.2"
            }
        }
    ]

    mocked_get.return_value = response

    app = App()
    app._App__show_games_to_play_given_user()

    mocked_print.assert_any_call("GAMES TO PLAY BY testuser")
    mocked_print.assert_any_call(
        f"{'1':<5} | "
        f"{'UserGame':<30} | "
        f"{'Game for user':<40} | "
        f"{'MMO, RPG':<20} | "
        f"{'PEGI 16':<6} | "
        f"{'2025-03-01':<12} | "
        f"6.20"
    )

@patch("builtins.input", side_effect=["testuser"])
@patch("builtins.print")
@patch("requests.get")
@patch("app.GlobalRating.create", side_effect=["6.20"])
def test_show_games_to_play_given_user_no_votes(mocked_create, mocked_get, mocked_print, mocked_input):
    response = Mock()
    response.json.return_value = [
        {
            "id": 50,
            "game": {
                "id": 1,
                "title": "UserGame",
                "description": "Game for user",
                "genres": [{"name": "MMO"}, {"name": "RPG"}],
                "pegi": 16,
                "release_date": "2025-03-01",
                "global_rating": "0.0"
            }
        }
    ]

    mocked_get.return_value = response

    app = App()
    app._App__show_games_to_play_given_user()

    mocked_print.assert_any_call(
        f"{'1':<5} | "
        f"{'UserGame':<30} | "
        f"{'Game for user':<40} | "
        f"{'MMO, RPG':<20} | "
        f"{'PEGI 16':<6} | "
        f"{'2025-03-01':<12} | "
        "No votes yet"
    )

@patch("builtins.input", side_effect=["testuser"])
@patch("builtins.print")
@patch("requests.get")
@patch("app.GlobalRating.create", side_effect=["6.20"])
def test_show_games_to_play_given_user_no_games_for_user(mocked_create, mocked_get, mocked_print, mocked_input):
    response = Mock()
    response.json.return_value = []

    mocked_get.return_value = response

    app = App()
    app._App__show_games_to_play_given_user()

    mocked_print.assert_any_call("No games for user testuser")


@patch("builtins.input", side_effect=["testuser"])
@patch("builtins.print")
@patch("requests.get")
def test_show_games_played_given_user(mocked_get, mocked_print, mocked_input):
    response = Mock()
    response.json.return_value = [
        {
            "id": 50,
            "game": {
                "id": 1,
                "title": "UserGame",
                "description": "Game for user",
                "genres": [{"name": "MMO"}, {"name": "RPG"}],
                "pegi": 16,
                "release_date": "2025-03-01",
            },
            "rating": 6
        }
    ]

    mocked_get.return_value = response

    app = App()
    app._App__token = Token("a" * 40)
    app._App__show_games_played_given_user()

    # Controlla intestazione
    mocked_print.assert_any_call("GAMES PLAYED BY testuser")

    # Controlla riga del gioco (spazi coerenti con il codice)
    mocked_print.assert_any_call(
        f"{'1':<5} | "
        f"{'UserGame':<30} | "
        f"{'Game for user':<40} | "
        f"{'MMO, RPG':<20} | "
        f"{'PEGI 16':<6} | "
        f"{'2025-03-01':<12} | "
        f"6"
    )


@patch("builtins.input", side_effect=["testuser"])
@patch("builtins.print")
@patch("requests.get")
def test_show_games_played_given_user_no_games_for_user(mocked_get, mocked_print, mocked_input):
    response = Mock()
    response.json.return_value = []
    mocked_get.return_value = response

    app = App()
    app._App__show_games_played_given_user()

    mocked_print.assert_any_call("No games for user testuser")


@patch("app.requests.get")
@patch("builtins.print")
def test_show_games_handles_invalid_primitive_data_and_continues(mocked_print, mocked_get):
    """
    Test that __show_games handles invalid primitive data (e.g., wrong PEGI)
    without crashing, printing an error message instead.
    """
    app = App()

    # Mocking response: 1st is valid, 2nd has invalid PEGI (99), 3rd is valid
    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.json.return_value = [
        {
            "id": 1,
            "title": "Valid Game 1",
            "description": "Desc",
            "genres": [{"name": "Action"}],
            "pegi": 12,
            "release_date": "2023-01-01",
            "global_rating": 8.5
        },
        {
            "id": 2,
            "title": "Invalid Game",
            "description": "Fails because of PEGI",
            "genres": [{"name": "Action"}],
            "pegi": 99,  # This will raise PegiRankingException
            "release_date": "2023-01-01",
            "global_rating": 5.0
        },
        {
            "id": 3,
            "title": "Valid Game 2",
            "description": "Desc",
            "genres": [{"name": "RPG"}],
            "pegi": 18,
            "release_date": "2023-05-05",
            "global_rating": 9.0
        }
    ]
    mocked_get.return_value = response_mock

    # Execution
    ids = app._App__show_games()

    # Verify that IDs 1 and 3 are returned, but 2 is skipped
    assert 1 in ids
    assert 3 in ids
    assert 2 not in ids

    # Check for the printed error message in the logs
    printed_messages = [str(call.args[0]) for call in mocked_print.call_args_list if call.args]
    assert any("ERROR: Game ID 2 has invalid data" in msg for msg in printed_messages)
    assert any("Valid Game 1" in msg for msg in printed_messages)
    assert any("Valid Game 2" in msg for msg in printed_messages)


@patch("app.requests.get")
@patch("builtins.print")
def test_show_games_handles_invalid_genre_structure_and_continues(mocked_print, mocked_get):
    """
    Test that __show_games handles a genre that is not a dictionary
    without crashing (checks the isinstance(g, dict) logic).
    """
    app = App()

    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.json.return_value = [
        {
            "id": 1,
            "title": "Broken Genre Game",
            "description": "Genre list contains an int instead of dict",
            "genres": [1],  # Error: Should be {"name": "..."}
            "pegi": 3,
            "release_date": "2023-01-01",
            "global_rating": "0.0"
        },
        {
            "id": 2,
            "title": "Valid Game After",
            "description": "Desc",
            "genres": [{"name": "Action"}],
            "pegi": 12,
            "release_date": "2023-01-01",
            "global_rating": "0.0"
        }
    ]
    mocked_get.return_value = response_mock

    # Execution
    ids = app._App__show_games()

    # The game with broken genre might still print (with empty genres)
    # depending on your exact internal logic in the loop,
    # but the key is that it MUST NOT crash and should process Game ID 2.
    assert 2 in ids

    printed_messages = [str(call.args[0]) for call in mocked_print.call_args_list if call.args]
    assert any("Valid Game After" in msg for msg in printed_messages)


@patch("app.requests.get")
@patch("app.App._App__get_genre")
def test_get_game_genres_as_dicts(mock_get_genre, mock_requests_get):
    """
    Test that __get_game correctly handles genres when they are
    returned as dictionaries (objects) instead of simple integers.
    This touches the line: if isinstance(g, dict): g_id = g.get('id')
    """
    app = App()

    # Mock della risposta di __get_genre per restituire un oggetto Genre valido
    mock_get_genre.return_value = Genre("RPG")

    # Simuliamo una risposta dove 'genres' è una lista di dizionari
    mock_response = Mock()
    mock_response.json.return_value = {
        "id": 1,
        "title": "Nested Genre Game",
        "description": "A game where genres are objects",
        "genres": [{"id": 10, "name": "RPG"}],  # <--- Qui g è un dict
        "pegi": 12,
        "release_date": "2024-12-18",
        "global_rating": "8.5"
    }
    mock_requests_get.return_value = mock_response

    # Esecuzione del metodo privato
    result = app._App__get_game(1)

    # Verifiche
    # 1. Controlliamo che __get_genre sia stato chiamato con l'ID estratto dal dizionario (10)
    mock_get_genre.assert_called_with(10)

    # 2. Verifichiamo che il risultato contenga l'oggetto Genre correttamente creato
    assert isinstance(result[2][0], Genre)
    assert str(result[2][0]) == "RPG"


@patch("app.requests.get")
@patch("app.App._App__get_genre")
def test_get_game_rating_parsing_error(mock_get_genre, mock_requests_get):
    """
    Test that __get_game handles cases where the global_rating format
    causes a ValueError or IndexError during parsing.
    This touches the line: except (ValueError, IndexError): rating_obj = "Rating Error"
    """
    app = App()

    # Mocking a response where global_rating is a malformed string
    # "10.abc" will cause a ValueError when trying to convert int("abc")
    mock_response = Mock()
    mock_response.json.return_value = {
        "id": 1,
        "title": "Malformed Rating Game",
        "description": "A game with a rating that cannot be parsed",
        "genres": [1],
        "pegi": 12,
        "release_date": "2024-12-18",
        "global_rating": "10.abc"
    }
    mock_requests_get.return_value = mock_response
    mock_get_genre.return_value = Genre("Action")

    # Execution
    result = app._App__get_game(1)

    # Verification
    # The 6th element of the tuple (index 5) should be the error string
    assert result[5] == "Rating Error"