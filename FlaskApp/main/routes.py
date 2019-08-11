from flask import (Blueprint, render_template, request, redirect, url_for,
                    current_app)
from datetime import datetime
from FlaskApp.models import Photos
from werkzeug.utils import secure_filename
from flask_login import current_user
import os
from FlaskApp import db


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


@main.route('/photos')
def photos():
    photos = Photos.query.all()
    return render_template('photos.html', title="Wedding Photos",
        photos=photos)


@main.route('/upload-photo', methods=["POST", "GET"])
def upload_photo():
    return render_template('upload_photo.html')


@main.route('/upload-photo-confirm', methods=["POST", "GET"])
def upload_photo_confirm():
    file = request.files['img_file']
    all_photos = Photos.query.all()
    photos_length = len(all_photos)
    filename = f"kirk-vanela-wedding-{photos_length}"
    if current_user.is_authenticated:
        user = current_user.name
    else:
        user = "Anonymous"
    picture_path = os.path.join(current_app.root_path, 'static/photos', filename)
    file.save(picture_path)
    photo_upload = Photos(uploaded_by=user, file_name=filename)
    db.session.add(photo_upload)
    db.session.commit()
    print("NUMBER OF PHOTOS IS: " + str(photos_length))
    return redirect(url_for('main.photos'))
