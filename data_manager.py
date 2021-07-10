from werkzeug.security import generate_password_hash

from extensions import db
from models import WebsiteSettings


def get_data():  # GET CONFIG DATA
    try:
        data = WebsiteSettings.query.all()[0].json_column
        return data
    except:
        set_default()
        data = WebsiteSettings.query.all()[0].json_column
        return data


def set_default():
    default_data = {"secret_password": generate_password_hash(password="default",
                                                              method='pbkdf2:sha256', salt_length=8),
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
        }}
    update_data(default_data)


def update_data(given_data):
    new_data = WebsiteSettings(json_column=given_data)
    if len(WebsiteSettings.query.all()) > 0 and WebsiteSettings.query.all()[0] is not None:
        db.session.delete(WebsiteSettings.query.all()[0])
    db.session.add(new_data)
    db.session.commit()
