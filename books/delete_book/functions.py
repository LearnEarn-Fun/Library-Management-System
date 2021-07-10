# ----------------------------- IMPORTS ----------------------------------
from flask import redirect, url_for, Blueprint, request
from models import Book, WebsiteLogs, User
from extensions import db
from utils import handle_page, admin_only, generate_date_time
from flask_login import login_required, current_user

# --------------- INITIALIZING BLUEPRINT, DB ------------------------------------
delete_book = Blueprint('delete_book', __name__, template_folder='templates')


# ---------------------- DELETE BOOK --------------------------------

@delete_book.route("/select_book_to_delete", methods=["GET", "POST"])
@login_required
@admin_only
def select_book():
    page = request.args.get('page', 1, type=int)
    books = Book.query.paginate(page=page, per_page=3)
    page_nums = []
    last_page = 0
    for page_num in books.iter_pages():
        page_nums.append(page_num)

    for page_num in books.iter_pages():
        if page_num == page_nums[len(page_nums)-1]:
            last_page = page_num
    return handle_page("select_book.html", url='delete_book.delete_specific_book', title="Delete", results=books,
                       url1='delete_book.select_book', last_page=last_page)


@delete_book.route('/delete_book/<id>', methods=["GET", "POST"])
@login_required
@admin_only
def delete_specific_book(id):
    if Book.query.filter_by(id=id).first() is None:  # If the book doesn't exist
        return redirect(url_for('home.homepage'))
    book = Book.query.filter_by(id=id).first()  # Getting the book
    done_by = User.query.filter_by(id=current_user.id).first()
    new_website = WebsiteLogs(website_history={"by": done_by, "log": f"{done_by.name} deleted the book: {book.name}",
                                               "on": generate_date_time()})
    db.session.add(new_website)
    db.session.delete(book)  # Delete the book in DB Session
    db.session.commit()  # Commit to the DB
    return redirect(url_for('home.homepage'))
