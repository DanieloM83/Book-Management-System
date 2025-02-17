from core.config import settings


async def test_success_login(client):
    user_creds = {"username": "Dan123", "password": "Hello123"}
    response = await client.post("/auth/register", json=user_creds)

    assert response.status_code == 200

    response = await client.post("/auth/login", json=user_creds)

    assert response.status_code == 200
    assert len(response.cookies) == 1


async def test_success_logout(client):
    user_creds = {"username": "Dan123", "password": "Hello123"}
    response = await client.post("/auth/register", json=user_creds)

    assert response.status_code == 200

    response = await client.post("/auth/login", json=user_creds)
    cookies = response.cookies

    assert response.status_code == 200
    assert len(cookies) == 1

    client.cookies.set(settings.COOKIE_NAME, cookies[settings.COOKIE_NAME])
    response = await client.post("/auth/logout")

    assert response.status_code == 200
    assert response.headers.get("set-cookie")


async def test_success_get_current_user(client):
    user_creds = {"username": "Dan123", "password": "Hello123"}
    response = await client.post("/auth/register", json=user_creds)

    assert response.status_code == 200

    response = await client.post("/auth/login", json=user_creds)
    cookies = response.cookies

    assert response.status_code == 200
    assert len(response.cookies) == 1

    client.cookies.set(settings.COOKIE_NAME, cookies[settings.COOKIE_NAME])
    response = await client.get("/auth/current_user")

    assert response.status_code == 200
    assert response.json()["username"] == user_creds["username"]
