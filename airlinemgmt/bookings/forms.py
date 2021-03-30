from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField, IntegerField
from wtforms.fields.html5 import DateField, DateTimeLocalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_login import current_user
from airlinemgmt.models import User, Flight, Status
from datetime import date

days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']

class SearchFlightForm(FlaskForm):
    from_city = StringField('From', validators=[DataRequired()])
    to_city = StringField('To', validators=[DataRequired()])
    submit = SubmitField('Search')

class BookFlightForm(FlaskForm):
    flight_id = IntegerField('Flight No.', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=5, message='Passengers only over age of 5')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    travel_date = DateField('Travel on', validators=[DataRequired()])
    submit = SubmitField('Book')

    def validate_flight_id(self, flight_id):
        flight = Flight.query.filter_by(id=flight_id.data).first()
        if flight is None:
            raise ValidationError('Flight does not exist')

    def validate_travel_date(self, travel_date):
        flight = Flight.query.filter_by(id=self.flight_id.data).first()
        if flight is not None:
            if days[travel_date.data.weekday()] != flight.day:
                raise ValidationError('Flight does not travel on given date')

class StatusEntryForm(FlaskForm):
    flight_id = IntegerField('Flight No.', validators=[DataRequired()])
    crew_id = IntegerField('Crew ID', validators=[DataRequired()])
    from_terminal = IntegerField('From terminal', validators=[DataRequired()])
    to_terminal = IntegerField('To terminal', validators=[DataRequired()])
    scheduled_time = DateTimeLocalField('Scheduled Time', validators=[DataRequired()], format='%d-%m-%Y %H:%M:%S')
    actual_time = DateTimeLocalField('Actual Time', validators=[DataRequired()], format='%d-%m-%Y %H:%M:%S')
    submit = SubmitField('Submit')