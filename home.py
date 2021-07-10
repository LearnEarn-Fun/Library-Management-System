from flask import Blueprint
from utils import handle_page
from models import Book, User
from data_manager import get_data
from requests import get

home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
def homepage():
    response = get(get_data()['website_config']['icon'])
    with open("static/icon.png", "wb") as icon:
        icon.write(response.content)
    results = []
    books = Book.query.order_by(Book.id.desc()).all()
    for book in books:
        if book.id == 6:
            break
        taken_user = User.query.filter_by(id=book.taken_by).first()
        try:
            taken_name = taken_user.name
        except:
            taken_name = ""
        results.append(
            {"id": book.id, "name": book.name, "price": book.price.strip('\r\n'), "author": book.author, "image": book.img,
             "free": book.is_free, "request_details": book.request_details, "year": book.year,
             "taken_by": taken_name, "category": book.category})
    return handle_page(endpoint='index.html', results=results)
