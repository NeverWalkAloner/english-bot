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
