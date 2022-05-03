from unittest import mock


def test_sign_up(client):
    request_data = {
        "update_id": 111, 
        "message": {
            "message_id": 111, 
            "from": {
                "id": 111, 
                "is_bot": False, 
                "first_name": "Luke", 
                "username": "darth", 
                "language_code": "en"
            }, 
            "chat": {"id": 111}, 
            "text": "Hello"
        }
    }
    response = client.post("/sign-up/", json=request_data)
    assert response.status_code == 200
    assert response.json()["id"] == 111
    assert response.json()["first_name"] == "Luke"
    assert response.json()["username"] == "darth"


def test_sign_up_existing_user(client, user):
    request_data = {
        "update_id": 111,
        "message": {
            "message_id": 111,
            "from": {
                "id": user.id,
                "is_bot": False,
                "first_name": user.first_name,
                "username": user.username,
                "language_code": "en"
            },
            "chat": {"id": 111},
            "text": "Hello"
        }
    }
    response = client.post("/sign-up/", json=request_data)
    assert response.status_code == 200
    assert response.json()["id"] == user.id
    assert response.json()["first_name"] == user.first_name
    assert response.json()["username"] == user.username


@mock.patch("app.api.routes.bot.send_message")
def test_current_word(mock_send_message, client, user, current_word):
    request_data = {
        "update_id": 111,
        "message": {
            "message_id": 111,
            "from": {
                "id": user.id,
                "is_bot": False,
                "first_name": user.first_name,
                "username": user.username,
                "language_code": "en"
            },
            "chat": {"id": 111},
            "text": "Hello"
        }
    }
    response = client.post("/current-word/", json=request_data)
    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    mock_send_message.assert_called_once()


@mock.patch("app.api.routes.bot.send_message")
def test_current_word_not_exists(mock_send_message, client, user):
    request_data = {
        "update_id": 111,
        "message": {
            "message_id": 111,
            "from": {
                "id": user.id,
                "is_bot": False,
                "first_name": user.first_name,
                "username": user.username,
                "language_code": "en"
            },
            "chat": {"id": 111},
            "text": "Hello"
        }
    }
    response = client.post("/current-word/", json=request_data)
    assert response.status_code == 200
    assert response.json()["status"] == "NOK"
    mock_send_message.assert_not_called()


@mock.patch("app.api.routes.bot.send_message")
def test_random_word(mock_send_message, client, user, current_word):
    request_data = {
        "update_id": 111,
        "message": {
            "message_id": 111,
            "from": {
                "id": user.id,
                "is_bot": False,
                "first_name": user.first_name,
                "username": user.username,
                "language_code": "en"
            },
            "chat": {"id": 111},
            "text": "Hello"
        }
    }
    response = client.post("/random-word/", json=request_data)
    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    mock_send_message.assert_called_once()


@mock.patch("app.api.routes.bot.send_message")
def test_guess_word_correct(mock_send_message, client, user, current_word):
    request_data = {
        "update_id": 111,
        "message": {
            "message_id": 111,
            "from": {
                "id": user.id,
                "is_bot": False,
                "first_name": user.first_name,
                "username": user.username,
                "language_code": "en"
            },
            "chat": {"id": 111},
            "text": current_word.word.english
        }
    }
    response = client.post("/guess-word/", json=request_data)
    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    mock_send_message.assert_called_once()


@mock.patch("app.api.routes.bot.send_message")
def test_guess_word_incorrect(mock_send_message, client, user, current_word):
    request_data = {
        "update_id": 111,
        "message": {
            "message_id": 111,
            "from": {
                "id": user.id,
                "is_bot": False,
                "first_name": user.first_name,
                "username": user.username,
                "language_code": "en"
            },
            "chat": {"id": 111},
            "text": "Incorrect"
        }
    }
    response = client.post("/guess-word/", json=request_data)
    assert response.status_code == 200
    assert response.json()["status"] == "NOK"
    mock_send_message.assert_called_once()
