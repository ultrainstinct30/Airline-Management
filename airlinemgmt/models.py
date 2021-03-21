from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from airlinemgmt import db, login_manager
from sqlalchemy.ext.hybrid import hybrid_property

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

