# Pytest is particular and wants us to start this file with test_
from urllib import response
from app.models.book import Book

def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books") #this sends an HTTP request to /books
    response_body = response.get_json() # this gets the json that is the response body

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_all_books_with_two_records(client, two_saved_books):
    # Act
    response = client.get("/books") #this sends an HTTP request to /books
    response_body = response.get_json()

    # Assert
    assert len(response_body) == 2
    assert response.status_code == 200
    assert response_body == [{
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    },
    {
        "id": 2,
        "title": "Mountain Book",
        "description": "i luv 2 climb rocks"
    }]

def test_get_one_book(client, two_saved_books): # We're passing in two fixtures
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }

def test_create_one_book(client):
    # Act
    response = client.post("/books", json={
        "title": "New Book",
        "description": "The Best!"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == "Book New Book successfully created"
    books = Book.query.all()
    assert len(books) == 1
    assert books[0].title == "New Book"
    assert books[0].description == "The Best!"

# Let's write a test that isn't a positive confirmation
# Remember our DB is emptied at the end of every test
# And re-layed out from scratch at the start

def test_get_one_book_with_empty_db_returns_404(client):
    response = client.get('/books/1')
    assert response.status_code == 404

