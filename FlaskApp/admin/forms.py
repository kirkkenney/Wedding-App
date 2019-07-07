from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, IntegerField, SelectField,
                    TextAreaField, FloatField)
from wtforms.validators import (DataRequired, Email, ValidationError)
from FlaskApp.models import Users


class AddGuestForm(FlaskForm):
    name = StringField('Guest Name', validators=[DataRequired()])
    email = StringField('Guest Email')
    number = StringField('Guest Phone Number')
    additional_guests = SelectField('Number Of Additional Guests',
                        choices=[
                        ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')
                        ])
    additional_guest_names = StringField('Additional Guest Names (separated by commas)')
    guest_type = SelectField('Guest Type', validators=[DataRequired()],
            choices=[('Day', 'Day'), ('Evening', 'Evening'), ('Admin', 'Admin')])
    language = SelectField('Guest Language', validators=[DataRequired()],
            choices=[('english', 'English'), ('romanian', 'Romanian')])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        approved_email = Users.query.filter_by(email=email.data).first()
        if approved_email:
            raise ValidationError('That email is taken. Please choose a different one')


class EditGuestForm(FlaskForm):
    name = StringField('Guest Name', validators=[DataRequired()])
    email = StringField('Guest Email')
    number = StringField('Guest Phone Number')
    additional_guests = SelectField('Number Of Additional Guests',
                        choices=[
                        ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')
                        ])
    additional_guest_names = StringField('Additional Guest Names (separated by commas)')
    is_attending = SelectField('Are They Attending?', validators=[DataRequired()],
                    choices=[
                    ('Unsure', 'Unsure'), ('Yes', 'Yes'), ('No', 'No')
                    ])
    guest_type = SelectField('Guest Type', validators=[DataRequired()],
            choices=[('Day', 'Day'), ('Evening', 'Evening'), ('Admin', 'Admin')])
    language = SelectField('Guest Language', validators=[DataRequired()],
            choices=[('english', 'English'), ('romanian', 'Romanian')])
    submit = SubmitField('Submit')


class AddExpensesForm(FlaskForm):
    title = StringField('What Are You Adding?', validators=[DataRequired()])
    cost_type = SelectField('What Is The Expense For?',
                validators=[DataRequired()],
                choices=[('Venue', 'Venue'), ('Rings', 'Rings'), ('Clothes', 'Clothes'), ('Other', 'Other')])
    notes = TextAreaField('Any Additional Notes?')
    cost = FloatField('How Much Does It Cost?')
    submit = SubmitField('Submit')


class EditExpensesForm(FlaskForm):
    title = StringField('What Are You Adding?', validators=[DataRequired()])
    cost_type = SelectField('What Is The Expense For?',
                validators=[DataRequired()],
                choices=[('Venue', 'Venue'), ('Rings', 'Rings'), ('Clothes', 'Clothes'), ('Other', 'Other')])
    notes = TextAreaField('Any Additional Notes?')
    cost = FloatField('How Much Does It Cost?')
    submit = SubmitField('Submit')


class UpdatePaymentForm(FlaskForm):
    payment = FloatField('How Much Have You Paid?',
                validators=[DataRequired()])
    submit = SubmitField('Submit')
