from flask import current_app
from FlaskApp import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    number = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    rsvp = db.Column(db.Boolean, default=False)
    is_attending = db.Column(db.String, default='Unsure')
    additional_guests = db.Column(db.Integer)
    additional_guest_names = db.Column(db.String)
    guest_type = db.Column(db.String)
    language = db.Column(db.String)

    def __repr__(self):
        return f'''User(Name: '{self.name}', Email: '{self.email}', RSVPed? '{self.rsvp}',
        Additional Guests: '{self.additional_guests}', Guest Type: '{self.guest_type}',
        Guest Language: '{self.language}')'''

    # generate a unique token, to be appended to invitation URL, password resets etc
    def get_reset_token(self, expires_sec=604800):
        # set up token with app's key and expiration time (604,800=1 week)
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # verify unique token when the user visits invitation URL, password reset etc
    # below decorator tells Python not to expect 'self' parameter as an arg
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Users.query.get(user_id)


class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    notes = db.Column(db.Text)
    cost = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Float, nullable=False, default=0.00)
    cost_type = db.Column(db.String, nullable=False)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text)
