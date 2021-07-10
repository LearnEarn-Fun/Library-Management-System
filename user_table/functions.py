from flask import Blueprint, request, flash, redirect, url_for, abort
from extensions import db
from models import User, WebsiteLogs
from utils import admin_only, handle_page, generate_date, get_admin_count
from flask_login import login_required, current_user
from all_forms import EditProfileForm

user_table = Blueprint('user_table', __name__)


@user_table.route('/user_table')
@login_required
@admin_only
def user_table_():
    page = request.args.get('page', 1, type=int)
    filter_by = request.args.get('filter_by', 'desc', type=str)
    users = User.query.order_by(User.join_date.desc()).paginate(page=page, per_page=5)
    if filter_by == 'aces':
        users = User.query.paginate(page=page, per_page=5)
    page_nums = []
    last_page = 0
    for page_num in users.iter_pages():
        page_nums.append(page_num)

    for page_num in users.iter_pages():
        if page_num == page_nums[len(page_nums) - 1]:
            last_page = page_num
    return handle_page("user_table.html", results=users, last_page=last_page, admins=get_admin_count(), users=len(User.query.all()))


@user_table.route('/make_admin/<id>')
@login_required
@admin_only
def make_admin(id):
    user = User.query.filter_by(id=id).first()
    done_by = User.query.filter_by(id=current_user.id).first()
    new_website = WebsiteLogs(website_history={"by": done_by, "log": f"{done_by.name} made {user.name} an admin",
                                               "on": generate_date()})
    db.session.add(new_website)
    db.session.query(User).filter(User.id==id).update({"admin": True})
    db.session.commit()
    flash(f'Successfully made {user.name} an admin!', 'success')
    return handle_page("success.html")


@user_table.route('/remove_admin/<id>')
@login_required
@admin_only
def remove_admin(id):
    if id == 1:
        abort(400)
    user = User.query.filter_by(id=id).first()
    done_by = User.query.filter_by(id=current_user.id).first()
    new_website = WebsiteLogs(website_history={"by": done_by, "log": f"{done_by.name} removed {user.name} an admin",
                                               "on": generate_date()})
    db.session.add(new_website)
    db.session.query(User).filter(User.id==id).update({"admin": False})
    db.session.commit()
    flash(f'Successfully removed {user.name} as an admin!', 'success')
    return handle_page("success.html")



@user_table.route('/edit_account/<id>', methods=['POST', 'GET'])
@login_required
@admin_only
def edit_profile(id):
    user = User.query.filter_by(id=id).first()
    form = EditProfileForm(obj=user)
    if form.validate_on_submit():
        done_by = User.query.filter_by(id=current_user.id).first()
        new_website = WebsiteLogs(website_history={"by": done_by, "log": f"{done_by.name} edited {user.name}\'s account",
                                                   "on": generate_date()})
        db.session.add(new_website)
        db.session.query(User).filter(User.id == id).update({"name": form.name.data,
                                                                                 "email": form.email.data,
                                                                                 "image": form.image.data,
                                                                                 "address": form.address.data},
                                                                                synchronize_session=False)
        db.session.commit()
        flash("Updated!", category="success")
        return redirect(url_for("home.homepage"))
    return handle_page('form.html', form=form, title="Edit Profile")
