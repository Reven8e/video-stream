from flask import Blueprint, render_template, flash, redirect, url_for, session, request

from src.DBMS import DBMS
from src import login_required

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        db = DBMS()
        statement, user = db.login_user(username, password)
        db.close_connection()

        if statement is True:
            session['logged_in'] = True
            session['user'] = user
            return redirect(url_for('movies.available_movies')), flash("Signed in in successfully!", category='success')
        
        else:
            flash(user, category='danger')

    return render_template("login.html")

@auth.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(username) < 3:
            flash("First name must be greater than 3 characters.", category='danger')

        elif password1 != password2:
            flash("Passwords dont match.", category='error')
        
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category='danger')

        else:
            db = DBMS()
            statement, data = db.register_user(username, password1)
            db.close_connection()

            if statement is True:
                session['logged_in'] = True
                session['user'] = data
                return redirect(url_for('movies.available_movies')), flash("Account created successfully!", category='success')
            else:
                flash(data, category='danger')

    return render_template("signup.html")

@auth.route('/signout')
@login_required
def sign_out():
    session.clear()
    return redirect(url_for('auth.login')), flash('You have signed out.', 'success')
