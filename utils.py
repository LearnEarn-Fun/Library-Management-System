import datetime as dt
from functools import wraps
import requests
from flask import render_template, abort, flash, redirect, url_for
from flask_login import current_user
from extensions import mail
from app_config import GOOGLE_DISCOVERY_URL
from data_manager import get_data
from models import User


def get_user_details():
    try:
        user = User.query.filter_by(id=current_user.id).first()
        user_details = {"name": user.name, "img": user.image, "admin": user.admin, "membership": user.membership, "id": user.id}
    except:
        user_details = {"name": "Guest", "img": "", "admin": False, "membership": {"membership": None, "started_on": ""}, "id": ""}
    return user_details


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def generate_date():
    months = [(i, dt.date(2008, i, 1).strftime('%B')) for i in range(1, 13)]
    now = dt.datetime.now()
    current_month = [month for month in months if now.month == month[0]][0][1]
    if now.day <= 9:
        return f'0{now.day}/{current_month}/{now.year}'
    else:
        return f'{now.day}/{current_month}/{now.year}'

def generate_date_time():
    months = [(i, dt.date(2008, i, 1).strftime('%B')) for i in range(1, 13)]
    now = dt.datetime.now()
    current_month = [month for month in months if now.month == month[0]][0][1]
    if now.minute <= 9:
        return f'{now.day}/{current_month}/{now.year} | {now.hour}:0{now.minute}:{now.second}'
    elif now.minute <= 9 and now.second <= 9:
        return f'{now.day}/{current_month}/{now.year} | {now.hour}:0{now.minute}:0{now.second}'
    elif now.second <= 9:
        return f'{now.day}/{current_month}/{now.year} | {now.hour}:{now.minute}:0{now.second}'
    elif now.day <= 9:
        return f'0{now.day}/{current_month}/{now.year} | {now.hour}:{now.minute}:0{now.second}'

def listToString(s):
    str1 = ""

    for i in s:
        str1 += i

    return str1


def handle_page(endpoint, **kwargs):
    user_details = get_user_details()
    is_valid = check_membership_cancel()
    return render_template(endpoint, user_name=user_details['name'], admin=user_details['admin'],
                           image=user_details['img'],
                           membership=user_details['membership'], id=user_details['id'], settings=get_data(),
                           is_valid=is_valid,
                           **kwargs)


def get_admin_count():
    return len([user for user in User.query.all() if user.admin is True])


def admin_only(f):
    @wraps(f)
    def wrapper(**kwargs):
        user = User.query.filter_by(id=current_user.id).first()
        if user.admin is True:
            return f(**kwargs)
        else:
            abort(403)

    return wrapper


def send_mail(msg):
    try:
        mail.send(msg)
        return True
    except AssertionError:
        flash("Sender Email is not specified, please contact the admin.")
        return redirect(url_for('home.homepage', category='error'))


def get_website_name(configuration=None):
    data = get_data()
    try:
        return dict(name=data["website_config"]["name"]) if configuration is None else \
            data["website_config"]["name"]
    except (TypeError, IndexError, KeyError):
        return dict(name="Library Managament System") if configuration is None else data["website_config"]["name"]


def check_membership_cancel():
    user_details = get_user_details()
    is_valid = False
    if user_details['membership']['membership'] != None:
        date = dt.datetime.now() - dt.datetime.strptime(user_details['membership']['started_on'], '%d/%B/%Y')
        if date.days > 5:
            is_valid = False
        if date.days < 5:
            is_valid = True
    return is_valid