from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired, Length


class ProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3, 30)])
    currency = SelectField("Default currency", choices=[
        ("BDT", "BDT — Bangladeshi Taka"),
        ("USD", "USD — US Dollar"),
        ("EUR", "EUR — Euro"),
        ("GBP", "GBP — British Pound"),
    ])
    theme    = SelectField("Theme", choices=[
        ("light",  "Light"),
        ("dark",   "Dark"),
        ("system", "System default"),
    ])
