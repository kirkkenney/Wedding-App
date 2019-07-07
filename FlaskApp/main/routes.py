from flask import (Blueprint, render_template)
from datetime import datetime


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    wedding_date = datetime(2020, 2, 12)
    today = datetime.today()
    countdown = wedding_date - today
    return render_template('home.html', title='Home',
            wedding_date=wedding_date,
            countdown=countdown)
