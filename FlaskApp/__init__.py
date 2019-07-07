from flask import Flask
from FlaskApp.config import Config
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from twilio.rest import Client
import os


mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


class Messaging():
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_phone = os.environ.get('TWILIO_FROM_PHONE')
    groom_phone = os.environ.get('TWILIO_TO_PHONE')
    client = Client(account_sid, auth_token)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from FlaskApp.main.routes import main
    from FlaskApp.users.routes import users
    from FlaskApp.admin.routes import admin

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(admin)

    return app
