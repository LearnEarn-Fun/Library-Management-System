from flask import request, abort, Blueprint, render_template, flash, url_for
from werkzeug.utils import redirect
from verification_manager.generate_verification import generate_password_reset
from models import User
from utils import handle_page
from verification_manager.handle_verification import handle_email_verification, load_token, handle_forgot_password
from all_forms import ForgetPasswordForm, ForgetHandlingForm

verification = Blueprint('verification', __name__)


@verification.route('/verify-email/<token>')
def verify_email(token):
    email = request.args.get('email')
    if email:
        return handle_email_verification(token=token, email=email)
    else:
        return abort(400)


@verification.route('/generate-forget', methods=['GET', 'POST'])
def generate_forget():
    form = ForgetHandlingForm()
    if form.validate_on_submit():
        return generate_password_reset(form.email.data)
    return handle_page('form.html', form=form, handling=True, title="Forgot Password")


@verification.route('/handle-forget/<token>', methods=['GET', 'POST'])
def forget_password(token):
    load_token(token=token, salt='forget-password', redirect_to='login_system.login')
    email = request.args.get('email')
    form = ForgetPasswordForm()
    user = User.query.filter_by(email=email).first()
    if user:
        if form.validate_on_submit():
            return handle_forgot_password(token=token, user=user, new_password=form.new_password.data)
        return handle_page('form.html', token=token, form=form, email=email, title="Forgot Password")
    else:
        flash("Could not find a user with the specified email address.")
        return redirect(url_for('home.homepage', category='error'))
