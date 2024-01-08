from flask import Blueprint, render_template, flash, redirect, url_for, session, request

from src.DBInterfaces import PostgresDatabase
from src.DBMS import DBMS
from src import login_required

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles the login functionality.

    This function is responsible for handling the login process. It retrieves the username and password from the request form,
    validates them against the user database, and sets the session variables accordingly. If the login is successful, the user
    is redirected to the available movies page. Otherwise, an error message is displayed.

    Returns:
        If the login is successful, the function redirects the user to the available movies page. Otherwise, it renders the login.html template.
    """
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        db = DBMS(PostgresDatabase())
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
    """
    Handles the sign-up functionality.

    This function is responsible for handling the sign-up process when a user submits the sign-up form.
    It validates the username and password entered by the user, registers the user in the database,
    and sets the session variables if the sign-up is successful.

    Returns:
        If the sign-up is successful, it redirects the user to the available_movies page and displays a success message.
        If there is an error during the sign-up process, it displays an appropriate error message.

    """
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
            db = DBMS(PostgresDatabase())
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
    """
    Clears the session and redirects the user to the login page.
    
    Returns:
        A redirect response to the login page.
    """
    session.clear()
    return redirect(url_for('auth.login')), flash('You have signed out.', 'success')
