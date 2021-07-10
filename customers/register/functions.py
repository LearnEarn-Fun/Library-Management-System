from werkzeug.security import generate_password_hash
from flask import redirect, url_for, flash, Blueprint
from models import User, WebsiteLogs
from extensions import db
from all_forms import RegisterForm
from flask_login import current_user
from utils import handle_page, generate_date, generate_date_time
from verification_manager.generate_verification import generate_email_verification

register = Blueprint('register', __name__, template_folder='templates')


@register.route('/register', methods=["GET", "POST"])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("You've already signed up with that email, log in instead!", category='error')
            return redirect(url_for('log_in_out.login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
            address=form.address.data,
            image=form.picture.data,
            join_date=generate_date()
        )
        done_by = User.query.filter_by(id=current_user.id).first()
        new_website = WebsiteLogs(
            website_history={"by": done_by,
                             "log": f"{form.name.data} registered!",
                             "on": generate_date_time()})
        db.session.add(new_website)
        db.session.add(new_user)
        db.session.commit()
        generate_email_verification(form.email.data, form.name.data)
        flash("You have successfully Registered!", category="success")
        return redirect(url_for("home.homepage"))
    return handle_page("register.html", form=form)
