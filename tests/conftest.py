import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.book import Book



@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove() # Cleans out anything in the queue waiting to be committed

    with app.app_context():
        db.create_all() # This does the work of commit and upgrade
        yield app # This chunk is going to set up our DB, and then return our app, kind of.
        # It will let us use the app, and then when we're done using the app, do cleanup below.
    with app.app_context(): # Gets run when we're done using the app
        db.drop_all() # Because we want to start every test with an empty DB.

# We have our app, but in order to send requests to it, we need to set up a client.
# A client is kind of like postman. It's a flask app feature that allows us to set up a client.

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_saved_books(app):
    # Arrange
    ocean_book = Book(title="Ocean Book", description="watr 4evr")
    mountain_book = Book(title="Mountain Book", description="i luv 2 climb rocks")

    db.session.add_all([ocean_book, mountain_book])
    # Alternatively, we could do
    # db.session.add(ocean_book)
    # db.session.add(mountain_book)
    db.session.commit() # Writes everything to the database

