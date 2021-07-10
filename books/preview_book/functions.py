from PyPDF2 import PdfFileWriter, PdfFileReader
from flask import Blueprint, abort
from flask_login import login_required
from models import Book
from utils import handle_page

preview_book = Blueprint('preview_book', __name__, template_folder='templates')


@preview_book.route('/preview_book/<id>')
@login_required
def preview_books(id, name):
    books = Book.query.all()
    book_ids = []
    for book in books:
        book_ids.append(book.id)
    if id not in book_ids:
        abort(404)
    if id in book_ids:
        pages_to_keep = [0, 1, 2, 3]
        infile = PdfFileReader(rf'C:\\Users\\veer4\\PycharmProjects\\Python Programs\\Library Managament System\\static\\book_pdfs\\{name}.pdf', 'rb')
        output = PdfFileWriter()
        for i in pages_to_keep:
            p = infile.getPage(i)
            output.addPage(p)
        with open(rf'C:\\Users\\veer4\\PycharmProjects\\Python Programs\\Library Managament System\\static\\book_pdfs\\{name}_preview.pdf', 'wb') as f:
            output.write(f)
        for_url = f"../static/book_pdfs/{name}_preview.pdf"
        return handle_page('preview-book.html', url=for_url, book_name=name)
