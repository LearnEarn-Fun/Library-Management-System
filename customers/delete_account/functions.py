from flask import Blueprint, abort
from flask_login import login_required, logout_user, current_user
from utils import handle_page, generate_date_time
from models import User, WebsiteLogs
from extensions import db

delete_profile = Blueprint('delete_profile', __name__, template_folder='templates')


@delete_profile.route('/delete_profile/<id>', methods=['POST', 'GET'])
@login_required
def delete_profile_view(id, admin=False):
    user = User.query.filter_by(id=current_user.id).first()
    user_delete = User.query.get(int(id))
    if not admin:
        if id != user.id:
            abort(403)
    if admin:
        if id == 1:
            abort(403)
    new_website = WebsiteLogs(website_history={"by": user, "log": f"{user.name} deleted {user_delete.name}\'s account",
                                               "on": generate_date_time()})
    db.session.add(new_website)
    logout_user()
    db.session.delete(user_delete)
    db.session.commit()
    return handle_page('success.html')
