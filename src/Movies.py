from flask import Blueprint, render_template, flash, redirect, url_for, session, request

from datetime import datetime, timedelta
import json

from src.DBMS import DBMS
from src.CodeManage import CodeManage
from src import login_required

movies = Blueprint('movies', __name__)

@movies.route("/videostream/available_movies", methods=["GET", "POST"])
@login_required
def available_movies():
    db = DBMS()
    statement, movies = db.fetch_movies()
    db.close_connection()

    if request.method == "POST":
        movie_id = request.form.get("movie_id")
        form_access_code = request.form.get("access_code")
        expiration_date_delta = request.form.get("expiration_date")

        if movie_id and expiration_date_delta:
            expiration_date = datetime.utcnow() + timedelta(days=int(expiration_date_delta))

            code_manager = CodeManage()
            access_code = code_manager.generate_access_code(json.loads(session['user'])['user_id'], int(movie_id), expiration_date)
            if access_code is None:
                return render_template("available_movies.html", movies=movies), flash(f"Error: Access Code Creation Error", category='danger')

        elif form_access_code:
            code_manager = CodeManage()
            check_code = code_manager.check_access_code(form_access_code)
            if check_code is True:
                access_code = form_access_code
            else:
                return render_template("available_movies.html", movies=movies), flash(f"Invalid access code. {form_access_code}", category='danger')

        return redirect(url_for('movies.videostream', access_code=access_code)), flash(f"Connecting to stream | Access Code: {access_code}", category='success')

    return render_template("available_movies.html", movies=movies)

@movies.route("/videostream/watch/<access_code>")
@login_required
def videostream(access_code):
    code_manager = CodeManage()
    statement, check_code = code_manager.check_access_code(access_code)

    if statement is False:
        return redirect(url_for('movies.available_movies')), flash(f"Invalid access code: {access_code} | Error: {access_code}", category='danger')

    db = DBMS()
    statement, movie_obj = db.fetch_movie(check_code[1])
    db.close_connection()

    if statement is False:
        return redirect(url_for('movies.available_movies')), flash(f"Error: {movie_obj}", category='danger')
    
    user_id = json.loads(session['user'])['user_id']

    return render_template("videostream.html", access_code=access_code, movie_path=movie_obj[2], user_id=user_id)
