from flask import Blueprint, request
from utils import handle_page
from models import Book, Comment

book = Blueprint('book', __name__, url_prefix="/book")


@book.route('/<id>', methods=['GET', 'POST'])
def book_page(id):
    book = Book.query.filter_by(id=id).first()
    results = []
    page = request.args.get('page', 1, type=int)
    comments = Comment.query.filter_by(parent_book=book).order_by(Comment.date.desc()).paginate(page=page, per_page=3)
    page_nums = []
    last_page = 0
    for page_num in comments.iter_pages():
        page_nums.append(page_num)

    for page_num in comments.iter_pages():
        if page_num == page_nums[len(page_nums) - 1]:
            last_page = page_num
    results.append({"id": book.id, "name": book.name, "year": book.year, "image": book.img, "category": book.category, "author": book.author})
    return handle_page(endpoint='book_page.html', results=results, comments=comments, last_page=last_page)