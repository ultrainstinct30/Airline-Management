from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from airlinemgmt.models import User, Flight

class SearchFlightForm(FlaskForm):
    from_city = StringField('From', validators=[DataRequired()])
    to_city = StringField('To', validators=[DataRequired()])
    submit = SubmitField('Search')

