from flask import render_template, request, Blueprint, flash, redirect, url_for, abort
from flask_login import current_user, login_required
from airlinemgmt import db, bcrypt
from airlinemgmt.models import User, Flight, Airport, Employee, Pilot, Plane, Booking, Status, Crew
from airlinemgmt.bookings.forms import SearchFlightForm
from airlinemgmt.main.forms import LoginForm, UpdateForm, RegistrationForm, PilotRegistrationForm, CrewRegistrationForm, FlightRegistrationForm, PlaneRegistrationForm, AirportRegistrationForm, StatusEntryForm 


main = Blueprint('main', __name__)

@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
    form = SearchFlightForm()
    if form.validate_on_submit():
        return redirect(url_for('bookings.result_flights', from_city=form.from_city.data, to_city=form.to_city.data))
    return render_template('home.html', flightsearchform=form)

@main.route("/admin")
@login_required
def admin():
    if not current_user.is_admin:
        abort(403)
    return render_template('admin_home.html')

@main.route("/admin/employees")
@login_required
def admin_employees():
    if not current_user.is_admin:
        abort(403)
    employees = Employee.query.all()
    return render_template('show_employees.html', employees=employees)

@main.route("/admin/planes")
@login_required
def admin_planes():
    if not current_user.is_admin:
        abort(403)
    planes = Plane.query.all()
    return render_template('show_planes.html', planes=planes)

@main.route("/admin/airports")
@login_required
def admin_airports():
    if not current_user.is_admin:
        abort(403)
    airports = Airport.query.all()
    return render_template('show_airports.html', airports=airports)

@main.route("/admin/flights")
@login_required
def admin_flights():
    if not current_user.is_admin:
        abort(403)
    flights = Flight.query.all()
    return render_template('show_flights.html', flights=flights)

@main.route("/admin/users")
@login_required
def admin_users():
    if not current_user.is_admin:
        abort(403)
    users = User.query.all()
    return render_template('show_users.html', users=users)

@main.route("/admin/bookings")
@login_required
def admin_bookings():
    if not current_user.is_admin:
        abort(403)
    bookings = Booking.query.all()
    return render_template('show_bookings.html', bookings=bookings)

@main.route("/admin/employee/<int:employee_id>")
@login_required
def show_employee(employee_id):
    if not current_user.is_admin:
        abort(403)
    employee = Employee.query.get_or_404(employee_id)
    return render_template('show_employees.html', employee=employee)

@main.route("/admin/plane/<int:plane_id>")
@login_required
def show_plane(plane_id):
    if not current_user.is_admin:
        abort(403)
    plane = Plane.query.get_or_404(plane_id)
    return render_template('show_plane.html', plane=plane)

@main.route("/admin/flight/<int:flight_id>")
@login_required
def show_flight(flight_id):
    if not current_user.is_admin:
        abort(403)
    flight = Flight.query.get_or_404(flight_id)
    return render_template('show_flight.html', flight=flight)

@main.route("/admin/user/<int:user_id>")
@login_required
def show_user(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)
    return render_template('show_user.html', user=user)

@main.route("/admin/booking/<int:booking_id>")
@login_required
def show_booking(booking_id):
    if not current_user.is_admin:
        abort(403)
    booking = Booking.query.get_or_404(booking_id)
    return render_template('show_booking.html', booking=booking)

@main.route("/admin/booking/<int:status_id>")
@login_required
def show_status(status_id):
    if not current_user.is_admin:
        abort(403)
    status = Status.query.get_or_404(status_id)
    return render_template('show_status.html', status=status)

@main.route("/admin/add-employees", methods=['GET', 'POST'])
@login_required
def add_employees():
    if not current_user.is_admin:
        abort(403)
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
        return redirect(url_for('main.add_employees'))
    return render_template('add_employee.html', form=form)

@main.route("/admin/add-planes", methods=['GET', 'POST'])
@login_required
def add_planes():
    if not current_user.is_admin:
        abort(403)
    form = PlaneRegistrationForm()
    if form.validate_on_submit():
        plane = Plane(  name=form.name.data,
                        manufacturer=form.manufacturer.data,
                        mfd_date=form.mfd_date.data,
                        engine_chk=form.engine_chk.data,
                        fuel_chk=form.fuel_chk.data,
                        part_chk=form.part_chk.data,
                        capacity=form.capacity.data)
        db.session.add(plane)
        db.session.commit()
        flash(f'Plane created {plane.id}!', 'success')
        return redirect(url_for('main.add_planes'))
    return render_template('add_plane.html', form=form)

@main.route("/admin/add-airports", methods=['GET', 'POST'])
@login_required
def add_airports():
    if not current_user.is_admin:
        abort(403)
    form = AirportRegistrationForm()
    if form.validate_on_submit():
        port = Airport( name=form.name.data,
                        region=form.region.data,
                        city=form.city.data,
                        country=form.country.data,
                        num_terminals=form.num_terminals.data)
        db.session.add(port)
        db.session.commit()
        flash(f'Airport created {port.id}!', 'success')
        return redirect(url_for('main.add_airports'))

    return render_template('add_airport.html', form=form)

