from flask import Blueprint, request
from utils import handle_page
from models import Book, User, Comment
from flask_login import login_required

my_profile = Blueprint('my_profile', __name__, template_folder='templates')


@my_profile.route('/my_profile/<id>')
@login_required
def my_profile_view(id):
    results = []
    user = User.query.filter_by(id=id).first()
    page = request.args.get('page', 1, type=int)
    comments = Comment.query.filter_by(author=user).order_by(Comment.date.desc()).paginate(page=page, per_page=3)
    results.append({"id": user.id, "name": user.name, "address": user.address, "image": user.image, "email": user.email,
                    "membership": user.membership})
    return handle_page('my_profile.html', results=results, number_results=len(results),
                           first_name=str(user.name).split(" ")[0], last_name=str(user.name).split(" ")[1],
                           no_books=len(Book.query.filter_by(taken_by=user.id).all()), comments=comments)
