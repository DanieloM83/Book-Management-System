async def test_get_books(client):
    response = await client.get("/books/")

    assert response.status_code == 200
    assert response.json() == []


async def test_create_fail(client):
    response = await client.post("/books/", json={
        "genre": "Fiction",
        "year": 1900,
        "title": "string",
        "author_name": "string"
    })

    assert response.status_code == 401
    assert b"You are not logged in." in response.content


async def test_get_by_id_fail(client):
    response = await client.get("/books/1")

    assert response.status_code == 404
    assert b"Book not found." in response.content


async def test_update_fail(client):
    response = await client.patch("/books/1", json={
        "genre": "Fiction",
        "year": 1900,
    })

    assert response.status_code == 401
    assert b"You are not logged in." in response.content


async def test_delete_fail(client):
    response = await client.delete("/books/1")

    assert response.status_code == 401
    assert b"You are not logged in." in response.content
