# ----------------------------- IMPORTS ----------------------------------
import datetime

from flask import Blueprint, flash, request
from flask_login import login_required, current_user

from models import Book, User, Reports, PaymentLogs, WebsiteLogs
from extensions import db
from utils import handle_page, generate_date, generate_date_time

# --------------- INITIALIZING BLUEPRINT, DB ------------------------------------
issue_book = Blueprint('issue_book', __name__, template_folder='templates')


@issue_book.route('/rent_book_options')
@login_required
def lend_book_options():
    page = request.args.get('page', 1, type=int)
    books = Book.query.paginate(page=page, per_page=3)
    page_nums = []
    last_page = 0
    for page_num in books.iter_pages():
        page_nums.append(page_num)

    for page_num in books.iter_pages():
        if page_num == page_nums[len(page_nums)-1]:
            last_page = page_num
    return handle_page('lend_book.html', results=books, last_page=last_page)


@issue_book.route('/rent_book/<id>')
@login_required
def request_book(id):
    book = Book.query.filter_by(id=id).first()  # Getting the book specified from the DB
    user = User.query.filter_by(id=current_user.id).first()
    taken_user = User.query.filter_by(id=book.taken_by).first()
    if book is None:
        flash("The book does not exist")
    if not book.is_free:  # Checking if it is free or not
        flash(f"The book is already rented by {taken_user.name}, Please see later", "error")
        return handle_page('error.html')
    if book is not None and book.is_free:
        cond = False
        membership = {"gold": "6", "silver": "4", "bronze": "2", "default": "1"}
        t = ""
        if user.membership['membership'] is None:
            cond = len(Book.query.filter_by(taken_by=user.id).all()) == 0
            t = "default"
        if user.membership['membership'] == "Gold":
            cond = len(Book.query.filter_by(taken_by=user.id).all()) <= 5
            t = "gold"
        if user.membership['membership'] == "Silver":
            cond = len(Book.query.filter_by(taken_by=user.id).all()) <= 3
            t = "silver"
        if user.membership['membership'] == "Bronze":
            cond = len(Book.query.filter_by(taken_by=user.id).all()) <= 1
            t = "bronze"
        if cond:
            db.session.query(Book).filter(Book.id==id).update(
                {"request_details": {"taken_on": generate_date(),
                                     "should_return_on": datetime.datetime.now() + datetime.timedelta(days=5)},
                 "is_free": False, "taken_by": user.id},
                synchronize_session=False)  # Updating the book
            db.session.commit()
            request_history = user.request_history  # Getting his/her request history
            request_history.append(
                {"book_img": book.img, "book_title": book.name, "taken_on": generate_date()})  # Appending to his/her request history
            db.session.query(User).filter(User.id==user.id).update(
                {"request_history": request_history},
                synchronize_session=False)  # Updating the request history in DB
            db.session.commit()  # Committing to the DB
            report = Reports.query.filter_by(month=datetime.datetime.now().month).first()
            new_log = PaymentLogs(payment_history={"money": book.price, "by": user,
                                                   "for": f"{user.name} rented the book {book.name}", "on": generate_date()})
            new_website = WebsiteLogs(
                website_history={"by": user, "log": f"{user.name} rented the book: {book.name}",
                                 "on": generate_date_time()})
            db.session.add(new_website)
            db.session.add(new_log)
            db.session.commit()
            if report:
                db.session.query(Reports).filter(Reports.month == datetime.datetime.now().month).update(
                    {"money_by_books": int(report.money_by_books) + int(book.price.strip("$")), "books_rented":
                        int(report.books_rented) + 1})
                db.session.commit()
            else:
                new_report = Reports(month=datetime.datetime.now().month, money_by_books=int(book.price.strip("$")),
                                     books_rented=1,
                                     money_by_membership=0)
                db.session.add(new_report)
                db.session.commit()
            flash("You can view the book in My Books. Please return the book in 5 Days or extra fees will "
                  "be taken", "success")
            return handle_page('success.html')
        else:
            if membership[t] == 1:
                flash(f"You have already {membership[t]} rented book", "error")
                flash("Please return the book and try to rent another book", "info")
            else:
                flash(f"You have already {membership[t]} rented books", "error")
                flash("Please return one or more books and try to rent another book", "info")
            return handle_page('error.html')
