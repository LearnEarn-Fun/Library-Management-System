from imports import *

def create_app(config_file='app_config.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    ckeditor.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    search.init_app(app)
    gravatar.init_app(app)
    csrf_protection.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        try:
            user = User.query.get(int(user_id))
            if user.confirmed_email:
                return user
        except AttributeError:
            pass
    app.register_blueprint(reports)
    app.register_blueprint(home)
    app.register_blueprint(add_book)
    app.register_blueprint(search_)
    app.register_blueprint(read_book)
    app.register_blueprint(reply)
    app.register_blueprint(return_books)
    app.register_blueprint(donate_book)
    app.register_blueprint(review_book)
    app.register_blueprint(update_book)
    app.register_blueprint(delete_book)
    app.register_blueprint(preview_book)
    app.register_blueprint(issue_book)
    app.register_blueprint(log_in_out)
    app.register_blueprint(register)
    app.register_blueprint(my_profile)
    app.register_blueprint(edit_profile)
    app.register_blueprint(delete_profile)
    app.register_blueprint(membership)
    app.register_blueprint(request_history)
    app.register_blueprint(my_books)
    app.register_blueprint(google_oauth)
    app.register_blueprint(verification)
    app.register_blueprint(user_table)
    app.register_blueprint(book)
    app.register_blueprint(settings)
    app.register_blueprint(payment_logs)
    app.register_blueprint(comment)
    app.register_blueprint(website_logs)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, not_found)
    app.register_error_handler(500, internal_error)
    app.register_error_handler(401, unauthorized)
    return app


app = create_app()
app.app_context().push()
from models import Book, BooksToReview, WebsiteSettings, Reports, User
db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
