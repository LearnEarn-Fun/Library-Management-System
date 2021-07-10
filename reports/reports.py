from flask import Blueprint, request
from models import Reports
from utils import admin_only, handle_page
from flask_login import login_required
from datetime import datetime

reports = Blueprint('library_reports', __name__)


@reports.route('/reports')
@login_required
@admin_only
def report():
    months = {}
    money = {}
    page = request.args.get('page', 1, type=int)
    reports = Reports.query.paginate(page=page, per_page=5)
    for repor in reports.items:
        obj = datetime.strptime(repor.month, "%m")
        months[repor.id - 1] = {"id": repor.id, "month": datetime.strftime(obj, "%B")}
        money[repor.id - 1] = {"id": repor.id, "money": int(repor.money_by_membership) + int(repor.money_by_books)}
    page_nums = []
    last_page = 0
    for page_num in reports.iter_pages():
        page_nums.append(page_num)

    for page_num in reports.iter_pages():
        if page_num == page_nums[len(page_nums) - 1]:
            last_page = page_num
    return handle_page("reports.html", results=reports, months=months, money=money, last_page=last_page)
