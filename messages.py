from utils import send_mail, get_website_name
from flask_mail import Message
from app_config import MAIL_USERNAME as EMAIL


def password_changed_notification(email, name, date):
    msg = Message(f'Password Changed', sender=EMAIL, recipients=[email])
    msg.body = f"Hello {name}, this is an automatic email from {get_website_name('m')} to notify you of recent" \
               f" events that occurred in regards to your account.\n\n" \
               f'Your account password was changed at {date}.\n\n' \
               f"If this wasn't you, contact us by replying to this email."
    send_mail(msg)


def reset_password_notification(name, email, link):
    msg = Message('Forget Password', sender=EMAIL, recipients=[email])
    msg.body = f"Hello {name}, you have recently requested a password change," \
               f" please go to this link to reset your password.\n\n{link}\n\n" \
               f"If this wasn't you, please contact us by replying to this email."
    return send_mail(msg)


def verify_email(name, email, link):
    msg = Message('Confirmation Email', sender=EMAIL, recipients=[email])
    msg.body = f"Hello {name}, please go to this link to finalize your registration.\n\n" \
               f"{link}\n\nNote: If you're unfamiliar with the source of this email, simply ignore it."
    return send_mail(msg)