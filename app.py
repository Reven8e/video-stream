from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit, leave_room

from dotenv import load_dotenv

import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET']
socketio = SocketIO(app)


@app.route('/watch_video/<session_code>')
def watch_video(session_code):
    video_path = '/static/video2/output.m3u8'
    return render_template('watch.html', video_url=video_path, session_code=session_code)


@socketio.on('join')
def on_join(data):
    room_code = data['session_code']
    join_room(room_code)
    emit('new_user_joined', {'session_code': room_code}, room=room_code)

@socketio.on('leave')
def on_leave(data):
    room_code = data['session_code']
    leave_room(room_code)

@socketio.on('sync_command')
def handle_sync_command(data):
    session_code = data['session_code']
    emit('sync_action', data, room=session_code, include_self=False)

@socketio.on('report_current_time')
def handle_report_current_time(data):
    session_code = data['session_code']
    emit('update_time', {'currentTime': data['currentTime']}, room=session_code)

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5003)
