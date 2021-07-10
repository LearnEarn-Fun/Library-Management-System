from flask import Blueprint
from all_forms import SearchForm
from models import User, Book
from utils import handle_page

search_ = Blueprint('search', __name__, url_prefix='/search')


@search_.route('/', methods=['GET', 'POST'])
def _search():
    form = SearchForm()
    if form.validate_on_submit():
        if form.category.data == "Books":
            books = Book.query.msearch(form.search.data).all()
            print(books)
            return handle_page('results.html', no_results=len(books), results=books, title="Books", books=True,
                               query=form.search.data)
        if form.category.data == "Users":
            users = User.query.msearch(form.search.data).all()
            return handle_page('results.html', no_results=len(users), results=users, title="Users", books=False,
                               query=form.search.data)
    return handle_page('search.html', form=form)
