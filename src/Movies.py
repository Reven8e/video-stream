from flask import Blueprint, render_template, flash, redirect, url_for, session, request

from datetime import datetime, timedelta
import json

from src.DBMS import DBMS
from src.DBInterfaces import PostgresDatabase
from src.CodeManage import CodeManage
from src import login_required
from flask import redirect, url_for, flash

movies = Blueprint('movies', __name__)

@movies.route("/videostream/available_movies", methods=["GET", "POST"])
@login_required
def available_movies():
    """
    Retrieves the list of available movies from the database and handles the logic for generating and checking access codes.

    Returns:
        If the HTTP request method is POST:
            - If a valid movie_id and expiration_date_delta are provided, generates an access code and redirects to the videostream page.
            - If a valid form_access_code is provided, checks the access code and redirects to the videostream page if it is valid.
            - If neither movie_id and expiration_date_delta nor form_access_code are provided, returns an error message.

        If the HTTP request method is not POST:
            - Retrieves the list of available movies from the database and renders the available_movies.html template.

    Raises:
        - If there is an error fetching movies from the database, returns an error message.
        - If there is an error generating or checking the access code, returns an error message.
    """
    db = DBMS(PostgresDatabase())
    movies_statement, movies = db.fetch_movies()
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
                if movies_statement is False:
                    return render_template("available_movies.html", movies=[]), flash(f"Error: {movies}\nError: Access Code Creation Error", category='danger'), 500

                return render_template("available_movies.html", movies=movies), flash(f"Error: Access Code Creation Error", category='danger'), 500

        elif form_access_code:
            code_manager = CodeManage()
            check_code_statement, check_code_data = code_manager.check_access_code(form_access_code)
            if check_code_statement is True:
                access_code = form_access_code
            else:
                return render_template("available_movies.html", movies=movies), flash(f"Error: {check_code_data}| Access Code: {form_access_code}", category='danger'), 500

        return redirect(url_for('movies.videostream', access_code=access_code)), flash(f"Connecting to stream | Access Code: {access_code}", category='success')

    if movies_statement is False:
        return render_template("available_movies.html", movies=[]), flash(f"Error: {movies}", category='danger'), 500

    return render_template("available_movies.html", movies=movies)

@movies.route("/videostream/watch/<access_code>")
@login_required
def videostream(access_code):
    """
    Function to handle video streaming.

    Parameters:
    access_code (str): The access code for the video.

    Returns:
    response: The response object for the video streaming page.
    """

    code_manager = CodeManage()
    statement, check_code = code_manager.check_access_code(access_code)

    if statement is False:
        return redirect(url_for('movies.available_movies')), flash(f"Invalid access code: {access_code} | Error: {access_code}", category='danger'), 400

    db = DBMS(PostgresDatabase())
    statement, movie_obj = db.fetch_movie(check_code[1])
    db.close_connection()

    if statement is False:
        return redirect(url_for('movies.available_movies')), flash(f"Error: {movie_obj}", category='danger'), 500
    
    user_id = json.loads(session['user'])['user_id']

    return render_template("videostream.html", access_code=access_code, movie_path=movie_obj[2], user_id=user_id), 200
