from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from airlinemgmt import db, bcrypt
from airlinemgmt.models import User, Airport, Flight
from airlinemgmt.bookings.forms import SearchFlightForm

bookings = Blueprint('bookings', __name__)

@bookings.route("/resultFlights/from?<string:from_city>&to?<string:to_city>")
def resultFlights(from_city, to_city):
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
