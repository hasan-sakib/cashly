from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class ExpenseForm(FlaskForm):
    category_id  = SelectField("Category",    coerce=int, validators=[DataRequired()])
    amount       = DecimalField("Amount",     places=2,   validators=[DataRequired(), NumberRange(min=0.01)])
    currency     = SelectField("Currency",    choices=[("BDT","BDT"),("USD","USD"),("EUR","EUR"),("GBP","GBP")])
    description  = StringField("Description", validators=[DataRequired(), Length(1, 200)])
    note         = TextAreaField("Note",      validators=[Optional(), Length(max=500)])
    expense_date = DateField("Date",          validators=[DataRequired()])
