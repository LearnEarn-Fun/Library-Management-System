from flask import Blueprint
from flask_login import login_required, current_user
from models import User
from extensions import db
from utils import handle_page

request_history = Blueprint('request_history', __name__, template_folder='templates')


@request_history.route("/request_history/<id>")
@login_required
def request_history_(id):
    user = User.query.filter_by(id=id).first()
    results = user.request_history
    return handle_page('request_history.html', results=results, no_results=len(results))


@request_history.route("/clear_request_history/<id>")
@login_required
def clear_request_history(id):
    db.session.query(User).filter(User.id==id).update({"request_history": []},
                                                                              synchronize_session=False)
    db.session.commit()
    return handle_page('request_history.html')
