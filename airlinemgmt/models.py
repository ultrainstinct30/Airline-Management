from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from airlinemgmt import db, login_manager
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    pincode = db.Column(db.String(6), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    phnum = db.Column(db.String(10))
    gender = db.Column(db.String(1))
    password = db.Column(db.String(60), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    @hybrid_property
    def age(self):
        today = datetime.today()
        return today.year - self.dob.year - ((today.month, today.day)<(self.dob.month, self.dob.day))

    def get_reset_token(self, expire_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expire_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.dob}')"


class Plane(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)
    mfd_date = db.Column(db.Date, nullable=False)
    engine_chk = db.Column(db.DateTime, nullable=False)
    fuel_chk = db.Column(db.DateTime, nullable=False)
    part_chk = db.Column(db.DateTime, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    flight = db.relationship('Flight', backref='plane', lazy=True, uselist=False)

    def __repr__(self):
        return f"Plane('{self.id}', '{self.name}', '{self.manufacturer}')"

class Airport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    num_terminals = db.Column(db.Integer, nullable=False)
    dpt_flights = db.relationship('Flight', backref='from_airport', foreign_keys="[Flight.from_id]", lazy=True)
    arrv_flights = db.relationship('Flight', backref='to_airport', foreign_keys="[Flight.to_id]", lazy=True)

    def __repr__(self):
        return f"Airport('{self.id}', '{self.name}', '{self.region}, '{self.city}', '{self.country}')"

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plane_id = db.Column(db.Integer, db.ForeignKey('plane.id'), nullable=False, unique=True)
    from_id = db.Column(db.Integer, db.ForeignKey('airport.id'), nullable=False)
    to_id = db.Column(db.Integer, db.ForeignKey('airport.id'), nullable=False)
    day = db.Column(db.String(15), nullable=False)
    depart_at = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Time, nullable=False)
    bookings = db.relationship('Booking', backref='flight', lazy=True)

    def __repr__(self):
        return f"Flight('{self.id}', '{self.from_id}', '{self.to_id}', '{self.day}')"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    travel_date = db.Column(db.Date, nullable=False)
    seat_no = db.Column(db.Integer, nullable=False)
    booking_time = db.Column(db.DateTime, nullable=False, server_default=func.now())

    def __repr__(self):
        return f"Booking('{self.id}', '{self.user_id}', '{self.flight_id}', '{self.seat_no}', '{self.travel_date}')"

