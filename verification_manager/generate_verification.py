from models import User
from werkzeug.utils import redirect
from flask import url_for, flash
from settings import serializer
from messages import verify_email, reset_password_notification


def generate_email_verification(email, name):
    token = serializer.dumps(email, salt='email-verify')
    link = url_for('verification.verify_email', token=token, email=email, _external=True)
    status = verify_email(email=email, name=name, link=link)
    category = "success" if status else "error"
    flash("A confirmation email has been sent to you.", category=category) if status else \
        flash("No sender specified, please contact the admin.", category=category)
    return redirect(url_for('home.homepage'))


def generate_password_reset(email):
    requesting_user = User.query.filter_by(email=email).first()
    if requesting_user:
        token = serializer.dumps(email, salt='forget-password')
        link = url_for('verification.forget_password', token=token, email=email, _external=True)
        status = reset_password_notification(requesting_user.name, email, link)
        category = "success" if status else "error"
        flash("A password reset email has been sent to you.", category=category) if status else \
            flash("No sender specified, please contact the admin.", category=category)
        return redirect(url_for('home.homepage'))
    else:
        flash("Could not find a user with the specified email address.")
        return redirect(url_for('verification.generate_forget'))
