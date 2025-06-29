import pytest
from fastapi.testclient import TestClient

def test_create_book(client):
    book_data = {
        "title": "New Book",
        "author": "New Author",
        "year": 2023
    }
    response = client.post("/book", json=book_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == book_data["title"]
    assert data["author"] == book_data["author"]
    assert data["year"] == book_data["year"]
    assert "id" in data

def test_get_books(client, sample_book):
    response = client.get("/book")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_book(client, sample_book):
    response = client.get(f"/book/{sample_book.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_book.id
    assert data["title"] == sample_book.title
    assert data["author"] == sample_book.author
    assert data["year"] == sample_book.year

def test_get_nonexistent_book(client):
    response = client.get("/book/999999")
    assert response.status_code == 404

def test_update_book(client, sample_book):
    update_data = {
        "id": sample_book.id,  # Include the ID in the update data
        "title": "Updated Title",
        "author": sample_book.author,
        "year": sample_book.year
    }
    response = client.put(f"/book/{sample_book.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_book.id
    assert data["title"] == update_data["title"]
    assert data["author"] == update_data["author"]
    assert data["year"] == update_data["year"]



