from flask import render_template, url_for, flash, redirect, request, Blueprint, request
from flask_login import login_user, current_user, logout_user, login_required
from airlinemgmt import db, bcrypt
from airlinemgmt.models import Employee, User
from airlinemgmt.employee.forms import LoginForm, UpdateForm, RegistrationForm, PilotRegistrationForm
# from airlinemgmt.employee.utils import send_reset_email

emp = Blueprint('emp', __name__)

@emp.route("/emplogin", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        emp = Employee.query.filter_by(email=form.email.data).first()
        if emp and bcrypt.check_password_hash(emp.password, form.password.data):
            login_user(emp, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Check email and pwd', 'danger')
    return render_template('emplogin.html', title='EmpLogin', form=form)

@emp.route("/empupdate", methods=['GET', 'POST'])
@login_required
def update():
    form = UpdateForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.pincode = form.pincode.data
        current_user.phnum = form.phnum.data
        current_user.gender = form.gender.data
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.pincode.data = current_user.pincode
        form.phnum.data = current_user.phnum
        form.gender.data = current_user.gender
    else:
        flash('Unable to update', 'danger')
    return render_template('empupdate.html', title='EmpUpdate', form=form)


@emp.route("/empregister", methods=['GET', 'POST'])
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
                    password=hashed_pw,
                    is_employee=True)
        db.session.add(user)
        db.session.commit()
        empl = Employee(id=user.id,
                        position=form.position.data,
                        joining_date=form.joining_date.data,
                        salary=form.salary.data)
        db.session.add(empl)
        db.session.commit()
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('user.login'))
    return render_template('empregister.html', title='Register', form=form)


@emp.route("/pilotregister", methods=['GET', 'POST'])
def piltregister():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = PilotRegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data,
                    email=form.email.data,
                    address=form.address.data,
                    pincode=form.pincode.data,
                    dob=form.dob.data,
                    phnum=form.phnum.data,
                    gender=form.gender.data,
                    password=hashed_pw,
                    is_employee=True)
        db.session.add(user)
        db.session.commit()
        empl = Employee(id=user.id,
                        position=form.position.data,
                        joining_date=form.joining_date.data,
                        salary=form.salary.data)
        db.session.add(empl)
        db.session.commit()
        pil = Pilot(id=empl.id,
                    licence_no=form.licence_no.data,
                    experience=form.experience.data,
                    rank=form.rank.data)
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('user.login'))
    return render_template('pilotregister.html', title='Register', form=form)
