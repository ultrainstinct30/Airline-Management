from flask import render_template, request, Blueprint, flash, redirect, url_for
from airlinemgmt import db
from airlinemgmt.models import User, Flight, Airport
from airlinemgmt.bookings.forms import SearchFlightForm

main = Blueprint('main', __name__)

@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
    form = SearchFlightForm()
    if form.validate_on_submit():
        return redirect(url_for('bookings.resultFlights', from_city=form.from_city.data, to_city=form.to_city.data))
    return render_template('home.html', flightsearchform=form)

# @main.route("/about")
# def about():
#     return render_template('about.html', title='about')
