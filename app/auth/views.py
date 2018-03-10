# app/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import Gamer

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        gamer = Gamer(email=form.email.data, username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, password=form.password.data)

        # add gamer to the database
        db.session.add(gamer)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log a gamer in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether gamer exists in the database and whether
        # the password entered matches the password in the database
        gamer = Gamer.query.filter_by(email=form.email.data).first()
        if gamer is not None and gamer.verify_password(
                form.password.data):
            # log employee in
            login_user(gamer)

            # redirect to the dashboard page after login
            return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log a gamer out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))
