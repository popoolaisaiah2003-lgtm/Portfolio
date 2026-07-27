from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(max=100)])
    email = EmailField("Email Address", validators=[DataRequired(), Email(), Length(max=254)])
    subject = StringField("Subject", validators=[DataRequired(), Length(max=150)])
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=10, max=3000)])
    submit = SubmitField("Send Message")