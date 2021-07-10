from flask import Blueprint, flash
from data_manager import get_data, update_data, set_default
from utils import handle_page, admin_only
from flask_login import login_required
from werkzeug.security import generate_password_hash
from all_forms import WebsiteConfig, BookDropdownMenu, FooterConfig

settings = Blueprint('settings', __name__, url_prefix="/settings")


@settings.route("/", methods=['GET', 'POST'])
@login_required
@admin_only
def setting():
    return handle_page('settings.html')


@settings.route("/reset", methods=['GET', 'POST'])
@login_required
@admin_only
def reset_settings():
    set_default()
    flash("Successfully Reset all the settings!", "success")
    return handle_page('success.html')


@settings.route("/update/website_config", methods=['GET', 'POST'])
@login_required
@admin_only
def update_website_config():
    data = get_data()['website_config']
    form = WebsiteConfig(name=data['name'], welcoming_txt=data['welcome_txt'],
                         no_books=data['no_books'], icon=data['icon'], font=data['font'], i1=data['images']['front_1'],
                         i2=data['images']['front_2'], i3=data['images']['front_3'])
    if form.validate_on_submit():
        update_data({"secret_password": generate_password_hash(password="default",
                                                               method='pbkdf2:sha256',
                                                               salt_length=8),
                     "website_config": {
                         "name": form.name.data,
                         "images": {
                             "front_1": form.i1.data,
                             "front_2": form.i2.data,
                             "front_3": form.i3.data
                         },
                         "welcome_txt": form.welcoming_txt.data,
                         "font": form.font.data,
                         "icon": form.icon.data,
                         "no_books": form.no_books.data
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
                         "twitter": get_data()["footer_config"]['twitter'],
                         "github": get_data()["footer_config"]['github'],
                         "facebook": get_data()["footer_config"]['facebook'],
                         "instagram": get_data()["footer_config"]['instagram'],
                         "youtube": get_data()["footer_config"]['youtube'],
                         "linkedin": get_data()["footer_config"]['linkedin'],
                         "dev": get_data()["footer_config"]['dev'],
                         "text": get_data()["footer_config"]['text']
                     }, "menu": {
                "book": {
                    "add_book": get_data()['menu']["book"]['add_book'],
                    "delete_book": get_data()['menu']["book"]['delete_book'],
                    "update_book": get_data()['menu']["book"]['update_book'],
                    "my_book": get_data()['menu']["book"]['my_book'],
                    "review_book": get_data()['menu']["book"]['review_book'],
                    "return_book": get_data()['menu']["book"]['return_book'],
                    "return_books": get_data()['menu']["book"]['return_books'],
                    "issue_book": get_data()['menu']["book"]['issue_book'],
                    "donate_book": get_data()['menu']["book"]['donate_book']
                }
            }})
        flash('You have successfully updated the website settings', 'success')
        return handle_page('success.html')
    return handle_page('form.html', form=form, title="Update Website Settings")


@settings.route("/update/book_menu_config", methods=['GET', 'POST'])
@login_required
@admin_only
def update_book_menu_config():
    data = get_data()['menu']['book']
    form = BookDropdownMenu(add_book=data['add_book'], delete_book=data['delete_book'],
                            update_book=data['update_book'], review_book=data['review_book'], my_book=data['my_book'],
                            donate_book=data['donate_book'], rent_book=data['issue_book'], return_book=data['return_book'],
                            return_books=data['return_books'])
    if form.validate_on_submit():
        update_data({"secret_password": generate_password_hash(password="default",
                                                               method='pbkdf2:sha256',
                                                               salt_length=8),
                     "website_config": {
                         "name": get_data()['website_config']['name'],
                         "images": {
                             "front_1": get_data()['website_config']['images']['front_1'],
                             "front_2": get_data()['website_config']['images']['front_2'],
                             "front_3": get_data()['website_config']['images']['front_3']
                         },
                         "welcome_txt": get_data()['website_config']['welcome_txt'],
                         "font": get_data()['website_config']['font'],
                         "icon": get_data()['website_config']['icon'],
                         "no_books": get_data()['website_config']['no_books']
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
                         "twitter": get_data()["footer_config"]['twitter'],
                         "github": get_data()["footer_config"]['github'],
                         "facebook": get_data()["footer_config"]['facebook'],
                         "instagram": get_data()["footer_config"]['instagram'],
                         "youtube": get_data()["footer_config"]['youtube'],
                         "linkedin": get_data()["footer_config"]['linkedin'],
                         "dev": get_data()["footer_config"]['dev'],
                         "text": get_data()["footer_config"]['text']
                     }, "menu": {
                "book": {
                    "add_book": form.add_book.data,
                    "delete_book": form.delete_book.data,
                    "update_book": form.update_book.data,
                    "my_book": form.my_book.data,
                    "review_book": form.review_book.data,
                    "return_book": form.return_book.data,
                    "return_books": form.return_books.data,
                    "issue_book": form.rent_book.data,
                    "donate_book": form.donate_book.data
                }
            }})
        flash('You have successfully updated the book menu settings', 'success')
        return handle_page('success.html')
    return handle_page('form.html', form=form, title="Update Book Menu Settings")


@settings.route("/update/footer_config", methods=['GET', 'POST'])
@login_required
@admin_only
def update_footer_config():
    data = get_data()['footer_config']
    form = FooterConfig(twitter=data['twitter'], facebook=data['facebook'], github=data['github'], youtube=data['youtube'],
                        instagram=data['instagram'], linkedin=data['linkedin'], dev=data['dev'], text=data['text'])
    if form.validate_on_submit():
        update_data({"secret_password": generate_password_hash(password="default",
                                                               method='pbkdf2:sha256',
                                                               salt_length=8),
                     "website_config": {
                         "name": get_data()['website_config']['name'],
                         "images": {
                             "front_1": get_data()['website_config']['images']['front_1'],
                             "front_2": get_data()['website_config']['images']['front_2'],
                             "front_3": get_data()['website_config']['images']['front_3']
                         },
                         "welcome_txt": get_data()['website_config']['welcome_txt'],
                         "font": get_data()['website_config']['font'],
                         "icon": get_data()['website_config']['icon'],
                         "no_books": get_data()['website_config']['no_books']
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
                         "twitter": form.twitter.data,
                         "github": form.github.data,
                         "facebook": form.facebook.data,
                         "instagram": form.instagram.data,
                         "youtube": form.youtube.data,
                         "linkedin": form.linkedin.data,
                         "dev": form.dev.data,
                         "text": form.text.data
                     }, "menu": {
                "book": {
                    "add_book": get_data()['menu']["book"]['add_book'],
                    "delete_book": get_data()['menu']["book"]['delete_book'],
                    "update_book": get_data()['menu']["book"]['update_book'],
                    "my_book": get_data()['menu']["book"]['my_book'],
                    "review_book": get_data()['menu']["book"]['review_book'],
                    "return_book": get_data()['menu']["book"]['return_book'],
                    "return_books": get_data()['menu']["book"]['return_books'],
                    "issue_book": get_data()['menu']["book"]['issue_book'],
                    "donate_book": get_data()['menu']["book"]['donate_book']
                }
            }})
        flash('You have successfully updated the website settings', 'success')
        return handle_page('success.html')
    return handle_page('form.html', form=form, title="Update Website Settings")