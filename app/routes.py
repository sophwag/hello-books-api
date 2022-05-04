from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request, abort

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods=["POST"])
def handle_books():
    request_body = request.get_json()
    new_book = Book(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)


def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message":f"book {book_id} invalid"}, 400))

    book = Book.query.get(book_id)

    if not book:
        abort(make_response({"message":f"book {book_id} not found"}, 404))

    return book

@books_bp.route("/<book_id>", methods=["GET"])
def handle_book(book_id):
    book = validate_book(book_id)
    return {
        "id": book.id,
        "title": book.title,
        "description": book.description
    }

@books_bp.route("", methods=["GET"]) # See alternate below
def read_all_books():
    # this code replaces the previous query all code
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()
    # end of the new code

    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })

    return jsonify(books_response)

@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id)

    request_body = request.get_json() # this will be a dictionary

    if "title" not in request_body or \
        "description" not in request_body:
        return jsonify({'msg': 'Request must include title and description.'}), 400


    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit() # To make sure the changes go all the way to postgres

    return make_response(f"Book #{book.id} successfully updated")


@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_book(book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully deleted"))

# from turtle import title
# from flask import Blueprint, jsonify, abort, make_response
# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description

# books = [
#     Book(1, "Dune", "Sandy"),
#     Book(2, "God Emperor", "Religious"),
#     Book(3, "Calvin and Hobbes", "Jokes")
# ]

# books_bp = Blueprint("books", __name__, url_prefix="/books") # Blueprint is a class, we are creating an instance of it 

# @books_bp.route("", methods=["GET"]) # Adding a decorater in front of a function changes what that function does, this particular decorate is showing how the client should call it
# def give_books(): 
#     books_response = []
#     for book in books:
#         books_response.append({
#             "id": book.id,
#             "title": book.title,
#             "description": book.description,
#         })
#     return jsonify(books_response) # This is because our browser knows this common file format. It's a way they can communicate.
    

# @books_bp.route("/titles", methods=["GET"])
# def give_titles():
#     books_response = []
#     for book in books:
#         books_response.append({
#             "title": book.title,
#         })
#     return jsonify(books_response), 418 # order matters, first one is response code


# def validate_book(book_id):
#     try:
#         book_id = int(book_id)
#     except:
#         abort(make_response({"message":f"book {book_id} invalid"}, 400))

#     for book in books:
#         if book.id == book_id:
#             return book

#     abort(make_response({"message":f"book {book_id} not found"}, 404))

# @books_bp.route("/<book_id>", methods=["GET"])
# def handle_book(book_id): # The parameter MUST have the same exact name as in the route string
#     book = validate_book(book_id)

#     return {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description,
#     } # This is how we send a response back to the client in flask 



# car example:

# @cars_bp.route("/car_id", methods = ["GET"]):
# def get_one_car(car_id):
#   try:
#     car_id = int(car_id)
#   except ValueError: # we only want to catch one specific error
#       return jsonify({'msg'}: f'Invalid car id: "{car_id}". ID must be an integer '}), 400
#     chosen_car = None
#         for car in cars:
#             ...
#             chosen_car = {car dict}
    
#     if chosen_car is None:
#         return {'msg': f' Could not find car with id {car_id}'}, 400
#     return jsonify(chosen_car)

# Jasmine style

# @books_bp.route("", methods=["GET"])
# def read_all_books():
#     # this code replaces the previous query all code
#     params = request.args #this is an object attribute
#     if "title" in params:
#         title_name = params["title"]
#         books = Book.query.filter_by(title=title_name)
#     else:
#         books = Book.query.all()

#     books_response = []
#     for book in books:
#         books_response.append({
#             "id": book.id,
#             "title": book.title,
#             "description": book.description
#         })

#     return jsonify(books_response)