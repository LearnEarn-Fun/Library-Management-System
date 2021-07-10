from flask_login import login_user
from itsdangerous import SignatureExpired, BadTimeSignature
from flask import flash, redirect, url_for, abort
from werkzeug.security import generate_password_hash
from settings import serializer, TOKEN_AGE
from models import User
from utils import generate_date
from extensions import db
from messages import password_changed_notification


def load_token(token, salt, redirect_to='home.home_page'):
    """Checks whether a token is valid or redirects the user."""
    try:
        confirmation = serializer.loads(token, salt=salt, max_age=TOKEN_AGE)
    except SignatureExpired:
        flash("The token is expired, please try again.")
        return redirect(url_for(redirect_to))
    except BadTimeSignature:
        flash("Incorrect token, please try again.")
        return redirect(url_for(redirect_to))


def handle_email_verification(token, email):
    load_token(token=token, salt='email-verify', redirect_to='register')
    user = User.query.filter_by(email=email).first()
    if user:
        if not user.confirmed_email:
            user.confirmed_email = True
            user.join_date = generate_date()
            login_user(user)
            db.session.commit()
            flash("You've confirmed your email successfully.", "success")
        else:
            flash("You've already confirmed your email.", category="error")
        return redirect(url_for('home.homepage'))
    else:
        flash("This user does not exist.")
        return redirect(url_for('log_in_out.register'))


def handle_forgot_password(token, user, new_password):
    load_token(token=token, salt='forget-password', redirect_to='login')
    if user:
        new_password = generate_password_hash(password=new_password,
                                              method='pbkdf2:sha256', salt_length=8)
        try:
            user.password = new_password
        except AttributeError:
            abort(400)
        db.session.commit()
        password_changed_notification(user.email, user.name, generate_date())
        flash("Password changed successfully.")
        return redirect(url_for('log_in_out.login', category='success'))
    else:
        flash("Could not find a user with the specified email address.")
        return redirect(url_for('home.homepage', category='error'))
