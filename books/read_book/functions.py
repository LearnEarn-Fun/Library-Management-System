from flask import Blueprint
from flask_login import login_required
from utils import handle_page
read_book = Blueprint('read_book', __name__, template_folder='templates')


@read_book.route('/read_book/<name>')
@login_required
def read_books(name):
    return handle_page('preview-book.html',
                           url=f"../static/book_pdfs/{name}.pdf",
                           book_name=name)
