from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)


@auth.route('login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if (user.password, password):
                flash('logged in succesfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))

            else:
                flash('Incorrect' , category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('signup', methods=['GET', 'POST']) # get is retrieving data, post is if it sent (button pressed)
def signup():
    if request.method == 'POST': #if button is clicked
        email = request.form.get('email') # get function, to get data from the entered post
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('email already exist!', category='error')
        elif len(email) < 4:
            flash(' Email must be longer ', category='error') #flash
        elif len(first_name) < 2:
            flash(' Firstname must be longer ', category='error')
        elif password1 != password2:
            flash(' NOT THE SAME ', category='error')
        elif len(password1) < 7:
            flash(' BRUH ', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=password1)
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash(' Account Created! ', category='success')
            return redirect(url_for('views.home')) #views is the page, home is the home url

    return render_template("signup.html", user=current_user)