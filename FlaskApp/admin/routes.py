from flask import (Blueprint, render_template, redirect, url_for, flash,
                    request)
from flask_login import current_user, login_required
from FlaskApp.models import Users, Expenses, Tasks
from FlaskApp.admin.forms import (AddGuestForm, EditGuestForm, AddExpensesForm,
                                EditExpensesForm, UpdatePaymentForm)
from FlaskApp import bcrypt, db, Messaging, mail
import secrets
from flask_mail import Message


admin = Blueprint('admin', __name__)


# Template function for Twilio api
# @admin.route('/twilio')
# @login_required
# def twilio():
#     message = Messaging.client.messages.create(
#         body='I am texting myself from my wedding app!',
#         from_=Messaging.from_phone,
#         to='+447845012119'
#         )
#     return redirect(url_for('admin.dashboard'))


@admin.route('/send_invitations')
@login_required
def send_invitations():
    # page restricted to admins. Redirect is user is not an admin (bride/groom)
    if current_user.guest_type != 'Admin':
        return redirect(url_for('main.home'))
    else:
        # get all guests details
        guests = Users.query.all()
        for guest in guests:
            # if the guest has a British mobile phone number stored, send their invitation
            # via text message
            if guest.number:
                if guest.number.startswith('+44'):
                    invitation_sms(guest)
            # if guest does not have a phone number stored, or their phone number is
            # not British, send them an email
            elif guest.email:
                invitation_email(guest)
            # if all of the above fails, text groom the details
            else:
                error_sms(guest)
    return redirect(url_for('admin.dashboard'))


def invitation_sms(guest):
    token = guest.get_reset_token()
    message = Messaging.client.messages.create(
        body=f'''Hi {guest.name}, you've been invited to Kirk & Vanela's Wedding. \n
        Please visit the below link to RSVP and find other info about the day. \n
        Hope to see you then! \n
        Kirk and Vanela. \n
        {url_for('users.welcome_page', token=token, _external=True)}''',
        from_=Messaging.from_phone,
        to=guest.number
        )


def invitation_email(guest):
    token = guest.get_reset_token()
    msg = Message("Kirk and Vanela's Wedding",
            sender='noreply@demo.com',
            recipients=[guest.email])
    msg.body = f'''Hi {guest.name}, you've been invited to Kirk and Vanela's Wedding.
    Please visit the below link to RSVP and find other info about the day.
    Hope to see you then!
    Kirk and Vanela.
    {url_for('users.welcome_page', token=token, _external=True)}'''
    mail.send(msg)


def error_sms(guest):
    msg = Messaging.client.messages.create(
        body=f'''{guest.name} was supposed to receive an invitation, but an error occurred.
        Please check that they have an email address or phone number stored.''',
        from_=Message.from_phone,
        to=Message.groom_phone
        )


@admin.route('/dasboard')
@login_required
def dashboard():
    # page restricted to admins. Redirect is user is not an admin (bride/groom)
    if current_user.guest_type != 'Admin':
        return redirect(url_for('main.home'))
    else:
        # get guests from db - count how many are evening guests,
        # and how many are invited for the whole day
        day_guests = Users.query.filter_by(guest_type='Day').count()
        evening_guests = Users.query.filter_by(guest_type='Evening').count()
        # call function to calculate total wedding expenses
        costs = calc_cost()
        return render_template('dashboard.html', title='Dashboard',
                costs=costs,
                day_guests=day_guests,
                evening_guests=evening_guests)


