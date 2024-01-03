from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from flask_bcrypt import Bcrypt
from src.DBMS import DBMS
from src import login_required

auth = Blueprint('auth', __name__)


@auth.route("/sign-in", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        db = DBMS()
        statement, user = db.login_user(username, password)

        if statement is True:
            session['logged_in'] = True
            session['user'] = user
            return redirect(url_for('views.home')), flash("Signed in in successfully!", category='success')
        
        else:
            flash(user, category='error')

    return render_template("login.html")
