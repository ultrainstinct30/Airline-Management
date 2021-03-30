from flask import render_template, request, Blueprint, flash, redirect, url_for, abort
from flask_login import current_user, login_required
from airlinemgmt import db
from airlinemgmt.models import User, Flight, Airport, Employee, Pilot, Plane, Booking
from airlinemgmt.bookings.forms import SearchFlightForm

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

@main.route("/admin/add-employees")
@login_required
def add_employees():
    if not current_user.is_admin:
        abort(403)
    bookings = Booking.query.all()
    return render_template('add_employee.html', bookings=bookings)

@main.route("/admin/add-planes")
@login_required
def add_planes():
    if not current_user.is_admin:
        abort(403)
    bookings = Booking.query.all()
    return render_template('add_plane.html', bookings=bookings)

@main.route("/admin/add-airports")
@login_required
def add_airports():
    if not current_user.is_admin:
        abort(403)
    bookings = Booking.query.all()
    return render_template('add_airport.html', bookings=bookings)

@main.route("/admin/add-flights")
@login_required
def add_flights():
    if not current_user.is_admin:
        abort(403)
    bookings = Booking.query.all()
    return render_template('add_flight.html', bookings=bookings)

@main.route("/admin/employee-del/<int:employee_id>")
@login_required
def delete_employee(employee_id):
    if not current_user.is_admin:
        abort(403)
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
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