def calc_cost():
    day_guests = Users.query.filter_by(guest_type='Day').count()
    evening_guests = Users.query.filter_by(guest_type='Evening').all()
    evening_cost = 0
    # evening guests are charged at £12 each
    for guest in evening_guests:
        evening_cost += 12
        # also account for additional related guests i.e. +1s
        if guest.additional_guests > 0:
            evening_cost += int(guest.additional_guests*12)
    # day guests are accounted for in the cost of the venue, unless the number
    # exceeds 30. Each additional full-day guest then costs £85 per head
    if day_guests > 30:
        day_cost = (day_guests-30)*85
    else:
        day_cost = 0
    # calculate total cost of guests
    guests_cost = day_cost + evening_cost
    # get all venue-related expenses
    venue = Expenses.query.filter_by(cost_type='Venue').all()
    venue_cost = 0
    venue_paid = 0
    for i in venue:
        # calculate all venue related expenses & and all venue-related payments made
        venue_cost += i.cost
        venue_paid += i.paid
    # get expenses for rings
    rings = Expenses.query.filter_by(cost_type='Rings').all()
    rings_cost = 0
    rings_paid = 0
    for i in rings:
        # calculate total ring expenses & all ring expenses already paid
        rings_cost += i.cost
        rings_paid += i.paid
    # get expenses for clothing eg dress, suit etc
    clothing = Expenses.query.filter_by(cost_type='Clothes').all()
    clothing_cost = 0
    clothing_paid = 0
    for i in clothing:
        # calculate total clothing related costs & and all clothing payments made
        clothing_cost += i.cost
        clothing_paid += i.paid
    # get all miscellaneous expenses
    extras = Expenses.query.filter_by(cost_type='Other').all()
    extras_cost = 0
    extras_paid = 0
    for i in extras:
        # calculate miscellaneous expenses and all payments made
        extras_cost += i.cost
        extras_paid += i.paid
    # calculate total expenses, and total payments made
    total_cost = guests_cost + rings_cost + clothing_cost + extras_cost + venue_cost
    total_paid = rings_paid + clothing_paid + extras_paid + venue_paid
    # return results as a dictionary for access and rendering in HTML page
    return {
            'guests': {
                'cost': guests_cost
                },
            'rings': {
                'cost': rings_cost,
                'paid': rings_paid
                },
            'clothing': {
                'cost': clothing_cost,
                'paid': clothing_paid
                },
            'extras': {
                'cost': extras_cost,
                'paid': extras_paid
                },
            'venue': {
                'cost': venue_cost,
                'paid': venue_paid
                },
            'total': {
                'cost': total_cost,
                'paid': total_paid
                }
            }


@admin.route('/add-guests', methods=['POST', 'GET'])
@login_required
def add_guests():
    # page restricted to admins. Redirect is user is not an admin (bride/groom)
    if current_user.guest_type != 'Admin':
        return redirect(url_for('main.home'))
    else:
        # generate and render AddGuestForm
        form = AddGuestForm()
        # if form alidated successfully, add form values to database as a new guest
        if form.validate_on_submit():
            # generate a random encrypted password for the guest
            password = bcrypt.generate_password_hash(secrets.token_hex(8)).decode('utf-8')
            # additional guests form field is rendered as a string, below converts it to an integer
            additional_guests_int = int(form.additional_guests.data)
            user = Users(name=form.name.data,
                        email=form.email.data,
                        password=password,
                        additional_guests=additional_guests_int,
                        additional_guest_names=form.additional_guest_names.data,
                        guest_type=form.guest_type.data,
                        language=form.language.data)
            db.session.add(user)
            db.session.commit()
            flash(f'{form.name.data} has been added to the guest list.', 'success')
            return redirect(url_for('admin.dashboard'))
        elif request.method == 'GET':
            # prepopulate phone number form field with '+44'
            form.number.data = '+44'
        return render_template('add_guests.html', title='Add Guests',
            form=form)


@admin.route('/view-guests')
@login_required
def view_guests():
    # page restricted to admins. Redirect is user is not an admin (bride/groom)
    if current_user.guest_type != 'Admin':
        return redirect(url_for('main.home'))
    else:
        day_guests = Users.query.filter_by(guest_type='Day').all()
        evening_guests = Users.query.filter_by(guest_type='Evening').all()
        return render_template('view_guests.html', title='View Guests',
                day_guests=day_guests,
                evening_guests=evening_guests)


@admin.route('/edit-guest/<string:guest_name>', methods=['POST', 'GET'])
@login_required
def edit_guest(guest_name):
    # page restricted to admins. Redirect is user is not an admin (bride/groom)
    if current_user.guest_type != 'Admin':
        return redirect(url_for('main.home'))
    else:
        form = EditGuestForm()
        # get the queried guest details from db
        guest = Users.query.filter_by(name=guest_name).first()
        # if form validated successfully, update the guests record in database
        if form.validate_on_submit():
            guest.name = form.name.data
            guest.email = form.email.data
            guest.number = form.number.data
            guest.additional_guests = int(form.additional_guests.data)
            guest.additional_guest_names = form.additional_guest_names.data
            guest.is_attending = form.is_attending.data
            guest.guest_type = form.guest_type.data
            guest.language = form.language.data
            db.session.commit()
            flash(f'{guest.name} has been updated.', 'success')
        elif request.method == 'GET':
            # prepopulate form fields with guest data
            form.name.data = guest.name
            form.email.data = guest.email
            form.number.data = guest.number
            form.additional_guests.data = str(guest.additional_guests)
            form.additional_guest_names.data = guest.additional_guest_names
            form.guest_type.data = guest.guest_type
            form.language.data = guest.language
        return render_template('edit_guest.html', title='Edit Guest',
                form=form, guest=guest)


