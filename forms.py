from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, FieldList, FormField
from wtforms.validators import DataRequired, Regexp, EqualTo, Length, EqualTo, Email, DataRequired, ValidationError
from tickets.models import User

class PassengerForm(FlaskForm):
    name = StringField('Passenger Name', validators=[DataRequired()])
    seat = SelectField('Seat Number', choices=[], coerce=int)

class TicketPurchaseForm(FlaskForm):
    flight = SelectField('Flight', choices=[], coerce=int)
    passengers = FieldList(FormField(PassengerForm), min_entries=1, max_entries=5)
    submit = SubmitField('Purchase Tickets')

class RegisterForm(FlaskForm):
    passport_id = StringField('Passport ID', validators=[
        DataRequired(),
        Regexp(r'^[A-Za-z0-9]+$', message="Passport ID must contain letters and numbers only.")  # Accept only letters and numbers
    ])
    country = StringField('Country', validators=[DataRequired()])
    email_address = StringField('Email Address', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password1', message='Passwords must match')])  # Password match validator
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    passport_id = StringField('Passport ID', validators=[
        DataRequired(),
        Regexp(r'^[A-Za-z0-9]+$', message="Passport ID must contain letters and numbers only.")  # Accept only letters and numbers
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
