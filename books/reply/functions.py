from flask import Blueprint, abort, flash
from flask_login import login_required, current_user
from models import Comment, WebsiteLogs, User, Reply
from all_forms import ReplyForm, EditReplyForm
from extensions import db
from utils import handle_page, generate_date, generate_date_time

reply = Blueprint('reply', __name__)


@reply.route("/reply/<comment_id>", methods=['GET', 'POST'])
@login_required
def reply_(comment_id):
    form = ReplyForm()
    if form.validate_on_submit():
        coment = Comment.query.get(int(comment_id))
        user = User.query.get(current_user.id)
        if not coment:
            abort(404)
        if coment:
            new_reply = Reply(author=user,
                              parent_comment=coment,
                              reply=form.reply.data,
                              date=generate_date())
            new_log = WebsiteLogs(website_history={"by": user,
                                                   "log": f"{user.name} replied on a comment that {coment.author.name} wrote on {coment.parent_book.name}",
                                                   "on": generate_date_time()})
            db.session.add(new_reply)
            db.session.add(new_log)
            db.session.commit()
            flash(
                f'You have successfully replied on the comment that {coment.author.name} wrote on {coment.parent_book.name}!',
                'success')
            return handle_page('success.html')
    return handle_page('form.html', form=form, title="Reply")


@reply.route("/edit_reply/<reply_id>", methods=['GET', 'POST'])
@login_required
def edit_reply(reply_id):
    reply = Reply.query.filter_by(id=reply_id).first()
    form = EditReplyForm(obj=reply)
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        new_log = WebsiteLogs(website_history={"by": user,
                                               "log": f"{user.name} edited a reply he wrote!",
                                               "on": generate_date_time()})
        db.session.query(Reply).filter(Reply.id == reply_id).update(
            {"reply": form.reply.data}, synchronize_session=False)
        db.session.add(new_log)
        db.session.commit()
        flash(
            f'You have successfully edited the reply!',
            'success')
        return handle_page('success.html')

    return handle_page('form.html', form=form, title="Edit Reply")
