from flask_socketio import SocketIO
from flask import Flask, redirect, session

from dotenv import load_dotenv

from functools import wraps

import os


load_dotenv()

socketio = SocketIO(async_mode='eventlet')


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)

        return redirect('/')

    return wrap

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['FLASK_SECRET']

    from .SocketEvents import socket_events
    from .Movies import movies
    from .Auth import auth

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(movies, url_prefix='/')
    app.register_blueprint(socket_events, url_prefix='/socket_events')

    socketio.init_app(app)

    return app
