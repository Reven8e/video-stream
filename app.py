from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/watch_video/<code>')
def watch_video(code):
    video_path = '/static/video1/output.m3u8'
    return render_template('watch.html', video_url=video_path, session_code=code)

@socketio.on('join')
def on_join(data):
    room = data['session_code']
    join_room(room)

@socketio.on('leave')
def on_leave(data):
    room = data['session_code']
    leave_room(room)

@socketio.on('sync_command')
def handle_sync_command(data):
    action = data.get('action')
    currentTime = data.get('currentTime')
    session_code = data.get('session_code')

    socketio.emit('sync_action', {
        'action': action,
        'currentTime': currentTime
    }, room=session_code, include_self=False)

if __name__ == "__main__":
    socketio.run(app, debug=True)
