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

    response = client.get(f"/me/items", headers={"X-API-TOKEN": token})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["title"] == title
    assert data[0]["description"] == description
    assert data[0]["owner_id"] == owner_id