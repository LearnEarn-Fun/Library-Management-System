from flask import redirect, url_for, flash, request, Blueprint
from flask_login import login_required, current_user

from all_forms import UpdateBookForm
from models import Book, User, WebsiteLogs
from utils import handle_page, generate_date_time
from extensions import db

update_book = Blueprint('update_book', __name__, template_folder='templates')


@update_book.route("/select_book", methods=["GET", "POST"])
@login_required
def select_book():
    page = request.args.get('page', 1, type=int)
    books = Book.query.paginate(page=page, per_page=3)
    page_nums = []
    last_page = 0
    for page_num in books.iter_pages():
        page_nums.append(page_num)

    for page_num in books.iter_pages():
        if page_num == page_nums[len(page_nums) - 1]:
            last_page = page_num
    return handle_page('select_book.html', results=books,
                       url='update_book.update_specific_book', title="Update", url1='update_book.select_book',
                       last_page=last_page)


@update_book.route('/update_book/<id>', methods=["GET", "POST"])
@login_required
def update_specific_book(id):
    book = Book.query.filter_by(id=id).first()
    form = UpdateBookForm(obj=book)
    if form.validate_on_submit():
        done_by = User.query.filter_by(id=current_user.id).first()
        new_website = WebsiteLogs(
            website_history={"by": done_by,
                             "log": f"{done_by.name} updated the book: {form.name.data}",
                             "on": generate_date_time()})
        db.session.add(new_website)
        db.session.query(Book).filter(Book.id == id).update({"name": form.name.data,
                                                             "author": form.author.data,
                                                             "img": form.img.data,
                                                             "year": form.year.data,
                                                             "price": form.price.data,
                                                             "url": form.url.data,
                                                             "category": form.category.data},
                                                            synchronize_session=False)
        db.session.commit()
        flash("Updated the book!", category="success")
        return redirect(url_for("home.homepage"))
    return handle_page("form.html", form=form, title="Update Book")
