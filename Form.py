from flask_wtf.file import FileRequired, FileAllowed
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField
from wtforms import TextAreaField, FileField
from wtforms.validators import Length, DataRequired, Regexp, Email
from flask_ckeditor import CKEditorField

from wtforms.validators import ValidationError
import re



class Form_Flask(Form):
    user_name = StringField("Username".capitalize(),
                            [validators.length(min=4, max=25)
                                , validators.DataRequired()])

    email = StringField('Email Address',
                        validators=[DataRequired(), Email(), Length(min=6, max=35)])

    full_name = StringField("Full Name".capitalize(),
                            [validators.length(min=4, max=25),
                             validators.DataRequired()])

    profile_picture = FileField("Upload Profile",
                                validators=[FileAllowed(['jpg', 'png'], 'Images only!')])

    password = PasswordField("Password", [
        validators.DataRequired(),
        validators.Length(min=8),
        validators.EqualTo("confirm", message="Passwords must match")
    ])
    submit = SubmitField("Submit")


class Profile(Form):
    name = StringField("name")
    bio = TextAreaField("Bio", validators=[Length(max=500)])
    submit = SubmitField("Submit")


class Create_post(Form):
    title = StringField("Title")
    subtitle = StringField("Subtitle")
    author = StringField("Author Name")
    content = CKEditorField('Content', validators=[DataRequired()])
    submit = SubmitField("Submit")


class CommentForm(Form):
    comment = StringField("Add a Note")
    add = SubmitField("Add")


class OTPForm(Form):
    otp = StringField('OTP', validators=[DataRequired()])
    submit = SubmitField('Verify OTP')
