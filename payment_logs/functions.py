from flask import Blueprint, request, flash
from utils import handle_page, admin_only
from models import PaymentLogs
from extensions import db

payment_logs = Blueprint('payment_logs', __name__, url_prefix="/payment_logs")


@payment_logs.route("/")
@admin_only
def payment_log():
    page = request.args.get('page', 1, type=int)
    filter_by = request.args.get('filter_by', 'desc', type=str)
    logs = PaymentLogs.query.order_by(PaymentLogs.id.desc()).paginate(page=page, per_page=5)
    if filter_by == 'aces':
        logs = PaymentLogs.query.paginate(page=page, per_page=5)
    page_nums = []
    total_money = 0
    last_page = 0
    for log in PaymentLogs.query.all():
        total_money += int(log.payment_history['money'].strip("$"))
    for page_num in logs.iter_pages():
        page_nums.append(page_num)
    for page_num in logs.iter_pages():
        if page_num == page_nums[len(page_nums) - 1]:
            last_page = page_num
    return handle_page('payment_logs.html', results=logs, last_page=last_page, total_money=total_money)
