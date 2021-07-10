import requests
from flask import redirect, url_for, flash, Blueprint, request
from flask_login import login_required, current_user

from all_forms import ReviewBookForm
from models import BooksToReview, Book, User, WebsiteLogs
from extensions import db
from utils import admin_only, handle_page, generate_date_time

review_book = Blueprint('review_book', __name__, template_folder='templates')


@review_book.route("/selectBookToReview", methods=["GET", "POST"])
@login_required
@admin_only
def select_book():
    page = request.args.get('page', 1, type=int)
    books = BooksToReview.query.order_by(BooksToReview.id.desc()).paginate(page=page, per_page=3)
    page_nums = []
    last_page = 0
    for page_num in books.iter_pages():
        page_nums.append(page_num)

    for page_num in books.iter_pages():
        if page_num == page_nums[len(page_nums)-1]:
            last_page = page_num
    return handle_page('select_book_review.html', results=books, url='review_book.review_specific_book',
                           title="Review", last_page=last_page)


@review_book.route('/review_book/<id>', methods=["GET", "POST"])
@login_required
@admin_only
def review_specific_book(id):
    book = BooksToReview.query.filter_by(id=id).first()
    form = ReviewBookForm(obj=book)  # Initializing the Form
    if form.validate_on_submit():  # Checking if the form has been submitted
        if Book.query.filter_by(name=form.name.data).first():  # Checking if the book already exists
            flash("That book already exists", category='error')
            return redirect(url_for('home.homepage'))
        else:
            if form.accept_decline.data == "Accept":
                new_book = Book(  # Preparing a new book
                    author=form.author.data,
                    name=form.name.data,
                    img=form.img.data,
                    year=form.year.data,
                    price=form.price.data,
                    url=form.url.data,
                    category=form.category.data
                )
                done_by = User.query.filter_by(id=current_user.id).first()
                new_website = WebsiteLogs(
                    website_history={"by": done_by,
                                     "log": f"{done_by.name} reviewed the book: {form.name.data} and approved it",
                                     "on": generate_date_time()})
                db.session.add(new_website)
                db.session.query(BooksToReview).filter(BooksToReview.id == id).update({"published": True},
                                                                                           synchronize_session=False)
                db.session.commit()
                r = requests.get(form.url.data, stream=True)  # Getting the book pdf to download it
                with open(f"static/book_pdfs/{form.name.data}.pdf", "wb") as pdf:  # Creating a pdf
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            pdf.write(chunk)  # Writing the original book pdf to the pdf
                db.session.add(new_book)  # Adding the new book to the DB
                db.session.commit()  # Committing to the DB
                flash("Added the new book!", category="success")
                return redirect(url_for("home.homepage"))
            else:
                done_by = User.query.filter_by(id=current_user.id).first()
                new_website = WebsiteLogs(
                    website_history={"by": done_by,
                                     "log": f"{done_by.name} reviewed the book: {form.name.data} and declined it",
                                     "on": generate_date_time()})
                db.session.add(new_website)
                book = BooksToReview.query.filter_by(id=id).first()
                db.session.delete(book)
                db.session.commit()
    return handle_page("form.html", form=form, title="Review Book")
