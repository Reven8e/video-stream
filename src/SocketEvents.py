from flask import Blueprint
from flask_socketio import Namespace, join_room, emit

from src import socketio

socket_events = Blueprint('socket_events', __name__)


class StreamManager(Namespace):
    def on_join(self, data):
        room_code = data['session_code']
        join_room(room_code)
        emit('new_user_joined', {'session_code': room_code}, room=room_code)

    def on_sync_command(self, data):
        session_code = data['session_code']
        emit('sync_action', data, room=session_code, include_self=False)

    def on_report_current_time(self, data):
        session_code = data['session_code']
        emit('update_time', {'currentTime': data['currentTime']}, room=session_code)

socketio.on_namespace(StreamManager('/StreamManager'))
