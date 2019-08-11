from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                    SelectField)
from wtforms.validators import (DataRequired, Email, EqualTo)


class LoginForm(FlaskForm):
    email = StringField('Email Address')
    number = StringField('Phone Number')
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RSVPForm(FlaskForm):
    email = StringField('Your Email', validators=[Email()])
    number = StringField('Your Number')
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
