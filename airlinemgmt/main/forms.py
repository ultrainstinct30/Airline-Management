from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField, IntegerField
from wtforms.fields.html5 import DateField, TimeField, DateTimeLocalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from airlinemgmt.models import Employee, User, Pilot, Crew, Status

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UpdateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', validators=[DataRequired()])
    pincode = StringField('Pincode', validators=[DataRequired(), Length(min=6, max=6)])
    phnum = StringField('Phone number', validators=[Length(min=10, max=10)])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female'), ('X', 'Rather Not Say')])
    submit = SubmitField('Update')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email taken')

class RegistrationForm(FlaskForm):
    name = StringField('Name (*)', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    email = StringField('Email (*)', validators=[DataRequired(), Email()])
    address = TextAreaField('Address (*)', validators=[DataRequired()])
    pincode = StringField('Pincode (*)', validators=[DataRequired(), Length(min=6, max=6)])
    dob = DateField('Date of Birth (*)', validators=[DataRequired()])
    phnum = StringField('Phone number', validators=[Length(min=10, max=10)])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female'), ('x', 'Rather not say')])
    password = PasswordField('Password (*)', validators=[DataRequired()])
    joining_date = DateField('Date of Joining', validators=[DataRequired()])
    salary = StringField('Salary', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password (*)', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email taken')

class PilotRegistrationForm(FlaskForm):
    name = StringField('Name (*)', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    email = StringField('Email (*)', validators=[DataRequired(), Email()])
    address = TextAreaField('Address (*)', validators=[DataRequired()])
    pincode = StringField('Pincode (*)', validators=[DataRequired(), Length(min=6, max=6)])
    dob = DateField('Date of Birth (*)', validators=[DataRequired()])
    phnum = StringField('Phone number', validators=[Length(min=10, max=10)])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female'), ('x', 'Rather not say')])
    password = PasswordField('Password (*)', validators=[DataRequired()])
    joining_date = DateField('Date of Joining', validators=[DataRequired()])
    salary = StringField('Salary', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password (*)', validators=[DataRequired(), EqualTo('password')])
    licence_no = IntegerField('Licence No.', validators=[DataRequired()])
    experience = IntegerField('Experience', validators=[DataRequired()])
    rank = SelectField('Rank', choices=[('J', 'Junior'), ('S', 'Senior')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email taken')

class CrewRegistrationForm(FlaskForm):
    pilot_id = IntegerField('Pilot ID', validators=[DataRequired()])
    copilot_id = IntegerField('Co-Pilot ID', validators=[DataRequired()])
    employee1_id = IntegerField('Employee1 ID', validators=[DataRequired()])
    employee2_id = IntegerField('Employee2 ID', validators=[DataRequired()])
    employee3_id = IntegerField('Employee3 ID', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class FlightRegistrationForm(FlaskForm):
    plane_id = IntegerField('Plane No.', validators=[DataRequired()])
    from_id = IntegerField('From Airport', validators=[DataRequired()])
    to_id = IntegerField('To Airport', validators=[DataRequired()])
    day = SelectField('Day', choices=[('MONDAY', 'MONDAY'), ('TUESDAY', 'TUESDAY'), ('WEDNESDAY', 'WEDNESDAY'), ('THURSDAY', 'THURSDAY'), ('FRIDAY', 'FRIDAY'), ('SATURDAY', 'SATURDAY'), ('SUNDAY', 'SUNDAY')])
    depart_at = TimeField('Usual Departure Time', validators=[DataRequired()], format='%H:%M:%S')
    duration = TimeField('Usual Flight Duration', validators=[DataRequired()], format='%H:%M:%S')
    submit = SubmitField('Submit')
    

class PlaneRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    manufacturer = StringField('Manufacturer', validators=[DataRequired()])
    mfd_date = DateField('Manufacturing Date', validators=[DataRequired()])
    engine_chk = DateTimeLocalField('Last Engine Check', validators=[DataRequired()], format='%d-%m-%Y %H:%M:%S')
    fuel_chk = DateTimeLocalField('Last Fuel Check', validators=[DataRequired()], format='%d-%m-%Y %H:%M:%S')
    part_chk = DateTimeLocalField('Last Part Check', validators=[DataRequired()], format='%d-%m-%Y %H:%M:%S')
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AirportRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    region = StringField('Region', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    num_terminals = IntegerField('No. of Terminals', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class StatusEntryForm(FlaskForm):
    flight_id = IntegerField('Flight No.', validators=[DataRequired()])
    crew_id = IntegerField('Crew ID', validators=[DataRequired()])
    from_terminal = IntegerField('From terminal', validators=[DataRequired()])
    to_terminal = IntegerField('To terminal', validators=[DataRequired()])
    scheduled_time = DateTimeLocalField('Scheduled Time', validators=[DataRequired()], format='%d-%m-%Y %H:%M:%S')
    actual_time = DateTimeLocalField('Actual Time', validators=[DataRequired()], format='%d-%m-%Y %H:%M:%S')
    submit = SubmitField('Submit')

