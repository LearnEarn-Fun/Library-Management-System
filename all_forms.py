from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, URL
from flask_wtf import FlaskForm


class CreateBookForm(FlaskForm):
    title = StringField("Book Name", validators=[DataRequired()])

    author = StringField("Book Author ", validators=[DataRequired()])

    img_url = StringField("Book Image URL ", validators=[DataRequired(),
                                                         URL()])

    year = StringField("Published Date of Book ", validators=[DataRequired()])

    price = StringField("Price of Book ", validators=[DataRequired()])

    book_url = StringField("Book PDF URL", validators=[DataRequired(), URL()])

    category = StringField("Categories of Book", validators=[DataRequired()])

    submit = SubmitField("Submit Book")


class ForgetPasswordForm(FlaskForm):
    new_password = PasswordField("Enter your new password:", validators=[DataRequired()])
    submit = SubmitField("Submit", render_kw={"style": "margin-top: 20px;"})


class ForgetHandlingForm(FlaskForm):
    email = StringField("Enter your email address:", validators=[DataRequired(), Email()])
    submit = SubmitField("Proceed", render_kw={"style": "margin-top: 20px;"})

class DeleteBookForm(FlaskForm):
    title = StringField("Book Name ", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UpdateBookForm(FlaskForm):
    name = StringField("Book Name", validators=[DataRequired()])

    author = StringField("Book Author", validators=[DataRequired()])

    img = StringField("Book Image URL", validators=[URL(), DataRequired()])

    year = StringField("Published Date of Book", validators=[DataRequired()])

    price = StringField("Price of Book", validators=[DataRequired()])

    url = StringField("URL of Book ( PDF )", validators=[DataRequired()])

    category = StringField("Categories of Book", validators=[DataRequired()])

    submit = SubmitField("Update Book")


class ReviewBookForm(FlaskForm):
    name = StringField("Book Name", validators=[DataRequired()])

    author = StringField("Book Author ", validators=[DataRequired()])

    img = StringField("Book Image URL ", validators=[DataRequired(),
                                                         URL()])

    year = StringField("Published Date of Book ", validators=[DataRequired()])

    price = StringField("Price of Book ", validators=[DataRequired()])

    url = StringField("Book PDF URL", validators=[DataRequired(), URL()])

    category = StringField("Categories of Book", validators=[DataRequired()])

    accept_decline = SelectField("Accept / Decline", choices=["Accept", "Decline"], validators=[DataRequired()])

    submit = SubmitField("Submit Book")


class SearchForm(FlaskForm):
    category = SelectField('Search By', choices=['Books', 'Users'], validators=[DataRequired()])
    search = StringField('Search Query', validators=[DataRequired()],
                         description="You can write any detail about the book or user, The search will bring it for you!")
    submit = SubmitField("Search!")


class WebsiteConfig(FlaskForm):
    name = StringField('Website Name', validators=[DataRequired()])
    font = StringField('Website Font ( Google Fonts URL )', validators=[DataRequired()])
    welcoming_txt = StringField('Welcoming text', validators=[DataRequired()])
    no_books = StringField('Number of Books', validators=[DataRequired()])
    icon = StringField('Website Icon', validators=[DataRequired()])
    i1 = StringField('Front Image 1 ( URL )', validators=[DataRequired(), URL()])
    i2 = StringField('Front Image 2 ( URL )', validators=[DataRequired(), URL()])
    i3 = StringField('Front Image 3 ( URL )', validators=[DataRequired(), URL()])
    submit = SubmitField("Submit!")


class FooterConfig(FlaskForm):
    twitter = StringField('Twitter URL', validators=[DataRequired(), URL()])
    facebook = StringField('Facebook URL', validators=[DataRequired(), URL()])
    youtube = StringField('YouTube URL', validators=[DataRequired(), URL()])
    instagram = StringField('Instagram URL', validators=[DataRequired(), URL()])
    linkedin = StringField('LinkedIn URL', validators=[DataRequired(), URL()])
    github = StringField('Github URL', validators=[DataRequired(), URL()])
    dev = StringField('Dev.to URL', validators=[DataRequired(), URL()])
    text = StringField('Footer Text', validators=[DataRequired()])
    submit = SubmitField("Submit!")


class BookDropdownMenu(FlaskForm):
    add_book = StringField('Add Book Name', validators=[DataRequired()])
    delete_book = StringField('Delete Book Name', validators=[DataRequired()])
    update_book = StringField('Update Book Name', validators=[DataRequired()])
    review_book = StringField('Review Book Name', validators=[DataRequired()])
    my_book = StringField('My Books Name', validators=[DataRequired()])
    donate_book = StringField('Donate Book Name', validators=[DataRequired()])
    rent_book = StringField('Rent Book Name', validators=[DataRequired()])
    return_book = StringField('Return Book Name', validators=[DataRequired()])
    return_books = StringField('Return All Book Name', validators=[DataRequired()])
    submit = SubmitField("Submit!")


class EditProfileForm(FlaskForm):
    name = StringField("Name ", validators=[DataRequired()])
    email = StringField("Email ", validators=[DataRequired(),
                                              Email()])
    address = StringField("Address ", validators=[DataRequired()])
    image = StringField('Profile Picture URL', validators=[DataRequired()])
    submit = SubmitField("Update Details!")


class RegisterForm(FlaskForm):
    name = StringField("Name ", validators=[DataRequired()])
    email = StringField("Email ", validators=[DataRequired(),
                                              Email()])
    password = PasswordField("Password ", validators=[DataRequired(),
                                                      Length(min=8, max=16)])
    confirm = PasswordField('Repeat Password ', validators=[DataRequired(),
                                                            EqualTo('password'),
                                                            Length(min=8, max=16)])
    address = StringField("Address ", validators=[DataRequired()])
    picture = StringField('Profile Picture URL', validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


class LoginForm(FlaskForm):
    email = StringField("Email ", validators=[DataRequired(),
                                              Email()])
    password = PasswordField("Password ", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comment ", validators=[DataRequired()])
    rating = SelectField("Book Rating: ", choices=['5', '4', '3', '2', '1'], validators=[DataRequired()])
    submit = SubmitField("Submit Comment")


class ReplyForm(FlaskForm):
    reply = CKEditorField("Reply", validators=[DataRequired()])
    submit = SubmitField("Submit Reply")


class EditReplyForm(FlaskForm):
    reply = CKEditorField("Edit Reply", validators=[DataRequired()])
    submit = SubmitField("Save Changes")


class EditCommentForm(FlaskForm):
    comment = CKEditorField("Edit Comment", validators=[DataRequired()])
    rating = SelectField("Book Rating: ", choices=['5', '4', '3', '2', '1'], validators=[DataRequired()])
    submit = SubmitField("Save Changes")
