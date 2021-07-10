from flask_login import UserMixin
from sqlalchemy.ext.mutable import MutableList, MutableDict
from sqlalchemy import PickleType
from extensions import db
from sqlalchemy import JSON
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash


class User(UserMixin, db.Model):
    __tablename__ = "users"
    __searchable__ = ['name', 'email']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    join_date = db.Column(db.String(300), default='', nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    confirmed_email = db.Column(db.Boolean(), default=False, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.String(250), nullable=False)
    admin = db.Column(db.Boolean(), default=False, nullable=False)
    request_history = db.Column(MutableList.as_mutable(PickleType), nullable=False, default=[])
    membership = db.Column(MutableDict.as_mutable(PickleType), nullable=False,
                           default={"membership": None, "started_on": "", "end_on": ""})
    comments = relationship("Comment")
    replies = relationship("Reply")


class Book(db.Model):
    __tablename__ = "books"
    __searchable__ = ["author", "name", "category", "year"]
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(1000), nullable=False)
    name = db.Column(db.String(1000), unique=True, nullable=False)
    img = db.Column(db.String(250), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    price = db.Column(db.String(150), nullable=False)
    is_free = db.Column(db.Boolean(), nullable=False, default=True)
    url = db.Column(db.String(500), nullable=False)
    taken_by = db.Column(db.String(1000), nullable=False, default="")
    request_details = db.Column(MutableDict.as_mutable(PickleType), nullable=False,
                                default={"taken_on": "", "return_on": ""})
    category = db.Column(db.String(1000))
    comments = relationship("Comment", back_populates="parent_book")
    users_who_took = db.Column(db.Integer, nullable=False)


class BooksToReview(db.Model):
    __tablename__ = "books_to_review"
    __searchable__ = ["author", "name", "donated_by", "category", "year"]
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(1000), nullable=False)
    name = db.Column(db.String(500), unique=True, nullable=False)
    img = db.Column(db.String(500), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    price = db.Column(db.String(150), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    published = db.Column(db.Boolean(), nullable=False, default=False)
    donated_by = db.Column(db.String(1000), nullable=False)
    category = db.Column(db.String(1000))


class WebsiteSettings(db.Model):
    __tablename__ = "website_settings"
    id = db.Column(db.Integer, primary_key=True)
    json_column = db.Column(JSON, nullable=False, default={"secret_password": generate_password_hash(password="default",
                                                                                                     method='pbkdf2:sha256',
                                                                                                     salt_length=8),
                                                           "website_config": {
                                                               "name": "Library Management System",
                                                               "images": {
                                                                   "front_1": "https://www.detroitlabs.com/wp-content/uploads/2018/02/alfons-morales-YLSwjSy7stw-unsplash.jpg",
                                                                   "front_2": "https://cherwell.org/wp-content/uploads/2020/05/various-book-books.jpg",
                                                                   "front_3": "http://st2.depositphotos.com/2769299/7314/i/450/depositphotos_73146765-A-stack-of-books-on-the-shelf.jpg"
                                                               },
                                                               "welcome_txt": "Welcome, ",
                                                               "font": "https://fonts.googleapis.com/css2?family=KoHo:wght@500&display=swap",
                                                               "icon": "https://img.icons8.com/bubbles/2x/library.png",
                                                               "no_books": 5
                                                           },
                                                           "membership_config": {"gold": {
                                                               "image": "https://www.daytradeideas.co.uk/wp-content/uploads/2021/01/Circle_Design_Membership_Level_GOLD.png",
                                                               "price": {"monthly": "$40", "yearly": "$440"},
                                                               "benefits": [
                                                                   "Lend 6 books together ( No Membership: Only 1 Book )"]
                                                           }, "silver": {
                                                               "image": "https://www.secondchancewildlifesanctuary.org/wp-content/uploads/2016/10/silver-member.jpg",
                                                               "price": {"monthly": "$20", "yearly": "$275"},
                                                               "benefits": [
                                                                   "Lend 4 books together ( No Membership: Only 1 Book )"]
                                                           }, "bronze": {
                                                               "image": "http://www.secondchancewildlifesanctuary.org/wp-content/uploads/2016/10/bronze-member.jpg",
                                                               "price": {"monthly": "$15", "yearly": "$165"},
                                                               "benefits": [
                                                                   "Lend 2 books together ( No Membership: Only 1 Book )"]
                                                           }},
                                                           "donation_config": {
                                                               "2_books": "1 month of Free Bronze Membership",
                                                               "4_books": "1 month of Free Silver Membership",
                                                               "6_books": "1 month of Free Gold Membership"},
                                                           "footer_config": {
                                                               "twitter": "https://www.twitter.com",
                                                               "github": "https://www.github.com",
                                                               "facebook": "https://www.facebook.com",
                                                               "instagram": "https://www.instagram.com",
                                                               "youtube": "https://www.youtube.com",
                                                               "linkedin": "https://www.linkedin.com",
                                                               "dev": "https://dev.to",
                                                               "text": "© 2021 Learn Earn & Fun Inc. All Rights Reserved"
                                                           }, "menu": {
            "book": {
                "add_book": "Add New Book",
                "delete_book": "Delete a book",
                "update_book": "Update a book",
                "my_book": "My Books",
                "review_book": "Review a Book",
                "return_book": "Return a Book",
                "return_books": "Return all Books",
                "issue_book": "Rent a Book",
                "donate_book": "Donate a Book"
            }
        }})


class Reports(db.Model):
    __tablename__ = "reports"
    __searchable__ = ["month"]
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(250), nullable=False)
    money_by_books = db.Column(db.String(250), nullable=False)
    money_by_membership = db.Column(db.String(250), nullable=False)
    books_rented = db.Column(db.Integer, nullable=False)


class PaymentLogs(db.Model):
    __tablename__ = "payment_logs"
    id = db.Column(db.Integer, primary_key=True)
    payment_history = db.Column(MutableDict.as_mutable(PickleType), nullable=False, default=[])


class WebsiteLogs(db.Model):
    __tablename__ = "website_logs"
    id = db.Column(db.Integer, primary_key=True)
    website_history = db.Column(MutableDict.as_mutable(PickleType), nullable=False, default=[])


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="comments")
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    parent_book = relationship("Book", back_populates='comments')
    replies = relationship("Reply", back_populates='parent_comment')
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(250), nullable=False)


class Reply(db.Model):
    __tablename__ = 'replies'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="replies")
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"))
    parent_comment = relationship("Comment", back_populates='replies')
    reply = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(250), nullable=False)