@admin.route('/delete_guest/<int:guest_id>', methods=['POST', 'GET'])
@login_required
def delete_guest(guest_id):
    # page restricted to admins. Redirect is user is not an admin (bride/groom)
    if current_user.guest_type != 'Admin':
        return redirect(url_for('main.home'))
    else:
        # get guest data for deletion
        guest = Users.query.get(guest_id)
        if guest:
            db.session.delete(guest)
            db.session.commit()
            flash(f'Guest deleted.', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash(f'Could not find that user in the database!')
            return redirect(url_for('admin.dashboard'))


@admin.route('/add-expenses', methods=['GET', 'POST'])
@login_required
def add_expenses():
    # page restricted to admins. Redirect is user is not an admin (bride/groom)
    if current_user.guest_type != 'Admin':
        return redirect(url_for('main.home'))
    else:
        form = AddExpensesForm()
        # if AddExpensesForm validates successfully, add the record to the database
        if form.validate_on_submit():
            expense = Expenses(title=form.title.data,
                            cost_type=form.cost_type.data,
                            notes=form.notes.data,
                            cost=form.cost.data)
            db.session.add(expense)
            db.session.commit()
            flash(f'{form.title.data} added.', 'success')
            return redirect(url_for('admin.view_expenses'))
        return render_template('add_expenses.html', title='Add Expenses',
                form=form)


@admin.route('/view_expenses')
@login_required
def view_expenses():
    # page restricted to admins. Redirect is user is not an admin (bride/groom)
    if current_user.guest_type != 'Admin':
        return redirect(url_for('main.home'))
    else:
        expenses = Expenses.query.all()
        return render_template('view_expenses.html', title='View Expenses',
              expenses=expenses)

@admin.route('/edit-expense/<int:expense_id>', methods=['POST', 'GET'])
@login_required
def edit_expense(expense_id):
    # page restricted to admins. Redirect is user is not an admin (bride/groom)
    if current_user.guest_type != 'Admin':
        return redirect(url_for('main.home'))
    else:
        # two forms rendered on Edit page:
        # First to edit the queried expenses
        # Second to update payments made for the expense
        form = EditExpensesForm()
        update_form = UpdatePaymentForm()
        # get queried expense from db
        expense = Expenses.query.get(expense_id)
        if update_form.validate_on_submit():
            # if UpdatePaymentForm validates successfully, commit the changes to db
            expense.paid += update_form.payment.data
            db.session.commit()
            flash(f'{expense.title} updated.', 'success')
            return redirect(url_for('admin.view_expenses'))
        # if EditExpensesForm validates successfully, commit the changes to db
        if form.validate_on_submit():
            expense.title = form.title.data
            expense.cost_type = form.cost_type.data
            expense.notes = form.notes.data
            expense.cost = form.cost.data
            db.session.commit()
            flash(f'{form.title.data} updated.', 'success')
            return redirect(url_for('admin.view_expenses'))
        # prepopulate form fields with expense data
        elif request.method == 'GET':
            form.title.data = expense.title
            form.cost_type.data = expense.cost_type
            form.notes.data = expense.notes
            form.cost.data = expense.cost
    return render_template('edit_expenses.html', title='Edit expense',
                form=form,
                expense=expense,
                update_form=update_form)


@admin.route('/delete-expense/<int:expense_id>')
@login_required
def delete_expense(expense_id):
    # page restricted to admins. Redirect is user is not an admin (bride/groom)
    if current_user.guest_type != 'Admin':
        return redirect(url_for('main.home'))
    else:
        expense = Expenses.query.get(expense_id)
        if expense:
            db.session.delete(expense)
            db.session.commit()
        return redirect(url_for('admin.view_expenses'))
