from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from airlinemgmt import db, bcrypt
from airlinemgmt.models import User, Airport, Flight, Booking
from airlinemgmt.bookings.forms import SearchFlightForm, BookFlightForm
from datetime import date

bookings = Blueprint('bookings', __name__)

@bookings.route("/result_flights/from?<string:from_city>&to?<string:to_city>")
def result_flights(from_city, to_city):
    from_airport = Airport.query.filter_by(city=from_city).all()
    to_airport = Airport.query.filter_by(city=to_city).all()
    flights = []
    for fr_arpt in from_airport:
        for to_arpt in to_airport:
            flights += Flight.query.filter_by(from_airport=fr_arpt, to_airport=to_arpt).all()
    if flights == []:
        flash(f'No flights between {from_city} and {to_city}', 'info')
        return redirect(url_for('main.home'))

    return render_template('result_flights.html', flights=flights)

@bookings.route("/book_flight/<int:flight_id>", methods=['GET', 'POST'])
@login_required
def book_flight(flight_id):
    form = BookFlightForm()
    if form.validate_on_submit():
        flight = Flight.query.filter_by(id=flight_id).first()
        seat_no = len(Booking.query.filter_by(flight=flight).all())+1
        if seat_no > flight.plane.capacity:
            flash(f'No seats available for flight no. {flight_id}', 'danger')
            return redirect(url_for('bookings.result_flights', 
                                    from_city=flight.from_airport.city, 
                                    to_city=flight.to_airport.city))
        booking = Booking(flight_id=form.flight_id.data, user=current_user, 
                            name=form.name.data, age=form.age.data, 
                            email=form.email.data, travel_date=form.travel_date.data, 
                            seat_no=seat_no)
        db.session.add(booking)
        db.session.commit()
        flash(f'Seat booked for flight no {booking.flight_id}', 'success')
        return redirect(url_for('users.bookings'))
    if request.method == 'GET':
        form.flight_id.data = flight_id
        form.name.data = current_user.name
        form.age.data = current_user.age
        form.email.data = current_user.email
        form.travel_date.data = date.today()
    return render_template('book_flight.html', form=form)

@bookings.route("/cancel_booking/<int:booking_id>", methods=['GET', 'POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user != current_user:
        abort(403)
    db.session.delete(booking)
    db.session.commit()
    flash(f'Your booking for flight no {booking.flight_id} has been deleted', 'success')
    return redirect(url_for('users.bookings'))

