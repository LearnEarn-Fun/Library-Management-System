from flask import Blueprint, abort, flash
from flask_login import login_required, current_user
from models import Book, User, WebsiteLogs
from extensions import db
from utils import handle_page, generate_date_time

return_books = Blueprint('return_books', __name__, template_folder='templates')


@return_books.route('/return_book_options')
@login_required
def return_book_view():
    user = User.query.filter_by(id=current_user.id).first()
    books = Book.query.filter_by(taken_by=user.id).all()
    results = []
    for book in books:
        book_name = book.name
        book_price = book.price
        book_price.strip('\r\n')
        book_author = book.author
        book_image = book.img
        results.append(
            {"id": book.id, "name": book_name, "price": book_price, "author": book_author, "image": book_image})
    return handle_page('return_books.html', results=results, number_results=len(results))


@return_books.route("/return_book/<id>")
@login_required
def return_book(id):
    user = User.query.filter_by(id=current_user.id).first()
    book = Book.query.filter_by(id=id).first()
    new_website = WebsiteLogs(
        website_history={"by": user, "log": f"{user.name} returned the book: {book.name}",
                         "on": generate_date_time()})
    db.session.add(new_website)
    db.session.query(Book).filter(Book.id == id).update({"request_details":
                                                             {"taken_on": "", "should_return_on": ""},
                                                         "is_free": True, "taken_by": ""},
                                                        synchronize_session=False)
    db.session.commit()
    flash('Successfully Returned the book!', 'success')
    return handle_page('success.html')


@return_books.route('/return_all_books')
@login_required
def return_all_together():
    user = User.query.filter_by(id=current_user.id).first()
    new_website = WebsiteLogs(
        website_history={"by": user, "log": f"{user.name} returned the all the books he had rented",
                         "on": generate_date_time()})
    db.session.add(new_website)
    db.session.query(Book).filter(Book.taken_by == user.id).update({"request_details":
                                                                        {"taken_on": "", "should_return_on": ""},
                                                                    "is_free": True, "taken_by": ""},
                                                                   synchronize_session=False)
    db.session.commit()
    return handle_page('success.html')
