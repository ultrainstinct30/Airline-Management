from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from airlinemgmt.models import Employee, User

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

