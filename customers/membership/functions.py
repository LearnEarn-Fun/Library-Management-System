import calendar
import datetime

from flask import Blueprint, flash
from flask_login import login_required, current_user

from data_manager import get_data
from extensions import db
from models import User, Reports, PaymentLogs, WebsiteLogs
from utils import handle_page, generate_date_time, generate_date, check_membership_cancel

membership = Blueprint('membership', __name__, template_folder='templates')


@membership.route('/membership_options')
@login_required
def membership_options():
    return handle_page('membership.html')


@membership.route('/cancel_membership')
@login_required
def cancel_membership():
    user = User.query.filter_by(id=current_user.id).first()
    can_cancel = check_membership_cancel()
    if user.membership['membership'] is not None and can_cancel:
        db.session.query(User).filter(User.id == current_user.id).update({
            "membership": {"membership": None, "started_on": "", "end_on": ""}
        }, synchronize_session=False)
        db.session.commit()
        flash("Successfully Cancelled The Membership", "success")
        return handle_page('success.html')
    if user.membership['membership'] is None:
        flash("You do not have any membership currently, Buy a membership to continue", "error")
        return handle_page('error.html')
    if not can_cancel:
        flash("You cannot cancel your membership after 5 days of buying", "error")
        return handle_page('error.html')


@membership.route('/buy_membership/<name>/<plan>')
@login_required
def buy_membership(name, plan):
    user = User.query.filter_by(id=current_user.id).first()
    if user.membership == {"membership": None, "started_on": "", "end_on": ""}:
        if plan == "monthly":
            start_date = datetime.datetime.now()
            final_end_date = start_date + datetime.timedelta(
                days=calendar.monthrange(start_date.year, start_date.month)[1])
            db.session.query(User).filter(User.id == user.id).update({
                "membership":
                    {"membership": name.capitalize(), "started_on": generate_date(), "end_on": final_end_date}
            },
                synchronize_session=False)
            db.session.commit()
        elif plan == "yearly":
            if calendar.isleap(datetime.datetime.now().year):
                final_end_date = datetime.datetime.now() + datetime.timedelta(days=366)
            if not calendar.isleap(datetime.datetime.now().year):
                final_end_date = datetime.datetime.now() + datetime.timedelta(days=365)
            db.session.query(User).filter(User.id == user.id).update({"membership":
                                                                          {"membership": name.capitalize(),
                                                                           "started_on": generate_date(),
                                                                           "end_on": final_end_date}
                                                                      },
                                                                     synchronize_session=False)
            db.session.commit()
        report = Reports.query.filter_by(month=datetime.datetime.now().month).first()
        new_log = PaymentLogs(
            payment_history={"money": get_data()['membership_config'][name]['price'][plan], "by": user,
                             "for": f"{user.name} bought the membership {name.capitalize()}, Plan: "
                                    f"{plan.capitalize()}",
                             "on": generate_date()})
        new_website = WebsiteLogs(
            website_history={"by": user,
                             "log": f"{user.name} bought the membership {name.capitalize()}, Plan: "
                                    f"{plan.capitalize()}",
                             "on": generate_date_time()})
        db.session.add(new_website)
        db.session.add(new_log)
        db.session.commit()
        if report:
            money_by_membership = report.money_by_membership
            db.session.query(Reports).filter(Reports.month == datetime.datetime.now().month).update(
                {"money_by_membership": int(money_by_membership) + int(
                    get_data()['membership_config'][name]['price'][plan].strip("$"))})
            db.session.commit()
        else:
            new_report = Reports(month=datetime.datetime.now().month, money_by_books=0,
                                 books_rented=0,
                                 money_by_membership=int(
                                     get_data()['membership_config'][name]['price'][plan].strip("$")))
            db.session.add(new_report)
            db.session.commit()
        flash(f"You have bought the {name.capitalize()} membership successfully!", "success")
        return handle_page('success.html')

    else:
        flash(f"You have already bought {user.membership['membership']} Membership", "error")
        flash(f"Your current membership is active till {user.membership['end_on'].strftime('%m/%d/%Y')}", "info")
        return handle_page('error.html')
