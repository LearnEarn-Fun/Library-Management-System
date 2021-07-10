# ----------------------------- IMPORTS ----------------------------------
from flask import redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from models import BooksToReview, User, WebsiteLogs
from extensions import db
from all_forms import CreateBookForm
from utils import handle_page, generate_date, generate_date_time

# --------------- INITIALIZING BLUEPRINT, DB ------------------------------------
donate_book = Blueprint('donate_book', __name__, template_folder='templates')


@donate_book.route('/donate_book_benefits', methods=["GET", "POST"])
@login_required
def donate_book_benefits():
    return handle_page('donate_book_benefits.html')


@donate_book.route('/donate_book', methods=["GET", "POST"])
@login_required
def donate_new_book():
    form = CreateBookForm() # Initializing the form
    user = User.query.filter_by(id=current_user.id).first()
    if form.validate_on_submit(): # Checking if the is submitted
        if BooksToReview.query.filter_by(name=form.title.data).first(): # Checking if the book already exists
            flash("That book already exists in the review queue", category='error')
            return redirect(url_for('home.homepage'))
        else:
            new_book = BooksToReview( # Preparing a new book
                author=form.author.data,
                name=form.title.data,
                img=form.img_url.data,
                year=form.year.data,
                price=form.price.data,
                url=form.book_url.data,
                donated_by=user.name,
                category=form.category.data
            )
            new_website = WebsiteLogs(
                website_history={"by": user, "log": f"{user.name} donated a book: {form.title.data}",
                                 "on": generate_date_time()})
            db.session.add(new_book) # Adding the book to the DB
            db.session.add(new_website)
            db.session.commit() # Committing to the DB
            flash("Added the book for review!", category="success")
            return redirect(url_for("home.homepage"))

    return handle_page("form.html", form=form, title="Donate Book")
