from flask import Blueprint
from models import Book, User
from flask_login import login_required, current_user
from utils import handle_page

my_books = Blueprint('my_books', __name__, template_folder='templates')


@my_books.route('/my_books')
@login_required
def my_book():
    books = Book.query.filter_by(taken_by=current_user.id).all()
    results = []
    for book in books:
        book_name = book.name
        book_price = book.price
        book_price.strip('\r\n')
        book_author = book.author
        book_image = book.img
        results.append({"name": book_name, "price": book_price, "author": book_author, "image": book_image})
    return handle_page('my_books.html', results=results, number_results=len(results))
