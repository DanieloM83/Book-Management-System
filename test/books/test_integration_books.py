async def test_create(client):
    user_creds = {"username": "Dan123", "password": "Hello123"}
    book = {
        "genre": "Fiction",
        "year": 1900,
        "title": "string",
        "author_name": "string"
    }

    response = await client.post("/auth/register", json=user_creds)
    assert response.status_code == 200
    response = await client.post("/books/", json=book)
    assert response.status_code == 200
    response = await client.get("/books/")
    assert response.status_code == 200
    assert response.json() == [{**book, "id": 1}]


async def test_get_by_id(client):
    user_creds = {"username": "Dan123", "password": "Hello123"}
    book = {
        "genre": "Fiction",
        "year": 1900,
        "title": "string",
        "author_name": "string"
    }

    response = await client.post("/auth/register", json=user_creds)
    assert response.status_code == 200
    response = await client.post("/books/", json=book)
    assert response.status_code == 200
    response = await client.get("/books/1")
    assert response.status_code == 200
    assert response.json() == {**book, "id": 1}


async def test_update(client):
    user_creds = {"username": "Dan123", "password": "Hello123"}
    book = {
        "genre": "Fiction",
        "year": 1900,
        "title": "string",
        "author_name": "string"
    }
    book2 = {
        "title": "string 2",
        "year": 1930,
    }

    response = await client.post("/auth/register", json=user_creds)
    assert response.status_code == 200
    response = await client.post("/books/", json=book)
    assert response.status_code == 200
    response = await client.patch("/books/1", json=book2)
    assert response.status_code == 200
    assert response.json() == {**book, **book2, "id": 1}


async def test_delete(client):
    user_creds = {"username": "Dan123", "password": "Hello123"}
    book = {
        "genre": "Fiction",
        "year": 1900,
        "title": "string",
        "author_name": "string"
    }

    response = await client.post("/auth/register", json=user_creds)
    assert response.status_code == 200
    response = await client.post("/books/", json=book)
    assert response.status_code == 200
    response = await client.delete("/books/1")
    assert response.status_code == 200
    response = await client.get("/books/")
    assert response.json() == []
