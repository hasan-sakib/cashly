from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    username = StringField("Username",        validators=[DataRequired(), Length(3, 30)])
    email    = EmailField("Email address",    validators=[DataRequired(), Email()])
    password = PasswordField("Password",      validators=[DataRequired(), Length(8, 128)])
    confirm  = PasswordField("Confirm password", validators=[
        DataRequired(), EqualTo("password", message="Passwords must match.")
    ])


class LoginForm(FlaskForm):
    email    = EmailField("Email address", validators=[DataRequired(), Email()])
    password = PasswordField("Password",   validators=[DataRequired()])
