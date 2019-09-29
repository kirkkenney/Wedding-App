from flask import (Blueprint, render_template, url_for, redirect, request,
    flash)
from FlaskApp.models import Users
from flask_login import login_user, current_user, logout_user, login_required
from FlaskApp import bcrypt, db, Messaging
from FlaskApp.users.forms import LoginForm, RSVPForm, RequestResetForm, ResetPasswordForm


users = Blueprint('users', __name__)


@users.route('/login', methods=['POST', 'GET'])
def login():
    # if the user is already logged in, redirect them to the home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.number.data:
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
        form.number.data = '+4'
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
            guest.is_attending = form.is_attending.data
            guest.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            db.session.commit()
            login_user(guest)
            return redirect(url_for('main.home'))
        return render_template('welcome.html', title="Welcome To Our Wedding",
            form=form, guest=guest)


@users.route('/reset_password', methods=['POST', 'GET'])
def reset_request():
    # check that user is not currently logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if request.method == 'GET':
        form.number.data = '+4'
    if form.validate_on_submit():
        print(form.number.data)
        user = Users.query.filter_by(number=form.number.data).first()
        send_reset_sms(user)
        flash('A text message has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

def send_reset_sms(user):
    # if user wants to reset their password, query call get_reset_token
    # function in User db model, and send them a text
    token = user.get_reset_token()
    msg = Messaging.client.messages.create(
        body=f'''Hi {user.name} a request to reset your password has been sent.\n
        If this was made by you, please visit the below link to reset your password.
        {url_for('users.reset_token', token=token, _external=True)}''',
        from_=Messaging.from_phone,
        to=user.number
    )

@users.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # call method from User class of models.py
    user = Users.verify_reset_token(token)
    if user is None:
        flash('Password reset has expired or is invalid. Please try again.', 'warning')
        return redirect(url_for('users.reset_request'))
    # if user is valid:
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # take password value and hash it using bcrypt
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated. You are now able to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route('/invite-guest/<string:guest_name>')
@login_required
def invite_guest(guest_name):
    # page restricted to admins. Redirect is user is not an admin (bride/groom)
    if current_user.guest_type != 'Admin':
        return redirect(url_for('main.home'))
    guest = Users.query.filter_by(name=guest_name).first()
    if guest.number.startswith('+4'):
        send_invite_sms(guest)
        flash(f'Invitation sent to {guest.name}', 'success')
        return redirect(url_for('admin.dashboard'))
    else:
        send_error_sms(guest)
        flash(f'An error occurred sending an invitation to {guest.name}', 'warning')
        return redirect(url_for('admin.dashboard'))

def send_invite_sms(guest):
    token = guest.get_reset_token()
    message = Messaging.client.messages.create(
        body=f'''Hi {guest.name}, you've been invited to Kirk & Vanela's Wedding'''
            +'\nPlease visit the below link to RSVP and find other info about the day.'
            +'\nHope to see you then!'
            +'\nKirk and Vanela.'
            +f'''\n{url_for('users.welcome_page', token=token, _external=True)}''',
        from_=Messaging.from_phone,
        to=guest.number
        )

def send_error_sms(guest):
    msg = Messaging.client.messages.create(
        body=f'''{guest.name} was supposed to receive an invitation, but an error occurred.
        Please check that they have a phone number stored.''',
        from_=Messaging.from_phone,
        to=Messaging.groom_phone
        )
