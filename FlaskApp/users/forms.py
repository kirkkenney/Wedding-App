from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                    SelectField, IntegerField)
from wtforms.validators import (DataRequired, Email, EqualTo, ValidationError)
from FlaskApp.models import Users


class LoginForm(FlaskForm):
    number = StringField('Phone Number (use international dialling code)')
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RSVPForm(FlaskForm):
    is_attending = SelectField('Are You Attending?', validators=[DataRequired()],
                    choices=[
                    ('Unsure', 'Unsure'), ('Yes', 'Yes'), ('No', 'No')
                    ])
    password = PasswordField('Choose A Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Your Password', validators=[
                        DataRequired(),
                        EqualTo('password', message='Passwords must match')
                        ])
    submit = SubmitField('Submit')


class RequestResetForm(FlaskForm):
    number = StringField('Phone Number (use international dialling code)')
    submit = SubmitField('Request Password Reset')

    def validate_number(self, number):
        user = Users.query.filter_by(number=number.data).first()
        if user is None:
            raise ValidationError('''There is no account with that phone number,
                please try again or speak to Kirk/Vanela.''')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')