async def test_register_fail(client):
    response = await client.post("/auth/register", json={"username": "", "password": "asdasdSA123"})
    assert response.status_code == 422


async def test_login_fail(client):
    response = await client.post("/auth/login", json={"username": "Asdasd23", "password": "asdasdSA123"})
    assert response.status_code == 401
    assert b"Wrong username or password." in response.content


async def test_current_user_fail(client):
    response = await client.get("/auth/current_user")
    assert response.status_code == 401
    assert b"You are not logged in." in response.content


async def test_logout(client):
    response = await client.post("/auth/logout")
    assert response.status_code == 200
