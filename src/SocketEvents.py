from flask import Blueprint
from flask_socketio import Namespace, join_room, emit

from src import socketio

socket_events = Blueprint('socket_events', __name__)


class StreamManager(Namespace):
    """
    Class representing a stream manager.

    This class handles various socket events related to streaming.

    Attributes:
        None

    Methods:
        on_join: Handles the 'join' event when a user joins a session.
        on_sync_command: Handles the 'sync_command' event when a sync command is received.
        on_report_current_time: Handles the 'report_current_time' event when the current time is reported.
    """
    
    def on_join(self, data):
        """
        Handles the 'join' event when a user joins a session.

        Args:
            data (dict): The data received from the client.
        """
        print('on_join', data)
        room_code = data['session_code']
        join_room(room_code)
        emit('new_user_joined', {'session_code': room_code}, room=room_code)

    def on_sync_command(self, data):
        """
        Handles the 'sync_command' event when a sync command is received.

        Args:
            data (dict): The data received from the client.
        """
        print('on_sync_command', data)
        session_code = data['session_code']
        emit('sync_action', data, room=session_code, include_self=False)

    def on_report_current_time(self, data):
        """
        Handles the 'report_current_time' event when the current time is reported.

        Args:
            data (dict): The data received from the client.
        """
        print('on_report_current_time', data)
        session_code = data['session_code']
        emit('update_time', {'currentTime': data['currentTime']}, room=session_code)

socketio.on_namespace(StreamManager('/StreamManager'))
