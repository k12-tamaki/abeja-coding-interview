def test_create_user(test_db, client):
    response = client.post(
        "/users/",
        json={"email": "deadpool@example.com", "password": "chimichangas4life"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert "id" in data
    user_id = data["id"]
    assert "token" in data
    token = data["token"]

    response = client.get(f"/users/{user_id}", headers={"X-API-TOKEN": token})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert data["id"] == user_id


def test_item_me(test_db, client):
    # Add User
    response = client.post(
        "/users/",
        json={"email": "deadpool@example.com", "password": "chimichangas4life"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    user_id = data["id"]
    assert "token" in data
    token = data["token"]

    # Add User Item
    title = "example_title"
    description = "example_description"
    response = client.post(
        f"/users/{user_id}/items/",
        json={"title": title, "description": description},
        headers={"X-API-TOKEN": token}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == title
    assert data["description"] == description
    assert "owner_id" in data
    owner_id = data["owner_id"]

    # Get User Item
    response = client.get("/me/items", headers={"X-API-TOKEN": token})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["title"] == title
    assert data[0]["description"] == description
    assert data[0]["owner_id"] == owner_id

def test_user_delete(test_db, client):
    # Add User1
    response = client.post(
        "/users/",
        json={"email": "deadpool@example.com", "password": "chimichangas4life"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    user_id = data["id"]
    assert "token" in data
    token = data["token"]

    # Add User2
    response = client.post(
        "/users/",
        json={"email": "deadpool2@example.com", "password": "chimichangas4life2"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    user_id_new = data["id"]
    assert "token" in data
    token_new = data["token"]

    # Add User2 Item
    title = "example_title"
    description = "example_description"
    response = client.post(
        f"/users/{user_id_new}/items/",
        json={"title": title, "description": description},
        headers={"X-API-TOKEN": token_new}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == title
    assert data["description"] == description
    assert "owner_id" in data

    # Delete User2
    response = client.delete(f"/users/{user_id_new}", headers={"X-API-TOKEN": token})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["status"] == "ok"

    # Get Item User1
    response = client.get("/me/items", headers={"X-API-TOKEN": token})
    data = response.json()
    assert data[0]["title"] == title
    assert data[0]["description"] == description
    assert data[0]["owner_id"] == user_id
