from flask import (Blueprint, render_template, url_for, redirect, request,
    flash)
from FlaskApp.models import Users
from flask_login import login_user, current_user, logout_user
from FlaskApp import bcrypt, db
from FlaskApp.users.forms import LoginForm, RSVPForm


users = Blueprint('users', __name__)


@users.route('/login', methods=['POST', 'GET'])
def login():
    # if the user is already logged in, redirect them to the home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data:
            user = Users.query.filter_by(email=form.email.data).first()
        elif form.number.data:
            user = Users.query.filter_by(number=form.number.data).first()
        # bcrypt method takes db query and form data as parameters to check
        # if the email provided is in the db, and the password they entered
        # matches the decoded password hash store, log them in
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # if user is trying to access a restricted page, they will be
            # prompted to login. Below gets their requested page and passes
            # it to below return ternary conditional
            next_page = request.args.get('next')
            flash(f'Hi {current_user.name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Cannot log in with those details. Check the details you entered are correct', 'danger')
    elif request.method == "GET":
        form.number.data = '+44'
    return render_template('login.html', title='Login', form=form)


@users.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# token argument is generated in the backend when the user is sent an invitation,
# password reset etc
@users.route('/welcome_page/<token>', methods=['POST', 'GET'])
def welcome_page(token):
    # return user to home page if they are already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # check that the token is correct, and not expired
    guest = Users.verify_reset_token(token)
    form = RSVPForm()
    if guest is None:
        flash('The link you were sent is either invalid or has expired. Please contact Kirk.', 'danger')
        return redirect(url_for('main.home'))
    else:
        # update user record in db to reflect their RSVP form values
        if form.validate_on_submit():
            guest.rsvp = True
            guest.email = form.email.data
            guest.number = form.number.data
            guest.is_attending = form.is_attending.data
            guest.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            db.session.commit()
            return redirect(url_for('main.home'))
        # prepopulate form fields with the values currently stored for the user
        elif request.method == 'GET':
            form.email.data = guest.email
            form.number.data = guest.number
        return render_template('welcome.html', title="Welcome To Our Wedding",
            form=form, guest=guest)
