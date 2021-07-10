from flask import Blueprint, request, abort, flash
from flask_login import login_required, current_user
from models import Comment, WebsiteLogs, Book, User
from all_forms import CommentForm, EditCommentForm
from extensions import db
from utils import handle_page, generate_date, generate_date_time

comment = Blueprint('comment', __name__)


@comment.route("/comment/<book_id>", methods=['GET', 'POST'])
@login_required
def comment_(book_id):
    form = CommentForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        book = Book.query.filter_by(id=book_id).first()
        if not book:
            abort(404)
        if book:
            new_comment = Comment(author=user,
                                  parent_book=book,
                                  comment=form.comment_text.data,
                                  date=generate_date(), rating=int(form.rating.data))
            new_log = WebsiteLogs(website_history={"by": user, "log": f"{user.name} commented on the book: {book.name}",
                                 "on": generate_date_time()})
            db.session.add(new_comment)
            db.session.add(new_log)
            db.session.commit()
            flash(f'You have successfully commented on {book.name}!', 'success')
            return handle_page('success.html')
    return handle_page('form.html', form=form, title="Comment")


@comment.route("/edit_comment/<comment_id>", methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    coment = Comment.query.filter_by(id=comment_id).first()
    form = EditCommentForm(obj=coment)
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        book = Book.query.filter_by(id=coment.parent_book.id).first()
        if not book:
            abort(404)
        if book:
            new_log = WebsiteLogs(website_history={"by": user, "log": f"{user.name} edited his comment that he commented on the book: {book.name}",
                                                   "on": generate_date_time()})
            db.session.add(new_log)
            db.session.query(Comment).filter(Comment.id == coment.id).update({"comment": form.comment.data, "rating": int(form.rating.data)}, synchronize_session=False)
            db.session.commit()
            flash(f'You have successfully edited the comment you commented on {book.name}!', 'success')
            return handle_page('success.html')
    return handle_page('form.html', form=form, title="Edit Comment")
