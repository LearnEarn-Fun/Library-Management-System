from flask import Blueprint, flash, url_for, redirect
from flask_login import login_required, current_user
from all_forms import EditProfileForm
from models import User, db
from utils import handle_page

edit_profile = Blueprint('edit_profile', __name__, template_folder='templates')

@edit_profile.route('/edit_profile/<id>', methods=['POST', 'GET'])
@login_required
def edit_profile_view(id):
    user = User.query.filter_by(id=current_user.id).first()
    form = EditProfileForm(obj=user)
    if form.validate_on_submit():
        db.session.query(User).filter(User.id == id).update({"name": form.name.data,
                                                                                 "email": form.email.data,
                                                                                 "image": form.image.data,
                                                                                 "address": form.address.data},
                                                                                synchronize_session=False)
        db.session.commit()
        flash("Updated!", category="success")
        return redirect(url_for("home.homepage"))
    return handle_page('form.html', form=form, title="Edit Profile")
