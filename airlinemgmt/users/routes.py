from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from airlinemgmt import db, bcrypt
from airlinemgmt.models import User, Booking
from airlinemgmt.users.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from airlinemgmt.users.utils import send_reset_email

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data,
                    email=form.email.data,
                    address=form.address.data,
                    pincode=form.pincode.data,
                    dob=form.dob.data,
                    phnum=form.phnum.data,
                    gender=form.gender.data,
                    password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if user.is_admin:
                return redirect(url_for('main.admin'))
            if user.is_employee:
                return redirect(url_for('emp.emphome'))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Check email and pwd', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/bookings")
@login_required
def bookings():
    user_bookings = Booking.query.filter_by(user=current_user)\
    .order_by(Booking.booking_time.desc())
    return render_template('user_bookings.html', bookings=user_bookings)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email sent with instruction to reset password', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid/expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash(f'Password updated for {user.email}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)



