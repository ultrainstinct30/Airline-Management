from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField, IntegerField
from wtforms.fields.html5 import DateField, DateTimeLocalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_login import current_user
from airlinemgmt.models import User, Flight, Status
from datetime import datetime

class FlightRegistrationForm(FlaskForm):
    plane_id = IntegerField('Plane No.', validators=[DataRequired()])
    from_id = IntegerField('From Airport', validators=[DataRequired()])
    to_id = IntegerField('To Airport', validators=[DataRequired()])
    day = SelectField('Day', choices=[('MONDAY', 'MONDAY'), ('TUESDAY', 'TUESDAY'), ('WEDNESDAY', 'WEDNESDAY'), ('THURSDAY', 'THURSDAY'), ('FRIDAY', 'FRIDAY'), ('SATURDAY', 'SATURDAY'), ('SUNDAY', 'SUNDAY')])
    depart_at = TimeField('Usual Departure Time', validators=[DataRequired()], format='%H:%M:%S')
    duration = TimeField('Usual Flight Duration', validators=[DataRequired()], format='%H:%M:%S')
    

class PlaneRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    manufacturer = StringField('Manufacturer', validators=[DataRequired()])
    mfd_date = DateField('Manufacturer', validators=[DataRequired()])
    engine_chk = DateTimeLocalField('Last Engine Check', validators=[DataRequired()], format='%d-%m-%Y %H:%M:%S')
    fuel_chk = DateTimeLocalField('Last Fuel Check', validators=[DataRequired()], format='%d-%m-%Y %H:%M:%S')
    part_chk = DateTimeLocalField('Last Part Check', validators=[DataRequired()], format='%d-%m-%Y %H:%M:%S')
    capacity = IntegerField('Capacity', validators=[DataRequired()])


class AirportRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    region = StringField('Region', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    num_terminals = IntegerField('No. of Terminals', validators=[DataRequired()])