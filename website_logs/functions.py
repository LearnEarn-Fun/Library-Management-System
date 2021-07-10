from flask import Blueprint, request
from utils import handle_page, admin_only
from models import WebsiteLogs

website_logs = Blueprint('website_logs', __name__, url_prefix="/website_logs")


@website_logs.route("/")
@admin_only
def website_log():
    page = request.args.get('page', 1, type=int)
    filter_by = request.args.get('filter_by', 'desc', type=str)
    logs = WebsiteLogs.query.order_by(WebsiteLogs.id.desc()).paginate(page=page, per_page=5)
    if filter_by == 'aces':
        logs = WebsiteLogs.query.paginate(page=page, per_page=5)
    page_nums = []
    last_page = 0
    for page_num in logs.iter_pages():
        page_nums.append(page_num)
    for page_num in logs.iter_pages():
        if page_num == page_nums[len(page_nums) - 1]:
            last_page = page_num
    return handle_page('website_logs.html', results=logs, last_page=last_page)
