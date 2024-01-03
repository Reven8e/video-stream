from flask import Blueprint
from flask_socketio import SocketIO, join_room, leave_room

socket_events = Blueprint('socket_events', __name__)
socketio = SocketIO()

@socketio.on('join', namespace='/socket_events')
def on_join(data):
    room_code = data['session_code']
    join_room(room_code)
    socketio.emit('new_user_joined', {'session_code': room_code}, room=room_code)

@socketio.on('sync_command', namespace='/socket_events')
def handle_sync_command(data):
    session_code = data['session_code']
    socketio.emit('sync_action', data, room=session_code, include_self=False)

@socketio.on('report_current_time', namespace='/socket_events')
def handle_report_current_time(data):
    session_code = data['session_code']
    socketio.emit('update_time', {'currentTime': data['currentTime']}, room=session_code)
