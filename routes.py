from tickets import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required  
from tickets.models import db, Flight, Seat, Order, Passenger, User
from tickets.forms import PassengerForm, TicketPurchaseForm, RegisterForm, LoginForm  
from tickets import db
from __init__ import create_app  

# Initialize app
app = create_app()

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/flights', methods=['GET', 'POST'])
@login_required
def flights_page():
    ticket_form = TicketPurchaseForm()
    if request.method == "POST":
        # Ticket Purchase Logic
        selected_flight_id = request.form.get('selected_flight')
        flight_object = Flight.query.get(selected_flight_id)
        if flight_object:
            if current_user.can_book(flight_object):  # Assuming can_book() exists in User model
                flight_object.book(current_user)  # Assuming book() exists in Flight model
                flash(f"Successfully booked flight {flight_object.flight_number} to {flight_object.destination}!", category='success')
            else:
                flash(f"Unable to book flight {flight_object.flight_number}. Please check availability or your account balance.", category='danger')

        return redirect(url_for('flights_page'))

    if request.method == "GET":
        available_flights = Flight.query.filter_by(available=True)  # Assuming available column exists
        return render_template('flights.html', flights=available_flights, ticket_form=ticket_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(passport_id=form.passport_id.data,  # Change to passport_id instead of username
                              country=form.country.data,  # Add country field
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.passport_id}", category='success')
        return redirect(url_for('flights_page'))
    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()  # Create an instance of LoginForm
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(passport_id=form.passport_id.data).first()  # Changed to passport_id
        if attempted_user and attempted_user.check_password_correction(  # Assuming this method exists
                attempted_password=form.password.data
        ):
            login_user(attempted_user)  # Log the user in
            flash(f'Success! You are logged in as: {attempted_user.passport_id}', category='success')  # Changed to passport_id
            return redirect(url_for('flights_page'))  # Redirect to the flights page after login
        else:
            flash('Passport ID and password do not match! Please try again', category='danger')

    return render_template('login.html', form=form)  # Render the login.html template

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))
