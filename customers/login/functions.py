from flask import redirect, url_for, flash, Blueprint
from all_forms import LoginForm
from models import User
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from utils import handle_page

log_in_out = Blueprint('log_in_out', __name__, template_folder='templates')


@log_in_out.route('/login_options', methods=['GET', 'POST'])
def login_options():
    return handle_page('login_options.html')


@log_in_out.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("A account with that email does not exist, Please register.", category="error")
            return redirect(url_for('register.register_user'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.', category="error")
            return redirect(url_for('log_in_out.login'))
        else:
            login_user(user)
            return redirect(url_for('home.homepage'))
    return handle_page('login.html', form=form)


@log_in_out.route("/logout")
@login_required
def logout():
    logout_user()
    return handle_page('logged_out.html')
