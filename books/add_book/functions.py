# ----------------------------- IMPORTS ----------------------------------
import requests
from flask import redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user

from all_forms import CreateBookForm
from extensions import db
from models import Book, User, WebsiteLogs
from utils import handle_page, admin_only, generate_date_time

# --------------- INITIALIZING BLUEPRINT, DB ------------------------------------
add_book = Blueprint('add_book', __name__, template_folder='templates')


# ------------------------- ADD BOOK -------------------------------

@add_book.route('/add_book', methods=["GET", "POST"])
@login_required
@admin_only
def add_new_book():
    form = CreateBookForm()  # Initializing the Form
    if form.validate_on_submit():  # Checking if the form has been submitted
        if Book.query.filter_by(name=form.title.data).first():  # Checking if the book already exists
            flash("The book already exists!", category='error')
            return redirect(url_for('home.homepage'))
        else:
            new_book = Book(  # Preparing a new book
                author=form.author.data,
                name=form.title.data,
                img=form.img_url.data,
                year=form.year.data,
                price=form.price.data,
                url=form.book_url.data,
                category=form.category.data
            )
            done_by = User.query.filter_by(id=current_user.id).first()
            new_website = WebsiteLogs(
                website_history={"by": done_by, "log": f"{done_by.name} added book: {form.name.data}",
                                 "on": generate_date_time()})
            db.session.add(new_website)
            db.session.add(new_book)  # Adding the new book to the DB
            db.session.commit()  # Committing to the DB
            r = requests.get(form.book_url.data, stream=True)  # Getting the book pdf to download it
            with open(f"static/book_pdfs/{form.title.data}.pdf", "wb") as pdf:  # Creating a pdf
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        pdf.write(chunk)  # Writing the original book pdf to the pdf
            flash("Added the new book!", category="success")
            return redirect(url_for("home.homepage"))
    return handle_page("form.html", form=form, title="Add Book")
