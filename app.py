from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, disconnect
from collections import deque
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Store user info: sid -> {'name': ..., 'is_admin': ...}
users = {}

# Last 100 messages
chat_history = deque(maxlen=100)
CHAT_HISTORY_FILE = 'chat_history.txt'

@app.route('/')
def index():
    return render_template('index.html')

# Send chat history on connect
@socketio.on('connect')
def handle_connect():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'r') as f:
            for line in f.readlines()[-100:]:
                emit('message', line.strip())

@socketio.on('join')
def handle_join(data):
    username = data.get('username', 'Anonymous')
    is_admin = data.get('is_admin', False)
    display_name = f"{username} (admin)" if is_admin else username
    users[request.sid] = {'name': display_name, 'is_admin': is_admin}
    send(f"{display_name} joined the chat.")
    emit_user_list()

@socketio.on('message')
def handle_message(msg):
    print(f"Received message: {msg}")
    chat_history.append(msg)
    with open(CHAT_HISTORY_FILE, 'a') as f:
        f.write(msg + '\n')
    send(msg, broadcast=True)

@socketio.on('typing')
def handle_typing(username):
    emit('show_typing', username, broadcast=True, include_self=False)

@socketio.on('disconnect')
def handle_disconnect():
    user = users.pop(request.sid, {'name': 'Someone'})
    send(f"{user['name']} left the chat.", broadcast=True)
    emit_user_list()

def emit_user_list():
    user_list = [{'sid': sid, 'name': data['name']} for sid, data in users.items()]
    socketio.emit('update_user_list', user_list)

@socketio.on('kick_user')
def handle_kick(target_sid):
    kicker = users.get(request.sid, {})
    if not kicker.get('is_admin'):
        return  # Only admins can kick

    if target_sid in users:
        kicked_user = users[target_sid]['name']
        emit('message', f"{kicked_user} was kicked by {kicker['name']}.", broadcast=True)
        socketio.emit('kicked', room=target_sid)
        disconnect(sid=target_sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)