@main.route("/admin/add-flights", methods=['GET', 'POST'])
@login_required
def add_flights():
    if not current_user.is_admin:
        abort(403)
    form = FlightRegistrationForm()
    if form.validate_on_submit():
        flight = Flight(plane_id=form.plane_id.data,
                        from_id=form.from_id.data,
                        to_id=form.to_id.data,
                        day=form.day.data,
                        depart_at=form.depart_at.data,
                        duration=form.duration.data)
        db.session.add(flight)
        db.session.commit()
        flash(f'Flight created {flight.id}!', 'success')
        return redirect(url_for('main.add_flights'))
    return render_template('add_flight.html', form=form)

@main.route("/admin/add-pilots", methods=['GET', 'POST'])
def add_pilots():
    if not current_user.is_admin:
        abort(403)
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
        db.session.add(pil)
        db.session.commit()
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('main.add_pilots'))
    return render_template('add_pilot.html', form=form)

@main.route("/admin/add-crews", methods=['GET', 'POST'])
def add_crews():
    if not current_user.is_admin:
        abort(403)
    form = CrewRegistrationForm()
    if form.validate_on_submit():

        crew = Crew(pilot_id=form.pilot_id.data,
                    copilot_id=form.copilot_id.data,
                    employee1_id=form.employee1_id.data,
                    employee2_id=form.employee2_id.data,
                    employee3_id=form.employee3_id.data,
                    )

        db.session.add(crew)
        db.session.commit()

        flash(f'Crew created {crew.id}!', 'success')
        return redirect(url_for('main.add_crews'))
    return render_template('add_crew.html', form=form)

@main.route("/admin/add-status", methods=['GET', 'POST'])
def add_status():
    if not current_user.is_admin:
        abort(403)
    form = StatusEntryForm()
    if form.validate_on_submit():

        status = Status(flight_id=form.flight_id.data,
                        crew_id=form.crew_id.data,
                        from_terminal=form.from_terminal.data,
                        to_terminal=form.to_terminal.data,
                        scheduled_time=form.scheduled_time.data,
                        actual_time=form.actual_time.data
                        )

        db.session.add(status)
        db.session.commit()

        flash(f'Status created {status.id}!', 'success')
        return redirect(url_for('main.add_status'))
    return render_template('add_status.html', form=form)


@main.route("/admin/employee-del/<int:employee_id>")
@login_required
def delete_employee(employee_id):
    if not current_user.is_admin:
        abort(403)
    employee = Employee.query.get_or_404(employee_id)
    pilot = employee.pilot
    user = employee.user
    if pilot is not None:
        db.session.delete(pilot)
    db.session.delete(employee)
    db.session.delete(user)
    db.session.commit()
    flash('Deleted!', 'success')
    return redirect(url_for('main.admin_employees'))

@main.route("/admin/plane-del/<int:plane_id>")
@login_required
def delete_plane(plane_id):
    if not current_user.is_admin:
        abort(403)
    plane = Plane.query.get_or_404(plane_id)
    db.session.delete(plane)
    db.session.commit()
    flash('Deleted!', 'success')
    return redirect(url_for('main.admin_planes'))

@main.route("/admin/flight-del/<int:flight_id>")
@login_required
def delete_flight(flight_id):
    if not current_user.is_admin:
        abort(403)
    flight = Flight.query.get_or_404(flight_id)
    db.session.delete(flight)
    db.session.commit()
    flash('Deleted!', 'success')
    return redirect(url_for('main.admin_flights'))

@main.route("/admin/user-del/<int:user_id>")
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Deleted!', 'success')
    return redirect(url_for('main.admin_users'))

@main.route("/admin/booking-del/<int:booking_id>")
@login_required
def delete_booking(booking_id):
    if not current_user.is_admin:
        abort(403)
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    flash('Deleted!', 'success')
    return redirect(url_for('main.admin_bookings'))

@main.route("/admin/status-del/<int:status_id>")
@login_required
def delete_status(status_id):
    if not current_user.is_admin:
        abort(403)
    status = Status.query.get_or_404(status_id)
    db.session.delete(status)
    db.session.commit()
    flash('Deleted!', 'success')
    return redirect(url_for('main.admin_status'))

@main.route("/admin/crew-del/<int:crew_id>")
@login_required
def delete_crew(crew_id):
    if not current_user.is_admin:
        abort(403)
    crew = Crew.query.get_or_404(crew_id)
    db.session.delete(crew)
    db.session.commit()
    flash('Deleted!', 'success')
    return redirect(url_for('main.admin_crew'))

@main.route("/admin/crew")
@login_required
def admin_crew():
    if not current_user.is_admin:
        abort(403)
    crew = Crew.query.all()
    return render_template('show_crews.html', crews=crew )

@main.route("/admin/airport-del/<int:airport_id>")
@login_required
def delete_airport(airport_id):
    if not current_user.is_admin:
        abort(403)
    airport = Airport.query.get_or_404(airport_id)
    db.session.delete(airport)
    db.session.commit()
    flash('Deleted!', 'success')
    return redirect(url_for('main.admin_airports'))

@main.route("/admin/status")
@login_required
def admin_status():
    if not current_user.is_admin:
        abort(403)
    status = Status.query.all()
    return render_template('show_status.html', status=status)